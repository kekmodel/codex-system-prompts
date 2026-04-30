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
  — captured as a "dynamic" body referencing the helper. Resolving the helper
  body to its template + arg list is a follow-up (covered separately in
  pass1_5_allowlist for explicit helpers we care about).

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
    description: str
    description_kind: str    # "static_plain" | "static_raw" | "let_binding" | "fn_call" | "unknown"
    let_binding_kind: str | None = None  # populated when description_kind="let_binding"
    fn_callee: str | None = None         # populated when description_kind="fn_call"
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
) -> tuple[str, str, str | None]:
    """Find ``let <var_name> = <expr>;`` in fn_text and classify <expr>.

    Returns (kind, body, sub_label). Currently handles two shapes:

    - ``let description = if cfg!(windows) { format!(r#"..."#, …) } else { r#"..."#.to_string() };``
      Returns kind="cfg_conditional", body="<windows>\n\n---\n\n<unix>".
    - Anything else: kind="let_unresolved", body="(see source — let-binding not statically resolvable)".
    """
    pat = re.compile(_LET_BINDING_RX_TPL.format(name=re.escape(var_name)))
    m = pat.search(fn_text)
    if not m:
        return ("let_unresolved", f"(no `let {var_name} = ...` found in enclosing fn)", None)

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
        return ("let_unresolved", "(could not find terminating semicolon for let-binding)", None)

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
        win_body = _classify_inline_string(win) or f"(non-literal Windows branch)\n\n```\n{win}\n```"
        unix_body = _classify_inline_string(unix) or f"(non-literal Unix branch)\n\n```\n{unix}\n```"
        body = (
            "## Windows branch (`cfg!(windows)` true)\n\n"
            f"{win_body}\n\n"
            "## Unix branch (`cfg!(windows)` false)\n\n"
            f"{unix_body}\n"
        )
        return ("cfg_conditional", body, None)

    # Direct call: `let description = something();`
    direct_m = re.match(r"^(\w+)\s*\(", expr)
    if direct_m:
        return ("let_fn_call", f"(see source — let binds the result of `{direct_m.group(1)}(…)`)", direct_m.group(1))

    # Plain literal — pass through.
    inline_body = _classify_inline_string(expr)
    if inline_body is not None:
        return ("let_literal", inline_body, None)

    # Fallback: emit the raw expression as a code block so the body is
    # inspectable.
    return ("let_unresolved", f"(non-literal let expression)\n\n```\n{expr}\n```", None)


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
    # `format!(r#"..."#, args...)` — capture the template body and append the
    # arg list as a footer so the placeholders are visible.
    fmt_m = re.match(r"^format!\s*\(\s*r(#*)\"(.*?)\"\1\s*(?:,(?P<args>.*))?\)\s*$", v, re.DOTALL)
    if fmt_m:
        template = fmt_m.group(2)
        args = (fmt_m.group("args") or "").strip()
        if args:
            return f"{template}\n\n_format!() args: `{args}`_"
        return template
    fmt_plain = re.match(r"^format!\s*\(\s*\"((?:[^\"\\]|\\.)*)\"\s*(?:,(?P<args>.*))?\)\s*$", v, re.DOTALL)
    if fmt_plain:
        template = fmt_plain.group(1).encode("utf-8", "replace").decode("unicode_escape", "replace")
        args = (fmt_plain.group("args") or "").strip()
        if args:
            return f"{template}\n\n_format!() args: `{args}`_"
        return template
    return None


def _resolve_fn_body_text(text: str, fn_name: str) -> str | None:
    """Locate ``(pub )?fn <fn_name>(...)`` in `text` and return its body
    (between the outermost `{` and matching `}`), or None if not found.
    """
    fn_open_rx = re.compile(
        rf"\b(?:pub\s+)?fn\s+{re.escape(fn_name)}\s*[<(]", re.MULTILINE
    )
    m = fn_open_rx.search(text)
    if not m:
        return None
    body_open = text.find("{", m.end())
    if body_open == -1:
        return None
    body_close = _scan_balanced(text, body_open + 1)
    if body_close == -1:
        return None
    return text[body_open + 1:body_close]


_STRING_LITERAL_RX = re.compile(
    r'(?P<raw>r(?P<hashes>#*)"(?P<rawbody>.*?)"(?P=hashes))'
    r"|"
    r'(?P<plain>"(?P<plainbody>(?:[^"\\]|\\.)*)")',
    re.DOTALL,
)


