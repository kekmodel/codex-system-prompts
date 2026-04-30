"""Pass 3: categorize captured candidates and emit `prompts/<category>/<filename>.md` (SPEC §2.2, §3.3)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .categorizer import categorize
from .frontmatter import render as render_frontmatter
from .pass1_5_allowlist import AllowListCapture
from .pass1_7_toolspec import ToolSpecCapture
from .pass1_autoinclude import Candidate
from .pass1_fragments import FragmentCapture
from .pass1_models import ModelEntry
from .tokens import count_o200k_base


@dataclass
class EmitResult:
    written: list[Path]            # paths written (relative to mirror repo)
    orphans: list[Candidate]       # candidates with no matching category rule
    allowlist_written: int = 0     # count of allow-list captures emitted
    fragment_written: int = 0      # count of ContextualUserFragment captures emitted
    toolspec_written: int = 0      # count of inline ToolSpec captures emitted (Pass 1.7)


def _kind_label(file_path: Path) -> str:
    """Map file extension → SPEC §3.3 source.kind label for include_str!-derived sources."""
    ext = file_path.suffix.lower()
    if ext in (".md", ".markdown"):
        return "include_str"
    if ext in (".toml",):
        return "include_str"
    if ext in (".lark",):
        return "include_str"
    if ext in (".json",):
        return "include_str"
    if ext in (".txt",):
        return "include_str"
    return "include_bytes"


def _description(target_rel: Path, category: str) -> str:
    """Best-effort description from the target's path. M5+ will refine."""
    return (
        f"Auto-extracted by Pass 3 (M2) from `codex-rs/{target_rel}`. "
        f"Category: {category}. Description will be refined at M5 review."
    )


def _struct_to_filename(name: str) -> str:
    """CamelCase struct name → kebab-case filename stem."""
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0 and not name[i - 1].isupper():
            out.append("-")
        out.append(ch.lower())
    return "".join(out)


