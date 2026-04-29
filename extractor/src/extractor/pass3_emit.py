"""Pass 3: categorize captured candidates and emit `prompts/<category>/<filename>.md` (SPEC §2.2, §3.3)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .categorizer import categorize
from .frontmatter import render as render_frontmatter
from .pass1_5_allowlist import AllowListCapture
from .pass1_autoinclude import Candidate
from .pass1_models import ModelEntry
from .tokens import count_o200k_base


@dataclass
class EmitResult:
    written: list[Path]            # paths written (relative to mirror repo)
    orphans: list[Candidate]       # candidates with no matching category rule
    allowlist_written: int = 0     # count of allow-list captures emitted


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


def emit(
    candidates: list[Candidate],
    model_entries: list[ModelEntry],
    allowlist_captures: list[AllowListCapture],
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

    return EmitResult(written=written, orphans=orphans, allowlist_written=allowlist_written)
