"""Pass 1.6: ContextualUserFragment auto-discovery (SPEC v0.6 §2.3 M5b).

Walks codex-rs/core/src/context/ for `impl ContextualUserFragment for <Struct>`
blocks and extracts the four pieces of information that fully characterize each
fragment from a static-analysis perspective:

  - struct name (from `impl ContextualUserFragment for <Name>`)
  - ROLE / START_MARKER / END_MARKER consts
  - body() function source

For body() rendering we try to extract a clean template string when body() is
a simple `format!(...)` or `"...".to_string()`; otherwise we fall back to
embedding the function source as a Rust code block so the reader gets full
fidelity.

This is mechanical (no curation needed). When codex adds a new fragment, it's
captured automatically on the next extraction cycle.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Find `impl ContextualUserFragment for <Struct> {` (multi-line tolerant).
_IMPL_RX = re.compile(r"impl\s+ContextualUserFragment\s+for\s+(\w+)\s*\{", re.MULTILINE)

# String literal extractors for ROLE/START_MARKER/END_MARKER.
_PLAIN_STR_RX = r'"((?:[^"\\]|\\.)*)"'

# Common body() patterns:
_BODY_FORMAT_RAW_RX = re.compile(r'format!\s*\(\s*r#"(?P<body>.*?)"#', re.DOTALL)
_BODY_FORMAT_PLAIN_RX = re.compile(r'format!\s*\(\s*"(?P<body>(?:[^"\\]|\\.)*)"', re.DOTALL)
_BODY_TO_STRING_PLAIN_RX = re.compile(r'^"(?P<body>(?:[^"\\]|\\.)*)"\s*\.to_string\(\)', re.DOTALL)
_BODY_TO_STRING_RAW_RX = re.compile(r'^r#"(?P<body>.*?)"#\s*\.to_string\(\)', re.DOTALL)


@dataclass(frozen=True)
class FragmentCapture:
    struct_name: str
    role: str
    start_marker: str
    end_marker: str
    body_source: str          # raw source of body() function body (without outer braces)
    body_template: str | None # cleaned template literal if body() is a simple format!
    source_rel: Path
    source_line: int          # 1-indexed line of `impl ContextualUserFragment for <Struct>`


def _decode_str_escapes(s: str) -> str:
    """Decode common Rust string escapes (\\n, \\t, \\\", \\\\)."""
    return s.encode("utf-8", "replace").decode("unicode_escape", "replace")


def _extract_const_str(block: str, name: str) -> str:
    """Extract `const NAME: &'static str = \"value\";` from an impl block. Returns '' if absent."""
    pattern = rf"const\s+{re.escape(name)}\s*:\s*&\s*'static\s+str\s*=\s*{_PLAIN_STR_RX}"
    m = re.search(pattern, block)
    return _decode_str_escapes(m.group(1)) if m else ""


def _find_body_fn(block: str) -> str | None:
    """Return the source of the body() function body, without surrounding `{}`."""
    m = re.search(r"fn\s+body\s*\(\s*&self\s*\)\s*->\s*String\s*\{", block)
    if not m:
        return None
    start = m.end()
    depth = 1
    pos = start
    while pos < len(block) and depth > 0:
        c = block[pos]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        pos += 1
    return block[start:pos].strip()


def _try_extract_template(body_source: str) -> str | None:
    """If body_source is a simple format!/string-literal pattern, extract the template."""
    body = body_source.strip()
    # Strip trailing semicolon
    if body.endswith(";"):
        body = body[:-1].strip()

    # format!(r#"..."#, ...)
    m = _BODY_FORMAT_RAW_RX.match(body)
    if m:
        return m.group("body")
    # format!("...", ...)
    m = _BODY_FORMAT_PLAIN_RX.match(body)
    if m:
        return _decode_str_escapes(m.group("body"))
    # "...".to_string()
    m = _BODY_TO_STRING_PLAIN_RX.match(body)
    if m:
        return _decode_str_escapes(m.group("body"))
    # r#"..."#.to_string()
    m = _BODY_TO_STRING_RAW_RX.match(body)
    if m:
        return m.group("body")
    return None


def _find_impl_block(text: str, struct_name_match: re.Match) -> tuple[str, int]:
    """Given a regex match for `impl ContextualUserFragment for X {`, return (block_body, line_no)."""
    body_start = struct_name_match.end()
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
    block_body = text[body_start:pos]
    line_no = text[: struct_name_match.start()].count("\n") + 1
    return block_body, line_no


def walk(codex_rs: Path) -> list[FragmentCapture]:
    """Walk codex-rs/core/src/context/ for `impl ContextualUserFragment for ...` blocks."""
    captures: list[FragmentCapture] = []
    ctx_dir = codex_rs / "core" / "src" / "context"
    if not ctx_dir.is_dir():
        return captures
    for rs in sorted(ctx_dir.rglob("*.rs")):
        # Skip test files (Pass 2 denylist would catch later, but elide here for clarity).
        rel = rs.relative_to(codex_rs)
        if rel.name in {"tests.rs", "test.rs"} or any(
            p in {"tests", "benches", "examples"} for p in rel.parts
        ):
            continue
        if rel.name.endswith(("_tests.rs", "_test.rs")):
            continue
        try:
            text = rs.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for m in _IMPL_RX.finditer(text):
            struct_name = m.group(1)
            block, line_no = _find_impl_block(text, m)
            role = _extract_const_str(block, "ROLE")
            start_marker = _extract_const_str(block, "START_MARKER")
            end_marker = _extract_const_str(block, "END_MARKER")
            body_source = _find_body_fn(block) or ""
            body_template = _try_extract_template(body_source) if body_source else None
            captures.append(
                FragmentCapture(
                    struct_name=struct_name,
                    role=role,
                    start_marker=start_marker,
                    end_marker=end_marker,
                    body_source=body_source,
                    body_template=body_template,
                    source_rel=rel,
                    source_line=line_no,
                )
            )
    return captures