def emit(
    candidates: list[Candidate],
    model_entries: list[ModelEntry],
    allowlist_captures: list[AllowListCapture],
    fragment_captures: list[FragmentCapture],
    toolspec_captures: list[ToolSpecCapture],
    out_root: Path,
    codex_version: str,
    codex_commit: str,
) -> EmitResult:
    """Materialize captured prompts under <out_root>/prompts/<category>/."""
    written: list[Path] = []
    orphans: list[Candidate] = []
    seen: dict[Path, Candidate] = {}  # dedupe: same target_path captured from multiple callsites

    # ========== Auto-include candidates ==========
    for c in candidates:
        if c.target_path in seen:
            continue
        seen[c.target_path] = c

        result = categorize(c.target_rel)
        if result is None:
            orphans.append(c)
            continue
        category, filename = result

        body = c.target_path.read_text(encoding="utf-8") if c.kind == "str" else ""
        if not body:
            continue

        token_count = count_o200k_base(body)
        callsite = (
            f"{c.callsite_file.relative_to(out_root.parent / 'codex' / 'codex-rs')}:{c.callsite_line}"
            if (out_root.parent / "codex" / "codex-rs") in c.callsite_file.parents
            else f"{c.callsite_file.name}:{c.callsite_line}"
        )

        fm = render_frontmatter(
            name=f"{category.capitalize()}: {filename}",
            category=category,
            codex_version=codex_version,
            codex_commit=codex_commit,
            source_path=Path("codex-rs") / c.target_rel,
            source_kind=_kind_label(c.target_path),
            callsite=callsite,
            extraction_pass=1,
            extraction_method="file",
            tokens_o200k_base=token_count,
            description=_description(c.target_rel, category),
        )

        out_path = out_root / "prompts" / category / f"{filename}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(fm + body)
        written.append(out_path.relative_to(out_root))

    # ========== Models.json fan-out ==========
    for me in model_entries:
        # Slug normalization: only minimal — strip slashes and spaces.
        safe_slug = me.slug.replace("/", "-").replace(" ", "-")
        filename = f"base-instructions-{safe_slug}.md"
        token_count = count_o200k_base(me.base_instructions)

        fm = render_frontmatter(
            name=f"Base instructions: {me.slug}",
            category="base-instructions",
            codex_version=codex_version,
            codex_commit=codex_commit,
            source_path=Path("codex-rs/models-manager/models.json"),
            source_kind="json_field",
            callsite=None,
            extraction_pass=1,
            extraction_method="json_field",
            tokens_o200k_base=token_count,
            description=(
                f"Per-model `base_instructions` for slug `{me.slug}`, "
                f"fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. "
                f"JSON pointer: {me.json_pointer}."
            ),
            extra={
                "source": {
                    "json_pointer": me.json_pointer,
                },
            },
        )

        out_path = out_root / "prompts" / "base-instructions" / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(fm + me.base_instructions)
        written.append(out_path.relative_to(out_root))

    # ========== Allow-list captures (Pass 1.5 — M5a) ==========
    allowlist_written = 0
    for cap in allowlist_captures:
        if not cap.body.strip():
            continue
        token_count = count_o200k_base(cap.body)
        callsite = f"{cap.source_rel}:{cap.source_line}"
        extra: dict = {}
        if cap.symbol:
            extra.setdefault("source", {})["symbol"] = cap.symbol
        if cap.extra:
            for k, v in cap.extra.items():
                extra.setdefault("source", {})[k] = v

        fm = render_frontmatter(
            name=f"{cap.category.capitalize()}: {cap.filename}",
            category=cap.category,
            codex_version=codex_version,
            codex_commit=codex_commit,
            source_path=Path("codex-rs") / cap.source_rel,
            source_kind=cap.source_kind,
            callsite=callsite,
            extraction_pass=1.5,
            extraction_method=cap.extraction_method,
            tokens_o200k_base=token_count,
            description=cap.description,
            extra=extra or None,
        )
        out_path = out_root / "prompts" / cap.category / f"{cap.filename}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(fm + cap.body)
        written.append(out_path.relative_to(out_root))
        allowlist_written += 1

    # ========== ContextualUserFragment captures (Pass 1.6 — M5b) ==========
    fragment_written = 0
    for fc in fragment_captures:
        kebab = _struct_to_filename(fc.struct_name)
        filename = f"context-fragment-{kebab}"

        # Compose body of the .md file:
        #   • If we extracted a clean template: show START_MARKER + template + END_MARKER
        #   • Else: show START_MARKER + Rust code block of body() + END_MARKER
        if fc.body_template is not None:
            md_body = (
                f"{fc.start_marker}{fc.body_template}{fc.end_marker}\n"
                if not fc.start_marker and not fc.end_marker
                else f"{fc.start_marker}\n{fc.body_template}\n{fc.end_marker}\n"
            )
            kind_suffix = "template"
        else:
            block = (
                "```rust\nfn body(&self) -> String {\n"
                + fc.body_source
                + "\n}\n```\n"
            )
            wrapped = (
                f"{block}\n"
                if not fc.start_marker and not fc.end_marker
                else f"{fc.start_marker}\n\n{block}\n{fc.end_marker}\n"
            )
            md_body = wrapped
            kind_suffix = "function-body-source"

        token_count = count_o200k_base(md_body)
        callsite = f"{fc.source_rel}:{fc.source_line}"

        extra: dict = {
            "source": {
                "struct": fc.struct_name,
                "role": fc.role,
                "start_marker": fc.start_marker,
                "end_marker": fc.end_marker,
                "body_extraction": kind_suffix,
            }
        }

        fm = render_frontmatter(
            name=f"Context fragment: {fc.struct_name}",
            category="context-fragment",
            codex_version=codex_version,
            codex_commit=codex_commit,
            source_path=Path("codex-rs") / fc.source_rel,
            source_kind="rust_contextual_user_fragment",
            callsite=callsite,
            extraction_pass=1.6,
            extraction_method="rust_contextual_user_fragment",
            tokens_o200k_base=token_count,
            description=(
                f"`{fc.struct_name}` ContextualUserFragment from "
                f"`codex-rs/{fc.source_rel}`. Role: {fc.role!r}. "
                f"Markers: {fc.start_marker!r} … {fc.end_marker!r}. "
                f"body() captured as {kind_suffix}."
            ),
            extra=extra,
        )
        out_path = out_root / "prompts" / "context-fragment" / f"{filename}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(fm + md_body)
        written.append(out_path.relative_to(out_root))
        fragment_written += 1

    # ========== ToolSpec captures (Pass 1.7 — M9) ==========
    #
    # Each captured ToolSpec emits one (or two, for cfg!(windows)) JSON
    # documents matching the wire format the model receives — i.e. the
    # same shape as `serde_json::to_string(&tool_spec)` in codex's
    # ResponsesApiTool serializer. The body of each .md file is the raw
    # JSON the model sees; nothing else is added.
    toolspec_written = 0
    safe_name_rx = re.compile(r"[^a-z0-9]+")

    def _build_tool_json(
        tool_name: str, description: str, parameters: list
    ) -> dict:
        properties: dict[str, dict] = {}
        for p in parameters:
            properties[p.name] = {
                "type": p.schema_type,
                "description": p.description,
            }
        return {
            "type": "function",
            "name": tool_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
            },
        }

    def _emit_toolspec(
        slug: str,
        variant_suffix: str,
        tc,
        description_text: str,
    ) -> None:
        nonlocal toolspec_written
        # Pick a filename, appending `-v2`, `-v3`, … on collision (two
        # ToolSpec literals with the same tool_name in the same file —
        # e.g. wait_agent v1 vs v2).
        base = f"tool-{slug}{variant_suffix}"
        out_path = out_root / "prompts" / "tool" / f"{base}.md"
        rel_path = out_path.relative_to(out_root)
        n = 1
        while rel_path in written:
            n += 1
            out_path = out_root / "prompts" / "tool" / f"{base}-v{n}.md"
            rel_path = out_path.relative_to(out_root)

        tool_json = _build_tool_json(tc.tool_name, description_text, tc.parameters)
        body = json.dumps(tool_json, indent=2, ensure_ascii=False) + "\n"
        token_count = count_o200k_base(body)

        extra: dict = {"source": {"tool_name": tc.tool_name}}
        if variant_suffix:
            extra["source"]["cfg_branch"] = variant_suffix.lstrip("-")

        fm = render_frontmatter(
            name=f"Tool: {tc.tool_name}",
            category="tool",
            codex_version=codex_version,
            codex_commit=codex_commit,
            source_path=Path("codex-rs") / tc.file_rel,
            source_kind="rust_toolspec_inline",
            callsite=f"{tc.file_rel}:{tc.line}",
            extraction_pass=1.7,
            extraction_method="rust_toolspec_inline",
            tokens_o200k_base=token_count,
            description=f"`{tc.tool_name}` ToolSpec.",
            extra=extra,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(fm + body)
        written.append(rel_path)
        toolspec_written += 1

    for tc in toolspec_captures:
        slug = safe_name_rx.sub("-", tc.tool_name.lower()).strip("-")

        # Skip captures whose description we cannot resolve at all — emitting
        # a JSON with an empty description string would be misleading. fn_call
        # / unresolved-let cases land here; resolving them is a follow-up.
        if (
            not tc.description.strip()
            and tc.windows_description is None
            and tc.unix_description is None
        ):
            continue

        if tc.windows_description is not None or tc.unix_description is not None:
            # cfg!(windows) split — emit one file per platform branch.
            if tc.windows_description:
                _emit_toolspec(slug, "-windows", tc, tc.windows_description)
            if tc.unix_description:
                _emit_toolspec(slug, "-unix", tc, tc.unix_description)
            continue

        _emit_toolspec(slug, "", tc, tc.description)

    return EmitResult(
        written=written,
        orphans=orphans,
        allowlist_written=allowlist_written,
        fragment_written=fragment_written,
        toolspec_written=toolspec_written,
    )
