"""Pass 1.5: allow-list resolution via Rust source static parsing (SPEC v0.6 §2.3 M5a).

v0.6 amends the original §2.3 plan: instead of building an in-workspace shim
crate against codex-core (impractical due to publish=false, async tokio,
Session dependencies), we use static Rust source parsing for the bulk of
the prompt-bearing constants and inline strings. The shim crate falls back
to M5c (optional) if static parsing leaves coverage gaps.

This module supports three entry kinds:
  - rust_const_str        : `(pub )?const SYMBOL: &str = r#"..."#;`
  - rust_fn_static_str    : `fn SYMBOL(...) -> &'static str { r#"..."# }`
  - rust_inline_at_marker : find marker line, then first r#"..."# below it
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

# Rust raw string `r#"..."#`. DOTALL so newlines are matched.
# Note: Rust supports r##"..."## (and more #s) for nesting; M5a handles only the single-# form
# which is what codex uses for the targeted constants (verified at rust-v0.126.0-alpha.12).
_RAW_STR_RX = re.compile(r'r#"(?P<body>.*?)"#', re.DOTALL)

# Plain double-quoted string with basic escape support, single-line.
_PLAIN_STR_RX = re.compile(r'"(?P<body>(?:[^"\\]|\\.)*)"')


@dataclass(frozen=True)
class AllowListCapture:
    """A captured prompt fragment from the allow-list, ready for Pass 3 emit."""

    body: str
    category: str
    filename: str
    description: str
    source_rel: Path           # relative to codex-rs/
    source_line: int           # 1-indexed
    source_kind: str           # frontmatter source.kind
    extraction_method: str     # rust_const_str | rust_fn_static_str | rust_inline_at_marker
    symbol: str | None
    extra: dict = field(default_factory=dict)


def load(extractor_dir: Path) -> list[dict]:
    """Load entries from allow_list.toml. Returns [] if no [[entry]] items."""
    with open(extractor_dir / "allow_list.toml", "rb") as f:
        data = tomllib.load(f)
    return data.get("entry", [])


def _line_of(text: str, char_idx: int) -> int:
    """1-indexed line number of a character offset."""
    return text[:char_idx].count("\n") + 1


def _find_const_assignment(text: str, symbol: str) -> int | None:
    """Find the `=` end-position of `(pub )?const SYMBOL: &str = ...` (or &'static str)."""
    pattern = rf"(?:pub\s+)?const\s+{re.escape(symbol)}\s*:\s*&\s*(?:'static\s+)?str\s*="
    m = re.search(pattern, text)
    return m.end() if m else None


def _extract_const_str(text: str, symbol: str) -> tuple[str, int] | None:
    """Extract value of `(pub )?const SYMBOL: &str = r#"..."#;` or simple `"..."`."""
    eq_end = _find_const_assignment(text, symbol)
    if eq_end is None:
        return None
    decl_line = _line_of(text, eq_end)
    # Try raw string first
    raw = _RAW_STR_RX.search(text, eq_end)
    if raw and raw.start() < eq_end + 200:  # close to assignment
        return raw.group("body"), decl_line
    # Try plain string literal (single-line).
    plain = _PLAIN_STR_RX.search(text, eq_end)
    if plain and plain.start() < eq_end + 200:
        # Decode common Rust string escapes (\\n, \\t, \\", \\\\).
        body = plain.group("body").encode("utf-8", "replace").decode("unicode_escape", "replace")
        return body, decl_line
    return None


def _extract_fn_static_str(text: str, symbol: str) -> tuple[str, int] | None:
    """Extract first r#"..."# inside `fn SYMBOL(...) -> &'static str { ... }`."""
    pattern = rf"fn\s+{re.escape(symbol)}\s*\([^)]*\)\s*->\s*&'static\s+str\s*\{{"
    m = re.search(pattern, text)
    if not m:
        return None
    body_start = m.end()
    # Track brace depth to find matching `}`.
    depth = 1
    pos = body_start
    while pos < len(text) and depth > 0:
        c = text[pos]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        pos += 1
    fn_body = text[body_start:pos]
    raw = _RAW_STR_RX.search(fn_body)
    if not raw:
        return None
    return raw.group("body"), _line_of(text, m.start())


def _extract_inline_at_marker(text: str, marker: str) -> tuple[str, int] | None:
    """Find marker; extract first r#"..."# starting from there."""
    idx = text.find(marker)
    if idx < 0:
        return None
    raw = _RAW_STR_RX.search(text, idx)
    if not raw:
        return None
    return raw.group("body"), _line_of(text, idx)


def resolve(entries: list[dict], codex_rs: Path) -> list[AllowListCapture]:
    """Resolve allow-list entries by parsing referenced Rust source files."""
    captures: list[AllowListCapture] = []
    for entry in entries:
        kind = entry.get("kind")
        rel = entry["file"]
        rs_path = codex_rs / rel
        if not rs_path.is_file():
            raise ValueError(f"allow_list: missing file codex-rs/{rel}")
        text = rs_path.read_text(encoding="utf-8")

        if kind == "rust_const_str":
            symbol = entry["symbol"]
            res = _extract_const_str(text, symbol)
            if res is None:
                raise ValueError(f"allow_list: const {symbol} not found in codex-rs/{rel}")
            body, line_no = res
            captures.append(
                AllowListCapture(
                    body=body,
                    category=entry["category"],
                    filename=entry["filename"],
                    description=entry.get("description", ""),
                    source_rel=Path(rel),
                    source_line=line_no,
                    source_kind="rust_const",
                    extraction_method=kind,
                    symbol=symbol,
                )
            )
        elif kind == "rust_fn_static_str":
            symbol = entry["symbol"]
            res = _extract_fn_static_str(text, symbol)
            if res is None:
                raise ValueError(f"allow_list: fn {symbol} not found in codex-rs/{rel}")
            body, line_no = res
            captures.append(
                AllowListCapture(
                    body=body,
                    category=entry["category"],
                    filename=entry["filename"],
                    description=entry.get("description", ""),
                    source_rel=Path(rel),
                    source_line=line_no,
                    source_kind="rust_fn_static",
                    extraction_method=kind,
                    symbol=symbol,
                )
            )
        elif kind == "rust_inline_at_marker":
            marker = entry["marker"]
            res = _extract_inline_at_marker(text, marker)
            if res is None:
                raise ValueError(
                    f"allow_list: marker '{marker}' not found in codex-rs/{rel}"
                )
            body, line_no = res
            captures.append(
                AllowListCapture(
                    body=body,
                    category=entry["category"],
                    filename=entry["filename"],
                    description=entry.get("description", ""),
                    source_rel=Path(rel),
                    source_line=line_no,
                    source_kind="rust_inline",
                    extraction_method=kind,
                    symbol=None,
                    extra={"marker": marker},
                )
            )
        else:
            raise ValueError(f"allow_list: unknown kind '{kind}'")

    return captures