def _harvest_string_literals(body: str) -> list[str]:
    """Pull every Rust string literal (raw or plain, with optional escape
    decode) out of `body`, preserving source order. Caller decides which
    are prompt-shaped — we just hand back the raw text.
    """
    out: list[str] = []
    for m in _STRING_LITERAL_RX.finditer(body):
        if m.group("raw") is not None:
            out.append(m.group("rawbody"))
        elif m.group("plain") is not None:
            text = m.group("plainbody")
            try:
                text = text.encode("utf-8", "replace").decode("unicode_escape", "replace")
            except UnicodeDecodeError:
                pass
            out.append(text)
    return out


def _resolve_fn_call_body(text: str, fn_name: str) -> str | None:
    """Try to render a useful Markdown body for a `description: fn_name(...)`
    case by inlining the helper fn's prompt-shaped string literals.

    Heuristic: find every Rust string literal in the helper's body, drop
    obvious non-prompt strings (length ≤ 1, or containing only printable
    punctuation), and present the survivors as separate Markdown sections.
    Placeholders like `{agent_role_guidance}` are preserved verbatim — the
    model receives them filled at runtime, but the structure is what matters
    for review.

    Returns None if the helper isn't defined in the same file.
    """
    body = _resolve_fn_body_text(text, fn_name)
    if body is None:
        return None
    literals = _harvest_string_literals(body)
    interesting = [
        lit for lit in literals
        if len(lit.strip()) > 16 and not lit.strip().isdigit()
    ]
    if not interesting:
        return None
    if len(interesting) == 1:
        return interesting[0]
    parts = [
        f"## Branch {i + 1}\n\n{lit.strip()}"
        for i, lit in enumerate(interesting)
    ]
    return "\n\n".join(parts) + "\n"


def _enclosing_fn_text(text: str, struct_pos: int) -> str:
    """Return the text of the function containing the ToolSpec at struct_pos.

    Heuristic: walk backwards to the most recent `pub fn` / `fn` opener,
    then forward through balanced braces.
    """
    fn_open_rx = re.compile(r"\b(?:pub\s+)?fn\s+\w+\s*[<(]", re.MULTILINE)
    candidates = list(fn_open_rx.finditer(text, 0, struct_pos))
    if not candidates:
        return text
    fn_match = candidates[-1]
    body_open = text.find("{", fn_match.end())
    if body_open == -1:
        return text
    body_close = _scan_balanced(text, body_open + 1)
    if body_close == -1:
        return text
    return text[fn_match.start():body_close + 1]


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

            kind = "unknown"
            body = "(see source)"
            let_kind: str | None = None
            fn_callee: str | None = None

            if is_shorthand:
                # Resolve the `description` variable in the enclosing fn.
                fn_text = _enclosing_fn_text(text, m.start())
                sub_kind, sub_body, sub_label = _resolve_let_binding(fn_text, "description")
                kind = "let_binding"
                let_kind = sub_kind
                body = sub_body
                if sub_label:
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
                    win_body = _classify_inline_string(win) or f"(non-literal)\n\n```\n{win}\n```"
                    unix_body = _classify_inline_string(unix) or f"(non-literal)\n\n```\n{unix}\n```"
                    kind = "cfg_conditional"
                    body = (
                        "## Windows branch (`cfg!(windows)` true)\n\n"
                        f"{win_body}\n\n"
                        "## Unix branch (`cfg!(windows)` false)\n\n"
                        f"{unix_body}\n"
                    )
                elif const_call_m:
                    # `SOMETHING.to_string()` — try to resolve as a string const.
                    resolved = _resolve_const_with_fallback(
                        text, const_call_m.group(1), codex_rs_root
                    )
                    if resolved is not None:
                        kind = "const_ref"
                        body = resolved
                        fn_callee = const_call_m.group(1)
                    else:
                        kind = "fn_call"
                        fn_callee = const_call_m.group(1)
                        body = f"(unresolved identifier `{fn_callee}.to_string()`; see source)"
                elif ident_m:
                    fn_text = _enclosing_fn_text(text, m.start())
                    sub_kind, sub_body, sub_label = _resolve_let_binding(fn_text, ident_m.group(1))
                    kind = "let_binding"
                    let_kind = sub_kind
                    body = sub_body
                    if sub_label:
                        fn_callee = sub_label
                elif fn_call_m:
                    kind = "fn_call"
                    fn_callee = fn_call_m.group(1)
                    resolved = _resolve_fn_call_body(text, fn_callee)
                    if resolved is not None:
                        body = resolved
                        kind = "fn_call_resolved"
                    else:
                        body = (
                            f"(dynamic — `{fn_callee}(...)` builds this description at "
                            "runtime; helper fn not in same file — see source)"
                        )

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
                    parameters=params,
                )
            )
    return captures
