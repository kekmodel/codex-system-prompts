"""Pass 1.7: ToolSpec auto-discovery (M9, SPEC §1.1 (a)–(d) / §2.2).

Walks `codex-rs/tools/src/*.rs` for inline
``ResponsesApiTool { name: "...", description: ..., parameters: ... }`` blocks
and emits one captured prompt per tool description.

Description value shapes handled in this first cut:

- ``"...".to_string()`` (plain string literal, escape-decoded).
- ``r#"..."#.to_string()`` (raw string literal, byte-for-byte).
- bare identifier ``description,`` — resolves the matching ``let description = …``
  binding in the enclosing function (covers the `cfg!(windows) { … } else { … }`
  pattern in `local_tool.rs`).
- direct call ``some_helper_fn()`` or ``some_helper_fn(args).to_string()``
  — same-file helper bodies are resolved by picking the longest string-bearing
  expression in the body (covers the multi-branch ``spawn_agent_tool_description``
  helpers and the simpler ``request_*_tool_description`` ones). Placeholders
  ``{name}`` referencing same-fn ``let`` bindings or file-level ``const`` are
  substituted in a single pass; unresolved placeholders stay verbatim.

JsonSchema parameter descriptions are intentionally NOT extracted here yet —
that's a separate sub-pass tracked under M9.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_RESPONSES_API_OPEN_RX = re.compile(r"\bResponsesApiTool\s*\{", re.MULTILINE)
_NAME_LITERAL_RX = re.compile(
    r'^"([^"\\]*(?:\\.[^"\\]*)*)"\s*\.to_string\s*\(\s*\)\s*$',
    re.DOTALL,
)
_NAME_CONST_REF_RX = re.compile(r'^(\w+)\s*\.to_string\s*\(\s*\)\s*$')

# Property entries inside `BTreeMap::from([...])` for ToolSpec.parameters:
#     ("name".to_string(), JsonSchema::<type>(Some("desc".to_string())))
# or with a raw-string description, or a const-ref name. Multi-line bodies
# happen often, so we scan with re.DOTALL.
_PROPERTY_RX = re.compile(
    r'\(\s*'
    # name: either "literal".to_string() or IDENT.to_string()
    r'(?:"([^"\\]*(?:\\.[^"\\]*)*)"|(\w+))\s*\.to_string\s*\(\s*\)\s*,\s*'
    # JsonSchema::<type>(Some(<desc>.to_string()))
    # Trailing commas inside Some(...) and after JsonSchema::TYPE(...)
    # are common when the body is split across multiple lines.
    r'JsonSchema::(\w+)\s*\(\s*Some\s*\(\s*'
    r'(?:"((?:[^"\\]|\\.)*)"|r(#*)"(.*?)"\5)\s*'
    r'\.to_string\s*\(\s*\)\s*,?\s*'
    r'\)',
    re.DOTALL,
)


def _resolve_string_const(text: str, name: str) -> str | None:
    """Find ``(pub )?const NAME: &str = "...";`` in `text`. Returns the
    string body, or None if no plain-string constant is found.
    """
    const_rx = re.compile(
        rf'\b(?:pub(?:\([^)]*\))?\s+)?const\s+{re.escape(name)}\s*:\s*&\s*str\s*=\s*("([^"\\]*(?:\\.[^"\\]*)*)"|r(#*)"(.*?)"\3)\s*;',
        re.DOTALL,
    )
    m = const_rx.search(text)
    if not m:
        return None
    if m.group(2) is not None:
        body = m.group(2)
        return body.encode("utf-8", "replace").decode("unicode_escape", "replace")
    return m.group(4)


# When a tool name is `SOMETHING_TOOL_NAME` referenced from `tools/src/`,
# the const may be defined in `tools/src/<file>.rs` itself (same-file) or
# re-exported from `protocol/src/models.rs`. Search those in order.
def _resolve_const_with_fallback(
    primary_text: str, name: str, codex_rs_root: Path
) -> str | None:
    body = _resolve_string_const(primary_text, name)
    if body is not None:
        return body
    fallbacks = [
        codex_rs_root / "protocol" / "src" / "models.rs",
        codex_rs_root / "tools" / "src" / "tool_spec.rs",
    ]
    for path in fallbacks:
        if not path.is_file():
            continue
        body = _resolve_string_const(path.read_text(encoding="utf-8"), name)
        if body is not None:
            return body
    return None


@dataclass
class ParameterCapture:
    name: str            # property name (e.g. "dir_path")
    schema_type: str     # "string" | "number" | "boolean" | "integer" | "array" | "object"
    description: str     # JsonSchema property description (post escape-decode)


@dataclass
class ToolSpecCapture:
    file_rel: Path           # path relative to codex-rs/
    line: int
    tool_name: str
    description: str         # raw description text the model receives (no framing)
    description_kind: str    # "static_plain" | "static_raw" | "const_ref" | "let_binding" | "cfg_conditional" | "fn_resolved" | "fn_call" | "unresolved"
    let_binding_kind: str | None = None  # populated when sub-kind="let_*"
    fn_callee: str | None = None         # populated when description came from a fn

    # Set only when the description splits across `cfg!(windows)` branches.
    # When set, `description` is empty; the emit step writes two separate
    # files (one for each platform).
    windows_description: str | None = None
    unix_description: str | None = None

    parameters: list[ParameterCapture] = field(default_factory=list)


def _scan_balanced(text: str, start: int) -> int:
    """Find the matching `}` for the `{` at position start-1.

    `start` points to the character immediately after the opening `{`.
    Respects string literals (plain + raw), char literals, and comments.
    Returns -1 if unbalanced.
    """
    depth = 1
    pos = start
    n = len(text)
    while pos < n:
        c = text[pos]

        # Raw string `r#"..."#` (or any number of `#`) or `r"..."`.
        if c == "r" and pos + 1 < n:
            m = re.match(r'r(#*)"', text[pos:])
            if m:
                hashes = m.group(1)
                end_pat = '"' + hashes
                end = text.find(end_pat, pos + len(m.group(0)))
                if end == -1:
                    return -1
                pos = end + len(end_pat)
                continue

        # Char literal — skip simple `'a'` / `'\n'`.
        if c == "'" and pos + 1 < n:
            j = pos + 2 if text[pos + 1] != "\\" else pos + 3
            if j < n and text[j] == "'":
                pos = j + 1
                continue

        # Plain string.
        if c == '"':
            pos += 1
            while pos < n:
                if text[pos] == "\\":
                    pos += 2
                    continue
                if text[pos] == '"':
                    pos += 1
                    break
                pos += 1
            continue

        # Line / block comments.
        if c == "/" and pos + 1 < n:
            if text[pos + 1] == "/":
                nl = text.find("\n", pos)
                pos = nl + 1 if nl != -1 else n
                continue
            if text[pos + 1] == "*":
                end = text.find("*/", pos + 2)
                pos = end + 2 if end != -1 else n
                continue

        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return pos
        pos += 1
    return -1


def _find_field(block: str, field_name: str) -> tuple[int, int] | None:
    """Return (value_start, value_end) for ``field_name: <value>,`` at the top
    level of `block`. The ending comma is excluded; a missing trailing comma
    (last field of the struct) is also accepted.
    """
    pat = re.compile(rf"^\s*{re.escape(field_name)}\s*:\s*", re.MULTILINE)
    m = pat.search(block)
    if not m:
        return None
    start = m.end()
    pos = start
    depth = 0
    n = len(block)
    while pos < n:
        c = block[pos]

        if c == "r" and pos + 1 < n:
            rm = re.match(r'r(#*)"', block[pos:])
            if rm:
                hashes = rm.group(1)
                end_pat = '"' + hashes
                end = block.find(end_pat, pos + len(rm.group(0)))
                if end == -1:
                    return None
                pos = end + len(end_pat)
                continue

        if c == "'" and pos + 1 < n:
            j = pos + 2 if block[pos + 1] != "\\" else pos + 3
            if j < n and block[j] == "'":
                pos = j + 1
                continue

        if c == '"':
            pos += 1
            while pos < n:
                if block[pos] == "\\":
                    pos += 2
                    continue
                if block[pos] == '"':
                    pos += 1
                    break
                pos += 1
            continue

        if c == "/" and pos + 1 < n:
            if block[pos + 1] == "/":
                nl = block.find("\n", pos)
                pos = nl + 1 if nl != -1 else n
                continue
            if block[pos + 1] == "*":
                end = block.find("*/", pos + 2)
                pos = end + 2 if end != -1 else n
                continue

        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
            if depth < 0:
                return (start, pos)
        elif c == "," and depth == 0:
            return (start, pos)

        pos += 1
    return (start, n) if start < n else None


_LET_BINDING_RX_TPL = (
    r"\blet\s+{name}\s*(?::\s*[^=]+)?=\s*"  # `let description: T = `
)


def _resolve_let_binding(
    fn_text: str, var_name: str
) -> tuple[str, str, str | None, str | None, str | None]:
    """Find ``let <var_name> = <expr>;`` in fn_text and classify <expr>.

    Returns (kind, body, sub_label, windows_body, unix_body):

    - For `if cfg!(windows) { … } else { … }`, kind="cfg_conditional",
      body="" (caller checks windows_body / unix_body), windows_body and
      unix_body hold the raw resolved literal for each platform.
    - For a literal value, kind="let_literal", body=<resolved>.
    - For a direct fn call, kind="let_fn_call", sub_label=<callee>.
    - Otherwise kind="let_unresolved", body=<diagnostic placeholder>.
    """
    pat = re.compile(_LET_BINDING_RX_TPL.format(name=re.escape(var_name)))
    m = pat.search(fn_text)
    if not m:
        return (
            "let_unresolved",
            f"(no `let {var_name} = ...` found in enclosing fn)",
            None,
            None,
            None,
        )

    expr_start = m.end()
    # Scan to the terminating `;` at depth 0, respecting strings + braces.
    depth = 0
    pos = expr_start
    n = len(fn_text)
    semicolon = -1
    while pos < n:
        c = fn_text[pos]
        if c == "r" and pos + 1 < n:
            rm = re.match(r'r(#*)"', fn_text[pos:])
            if rm:
                hashes = rm.group(1)
                end_pat = '"' + hashes
                end = fn_text.find(end_pat, pos + len(rm.group(0)))
                if end == -1:
                    return ("let_unresolved", "(unbalanced raw string in let-binding)", None)
                pos = end + len(end_pat)
                continue
        if c == '"':
            pos += 1
            while pos < n:
                if fn_text[pos] == "\\":
                    pos += 2
                    continue
                if fn_text[pos] == '"':
                    pos += 1
                    break
                pos += 1
            continue
        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
        elif c == ";" and depth == 0:
            semicolon = pos
            break
        pos += 1

    if semicolon == -1:
        return (
            "let_unresolved",
            "(could not find terminating semicolon for let-binding)",
            None,
            None,
            None,
        )

    expr = fn_text[expr_start:semicolon].strip()

    # Match `if cfg!(windows) { ... } else { ... }`.
    cfg_m = re.match(
        r"^if\s+cfg!\s*\(\s*windows\s*\)\s*\{(?P<win>.*)\}\s*else\s*\{(?P<unix>.*)\}\s*$",
        expr,
        re.DOTALL,
    )
    if cfg_m:
        win = cfg_m.group("win").strip()
        unix = cfg_m.group("unix").strip()
        win_body = _classify_inline_string(win)
        unix_body = _classify_inline_string(unix)
        return ("cfg_conditional", "", None, win_body, unix_body)

    # Direct call: `let description = something();`
    direct_m = re.match(r"^(\w+)\s*\(", expr)
    if direct_m:
        return (
            "let_fn_call",
            "",
            direct_m.group(1),
            None,
            None,
        )

    # Plain literal — pass through.
    inline_body = _classify_inline_string(expr)
    if inline_body is not None:
        return ("let_literal", inline_body, None, None, None)

    # Fallback: leave a diagnostic placeholder so a reviewer can see the
    # raw expression.
    return (
        "let_unresolved",
        f"(non-literal let expression: {expr[:80]}…)",
        None,
        None,
        None,
    )


def _classify_inline_string(value: str) -> str | None:
    """If `value` is a plain or raw string literal (with optional trailing
    `.to_string()`/`format!(...)` simple wrapper), return the body text;
    otherwise return None.
    """
    v = value.strip()
    raw_m = re.match(r'^r(#*)"(.*?)"\1\s*(?:\.to_string\s*\(\s*\))?\s*$', v, re.DOTALL)
    if raw_m:
        return raw_m.group(2)
    plain_m = re.match(r'^"((?:[^"\\]|\\.)*)"\s*(?:\.to_string\s*\(\s*\))?\s*$', v, re.DOTALL)
    if plain_m:
        body = plain_m.group(1)
        return body.encode("utf-8", "replace").decode("unicode_escape", "replace")
    # `format!(r#"..."#, args...)` — return the raw template; placeholders
    # like `{name}` are preserved verbatim. The arg list is metadata for the
    # mirror, not for the model, so we drop it from the body.
    fmt_m = re.match(r"^format!\s*\(\s*r(#*)\"(.*?)\"\1\s*(?:,.*)?\)\s*$", v, re.DOTALL)
    if fmt_m:
        return fmt_m.group(2)
    fmt_plain = re.match(r"^format!\s*\(\s*\"((?:[^\"\\]|\\.)*)\"\s*(?:,.*)?\)\s*$", v, re.DOTALL)
    if fmt_plain:
        return fmt_plain.group(1).encode("utf-8", "replace").decode("unicode_escape", "replace")
    return None


_HELPER_FN_OPEN_TPL = (
    r"\b(?:pub\s+)?fn\s+{name}\s*\([^)]*\)\s*->\s*String\s*\{{"
)
_PLACEHOLDER_RX = re.compile(r"\{(\w+)\}")


def _scan_to_semicolon(text: str, start: int) -> int:
    """Return the index of the `;` ending an expression that begins at `start`.

    Respects strings, raw strings, char literals, comments, and bracket depth.
    Returns -1 if no terminating `;` is found.
    """
    depth = 0
    pos = start
    n = len(text)
    while pos < n:
        c = text[pos]
        if c == "r" and pos + 1 < n:
            rm = re.match(r'r(#*)"', text[pos:])
            if rm:
                hashes = rm.group(1)
                end_pat = '"' + hashes
                end = text.find(end_pat, pos + len(rm.group(0)))
                if end == -1:
                    return -1
                pos = end + len(end_pat)
                continue
        if c == "'" and pos + 1 < n:
            j = pos + 2 if text[pos + 1] != "\\" else pos + 3
            if j < n and text[j] == "'":
                pos = j + 1
                continue
        if c == '"':
            pos += 1
            while pos < n:
                if text[pos] == "\\":
                    pos += 2
                    continue
                if text[pos] == '"':
                    pos += 1
                    break
                pos += 1
            continue
        if c == "/" and pos + 1 < n:
            if text[pos + 1] == "/":
                nl = text.find("\n", pos)
                pos = nl + 1 if nl != -1 else n
                continue
            if text[pos + 1] == "*":
                end = text.find("*/", pos + 2)
                pos = end + 2 if end != -1 else n
                continue
        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
        elif c == ";" and depth == 0:
            return pos
        pos += 1
    return -1


def _collect_let_strings(body_text: str) -> dict[str, str]:
    """Collect ``let <var> = <string-expr>;`` mappings from a fn body.

    Only inline string-bearing expressions (plain literal, raw literal,
    ``format!`` template) are recorded. Other shapes (function calls,
    conditionals, .map() chains) are skipped — the placeholder will stay
    verbatim in the substituted result.
    """
    out: dict[str, str] = {}
    let_rx = re.compile(r"\blet\s+(\w+)\s*(?::\s*[^=]+)?=\s*", re.MULTILINE)
    for lm in let_rx.finditer(body_text):
        var = lm.group(1)
        if var in out:
            continue
        expr_start = lm.end()
        semi = _scan_to_semicolon(body_text, expr_start)
        if semi == -1:
            continue
        expr = body_text[expr_start:semi].strip()
        s = _classify_inline_string(expr)
        if s is not None:
            out[var] = s
    return out


def _string_literal_spans(text: str) -> list[tuple[int, int, str]]:
    """Return (start, end_exclusive, body) for every raw or plain string
    literal in `text`. Body is the inner content; for plain strings the
    escapes are NOT decoded here (callers decide).
    """
    spans: list[tuple[int, int, str]] = []
    pos = 0
    n = len(text)
    while pos < n:
        c = text[pos]
        if c == "r" and pos + 1 < n:
            rm = re.match(r'r(#*)"', text[pos:])
            if rm:
                hashes = rm.group(1)
                end_pat = '"' + hashes
                start_inner = pos + len(rm.group(0))
                end = text.find(end_pat, start_inner)
                if end == -1:
                    return spans
                spans.append((pos, end + len(end_pat), text[start_inner:end]))
                pos = end + len(end_pat)
                continue
        if c == "'" and pos + 1 < n:
            j = pos + 2 if text[pos + 1] != "\\" else pos + 3
            if j < n and text[j] == "'":
                pos = j + 1
                continue
        if c == '"':
            start_inner = pos + 1
            scan = start_inner
            while scan < n:
                if text[scan] == "\\":
                    scan += 2
                    continue
                if text[scan] == '"':
                    break
                scan += 1
            if scan >= n:
                return spans
            raw = text[start_inner:scan]
            try:
                decoded = raw.encode("utf-8", "replace").decode("unicode_escape", "replace")
            except UnicodeDecodeError:
                decoded = raw
            spans.append((pos, scan + 1, decoded))
            pos = scan + 1
            continue
        if c == "/" and pos + 1 < n:
            if text[pos + 1] == "/":
                nl = text.find("\n", pos)
                pos = nl + 1 if nl != -1 else n
                continue
            if text[pos + 1] == "*":
                end = text.find("*/", pos + 2)
                pos = end + 2 if end != -1 else n
                continue
        pos += 1
    return spans


def _resolve_helper_fn_description(
    file_text: str, fn_name: str, codex_rs_root: Path
) -> str | None:
    """Resolve a helper fn ``-> String`` body to its dominant description text.

    Strategy: pick the longest string literal in the fn body. Substitute
    ``{var}`` placeholders that match a same-fn ``let var = ...;`` literal
    binding or a file-level ``const VAR: &str = "...";``. Anything else
    stays verbatim — the model still sees an explicit placeholder rather
    than silent omission.
    """
    fn_open_rx = re.compile(_HELPER_FN_OPEN_TPL.format(name=re.escape(fn_name)))
    m = fn_open_rx.search(file_text)
    if not m:
        return None
    body_open = m.end() - 1
    body_close = _scan_balanced(file_text, body_open + 1)
    if body_close == -1:
        return None
    body_text = file_text[body_open + 1:body_close]

    spans = _string_literal_spans(body_text)
    if not spans:
        return None
    longest = max(spans, key=lambda s: len(s[2]))
    body = longest[2]

    let_map = _collect_let_strings(body_text)

    def substitute(s: str) -> str:
        def repl(match: re.Match) -> str:
            name = match.group(1)
            if name in let_map:
                return let_map[name]
            const_body = _resolve_string_const(file_text, name)
            if const_body is not None:
                return const_body
            return match.group(0)

        return _PLACEHOLDER_RX.sub(repl, s)

    prev = body
    for _ in range(4):
        nxt = substitute(prev)
        if nxt == prev:
            break
        prev = nxt
    return prev


def _enclosing_fn(text: str, struct_pos: int) -> tuple[str, str] | None:
    """Return (fn_name, fn_text) for the function containing struct_pos.

    Heuristic: walk backwards to the most recent `pub fn NAME` / `fn NAME`
    opener, then forward through balanced braces.
    """
    fn_open_rx = re.compile(r"\b(?:pub\s+)?fn\s+(\w+)\s*[<(]", re.MULTILINE)
    candidates = list(fn_open_rx.finditer(text, 0, struct_pos))
    if not candidates:
        return None
    fn_match = candidates[-1]
    body_open = text.find("{", fn_match.end())
    if body_open == -1:
        return None
    body_close = _scan_balanced(text, body_open + 1)
    if body_close == -1:
        return None
    return fn_match.group(1), text[fn_match.start():body_close + 1]


def _enclosing_fn_text(text: str, struct_pos: int) -> str:
    """Backwards-compat shim — returns fn body text only."""
    res = _enclosing_fn(text, struct_pos)
    return res[1] if res else text


def _find_sibling_description_helper(
    file_text: str, enclosing_fn_name: str
) -> str | None:
    """Look for a same-file ``fn <X>_tool_description(...) -> String`` whose
    name shares a token with `enclosing_fn_name` (e.g.
    ``create_request_permissions_tool`` matches ``request_permissions_tool_description``).
    Returns the helper fn name, or None.
    """
    helper_rx = re.compile(
        r"\b(?:pub\s+)?fn\s+(\w+_tool_description)\s*\([^)]*\)\s*->\s*String\s*\{",
        re.MULTILINE | re.DOTALL,
    )
    candidates = [m.group(1) for m in helper_rx.finditer(file_text)]
    if not candidates:
        return None
    enc_tokens = set(enclosing_fn_name.split("_"))
    best: tuple[int, str] | None = None
    for cand in candidates:
        cand_tokens = set(cand.split("_"))
        score = len(enc_tokens & cand_tokens)
        if score == 0:
            continue
        if best is None or score > best[0]:
            best = (score, cand)
    return best[1] if best else None


def _extract_parameters(
    fn_text: str, source_text: str, codex_rs_root: Path
) -> list[ParameterCapture]:
    """Pull JsonSchema property descriptions out of `fn_text`.

    Matches the literal pattern
    ``("name".to_string(), JsonSchema::<type>(Some("desc".to_string())))``
    (or with raw-string description, or with a const-ref name resolved via
    same-file/protocol/tool_spec fallback). Order is source order.

    Nested JsonSchema::object/array property bags inside a property — common
    when a parameter is itself a structured object — are deliberately not
    descended into in this first cut; only top-level scalar/array property
    entries with a directly-captured description string surface here.
    """
    captures: list[ParameterCapture] = []
    for m in _PROPERTY_RX.finditer(fn_text):
        name_literal, name_const, schema_type = m.group(1), m.group(2), m.group(3)
        desc_plain = m.group(4)
        desc_raw = m.group(6)

        if name_literal is not None:
            name = name_literal.encode("utf-8", "replace").decode("unicode_escape", "replace")
        elif name_const is not None:
            resolved = _resolve_const_with_fallback(source_text, name_const, codex_rs_root)
            if resolved is None:
                # Skip — the parameter name won't be meaningful without it.
                continue
            name = resolved
        else:
            continue

        if desc_raw is not None:
            description = desc_raw
        elif desc_plain is not None:
            description = desc_plain.encode("utf-8", "replace").decode("unicode_escape", "replace")
        else:
            continue

        captures.append(
            ParameterCapture(
                name=name,
                schema_type=schema_type,
                description=description,
            )
        )
    return captures


def walk(codex_rs_root: Path) -> list[ToolSpecCapture]:
    """Discover every inline ToolSpec (ResponsesApiTool) in tools/src/*.rs."""
    captures: list[ToolSpecCapture] = []
    target = codex_rs_root / "tools" / "src"
    if not target.is_dir():
        return captures

    for rs in sorted(target.glob("*.rs")):
        if rs.name.endswith("_tests.rs"):
            continue
        # tool_spec.rs is the type definition; responses_api.rs builds
        # ResponsesApiTool from runtime ToolDefinition.
        if rs.name in ("tool_spec.rs", "responses_api.rs"):
            continue
        text = rs.read_text(encoding="utf-8")

        for m in _RESPONSES_API_OPEN_RX.finditer(text):
            block_open = m.end() - 1
            block_close = _scan_balanced(text, block_open + 1)
            if block_close == -1:
                continue
            block = text[block_open + 1:block_close]
            line = text[: m.start()].count("\n") + 1

            # name field
            name_span = _find_field(block, "name")
            if not name_span:
                continue
            name_text = block[name_span[0]:name_span[1]].strip()
            tool_name: str | None = None
            literal_m = _NAME_LITERAL_RX.match(name_text)
            if literal_m:
                tool_name = literal_m.group(1)
            else:
                const_ref_m = _NAME_CONST_REF_RX.match(name_text)
                if const_ref_m:
                    tool_name = _resolve_const_with_fallback(
                        text, const_ref_m.group(1), codex_rs_root
                    )
            if not tool_name:
                continue

            # description field — could be `description: <value>,` or
            # the shorthand `description,` (Rust struct shorthand: field name
            # matches an in-scope variable of the same name).
            desc_span = _find_field(block, "description")
            shorthand_rx = re.compile(r"^\s*description\s*(?:,|\})", re.MULTILINE)
            is_shorthand = desc_span is None and bool(shorthand_rx.search(block))
            if desc_span is None and not is_shorthand:
                continue

            kind = "unresolved"
            body = ""
            let_kind: str | None = None
            fn_callee: str | None = None
            windows_body: str | None = None
            unix_body: str | None = None

            if is_shorthand:
                # Resolve the `description` variable in the enclosing fn.
                enc = _enclosing_fn(text, m.start())
                fn_text = enc[1] if enc else text
                enc_name = enc[0] if enc else ""
                sub_kind, sub_body, sub_label, sub_win, sub_unix = _resolve_let_binding(
                    fn_text, "description"
                )
                kind = "let_binding"
                let_kind = sub_kind
                if sub_kind == "cfg_conditional":
                    windows_body = sub_win
                    unix_body = sub_unix
                elif sub_kind == "let_fn_call" and sub_label:
                    fn_callee = sub_label
                    resolved = _resolve_helper_fn_description(
                        text, sub_label, codex_rs_root
                    )
                    if resolved is not None:
                        kind = "fn_resolved"
                        body = resolved
                elif sub_kind == "let_unresolved":
                    helper = _find_sibling_description_helper(text, enc_name)
                    if helper:
                        resolved = _resolve_helper_fn_description(
                            text, helper, codex_rs_root
                        )
                        if resolved is not None:
                            kind = "fn_resolved"
                            fn_callee = helper
                            body = resolved
                else:
                    body = sub_body
                if sub_label and fn_callee is None:
                    fn_callee = sub_label
            else:
                desc_text = block[desc_span[0]:desc_span[1]].strip()
                inline = _classify_inline_string(desc_text)
                inline_cfg_m = re.match(
                    r"^if\s+cfg!\s*\(\s*windows\s*\)\s*\{(?P<win>.*)\}\s*else\s*\{(?P<unix>.*)\}\s*$",
                    desc_text,
                    re.DOTALL,
                )
                const_call_m = re.match(
                    r"^(\w+)\s*\.to_string\s*\(\s*\)\s*$", desc_text
                )
                ident_m = re.match(r"^(\w+)$", desc_text)
                fn_call_m = re.match(r"^(\w+)\s*\(", desc_text)

                if inline is not None:
                    kind = "static_raw" if desc_text.lstrip().startswith("r") else "static_plain"
                    body = inline
                elif inline_cfg_m:
                    win = inline_cfg_m.group("win").strip()
                    unix = inline_cfg_m.group("unix").strip()
                    windows_body = _classify_inline_string(win)
                    unix_body = _classify_inline_string(unix)
                    kind = "cfg_conditional"
                elif const_call_m:
                    resolved = _resolve_const_with_fallback(
                        text, const_call_m.group(1), codex_rs_root
                    )
                    if resolved is not None:
                        kind = "const_ref"
                        body = resolved
                        fn_callee = const_call_m.group(1)
                    else:
                        kind = "unresolved"
                        fn_callee = const_call_m.group(1)
                elif ident_m:
                    enc = _enclosing_fn(text, m.start())
                    fn_text = enc[1] if enc else text
                    enc_name = enc[0] if enc else ""
                    sub_kind, sub_body, sub_label, sub_win, sub_unix = _resolve_let_binding(
                        fn_text, ident_m.group(1)
                    )
                    kind = "let_binding"
                    let_kind = sub_kind
                    if sub_kind == "cfg_conditional":
                        windows_body = sub_win
                        unix_body = sub_unix
                    elif sub_kind == "let_fn_call" and sub_label:
                        fn_callee = sub_label
                        resolved = _resolve_helper_fn_description(
                            text, sub_label, codex_rs_root
                        )
                        if resolved is not None:
                            kind = "fn_resolved"
                            body = resolved
                    elif sub_kind == "let_unresolved":
                        helper = _find_sibling_description_helper(text, enc_name)
                        if helper:
                            resolved = _resolve_helper_fn_description(
                                text, helper, codex_rs_root
                            )
                            if resolved is not None:
                                kind = "fn_resolved"
                                fn_callee = helper
                                body = resolved
                    else:
                        body = sub_body
                    if sub_label and fn_callee is None:
                        fn_callee = sub_label
                elif fn_call_m:
                    fn_callee = fn_call_m.group(1)
                    resolved = _resolve_helper_fn_description(
                        text, fn_callee, codex_rs_root
                    )
                    if resolved is not None:
                        kind = "fn_resolved"
                        body = resolved
                    else:
                        kind = "fn_call"

            # Pull JsonSchema parameter descriptions from the enclosing fn.
            # Use _enclosing_fn_text rather than the ToolSpec block itself
            # because most properties are defined in a `let properties = …`
            # binding immediately above the ToolSpec literal.
            fn_text_for_params = _enclosing_fn_text(text, m.start())
            params = _extract_parameters(fn_text_for_params, text, codex_rs_root)

            captures.append(
                ToolSpecCapture(
                    file_rel=rs.relative_to(codex_rs_root),
                    line=line,
                    tool_name=tool_name,
                    description=body,
                    description_kind=kind,
                    let_binding_kind=let_kind,
                    fn_callee=fn_callee,
                    windows_description=windows_body,
                    unix_description=unix_body,
                    parameters=params,
                )
            )
    return captures
