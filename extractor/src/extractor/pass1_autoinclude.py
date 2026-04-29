"""Pass 1: enumerate include_str!/include_bytes! callsites in shipping .rs files (SPEC §2.1 (A), §2.2)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Matches  include_str!("path/to/file")  and  include_bytes!(...).
# Tolerant of whitespace and line wraps. Multi-line tolerant via re.DOTALL? No —
# include_str! macros nearly always fit on one line in codex source. Keep simple.
INCLUDE_RX = re.compile(r"""include_(?P<kind>str|bytes)!\s*\(\s*"(?P<path>[^"]+)"\s*\)""")

# Heuristic test-block detector: a line is "in a test block" if a recent (within
# ~50 lines above) line declares #[cfg(test)] / #[cfg(any(test, ...))] /
# #[cfg(all(test, ...))] BEFORE the next non-cfg item attribute.
TEST_CFG_RX = re.compile(r"#\s*\[\s*cfg\s*\(\s*(?:any|all)?\s*\(?[^)]*\btest\b")


@dataclass(frozen=True)
class Candidate:
    """A single include_str!/include_bytes! capture."""

    target_path: Path           # absolute path to the included file
    target_rel: Path            # path relative to codex_rs root
    callsite_file: Path         # the .rs file containing the macro
    callsite_line: int          # 1-indexed line number
    kind: str                   # "str" | "bytes"


def _is_test_path(rel: Path) -> bool:
    parts = rel.parts
    if any(p in {"tests", "benches", "examples"} for p in parts):
        return True
    if rel.name in {"tests.rs", "test.rs"}:
        return True
    if rel.name.endswith(("_tests.rs", "_test.rs")):
        return True
    return False


_ITEM_RX = re.compile(
    r"^\s*(pub\s*(\([^)]*\)\s*)?)?(use|fn|struct|impl|trait|mod|enum|const|static|type|extern)\s"
)


def _is_test_block(lines: list[str], line_idx: int, lookback: int = 60) -> bool:
    """Heuristic: is the line at line_idx attached to a #[cfg(test)] attribute?

    A `#[cfg(test)]` attribute applies ONLY to the next item declaration. Walking
    backwards from line_idx, we collect contiguous attribute / comment / blank
    lines. The first non-attribute item line we hit *consumes* any earlier
    attributes — they don't apply to us. So we only return True if a cfg(test)
    is in the contiguous attribute prefix of our own item.

    NOTE: this misses enclosing `#[cfg(test)] mod tests { ... }` blocks. In
    practice, codex test fixtures using include_str! live under `tests/` paths
    which we already deny via `_is_test_path` / denylist. M5 may refine.
    """
    start = max(0, line_idx - lookback)
    for i in range(line_idx - 1, start - 1, -1):
        raw = lines[i]
        line = raw.strip()
        if not line or line.startswith("//") or line.startswith("/*"):
            continue
        if line.startswith("#["):
            if TEST_CFG_RX.search(line):
                return True
            continue  # other attribute; keep walking
        # Non-attribute, non-comment, non-blank line.
        # If it's an item declaration, the attributes above it are NOT ours.
        if _ITEM_RX.match(raw):
            return False
        # Otherwise (e.g. inside a function body), keep walking.
    return False


def walk(codex_rs: Path) -> list[Candidate]:
    """Walk codex-rs/ and collect include_str!/include_bytes! candidates."""
    out: list[Candidate] = []
    for rs in codex_rs.rglob("*.rs"):
        rel = rs.relative_to(codex_rs)
        if _is_test_path(rel):
            continue
        try:
            text = rs.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "include_str!" not in text and "include_bytes!" not in text:
            continue
        lines = text.splitlines()
        for line_idx, line in enumerate(lines):
            for m in INCLUDE_RX.finditer(line):
                if _is_test_block(lines, line_idx):
                    continue
                target = (rs.parent / m.group("path")).resolve()
                if not target.is_file():
                    continue
                try:
                    target_rel = target.relative_to(codex_rs)
                except ValueError:
                    # Target outside codex-rs/ (e.g., workspace-relative); skip
                    continue
                out.append(
                    Candidate(
                        target_path=target,
                        target_rel=target_rel,
                        callsite_file=rs,
                        callsite_line=line_idx + 1,
                        kind=m.group("kind"),
                    )
                )
    return out
