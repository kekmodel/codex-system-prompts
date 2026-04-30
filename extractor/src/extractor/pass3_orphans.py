"""Pass 3 (orphan audit): emit prompt-shaped files not reached by include_str! / allow-list.

Per SPEC §1.3 boundary cases, files like `core/templates/personalities/*.md`,
`core/templates/agents/orchestrator.md`, `gpt_5_codex_prompt.md` etc. exist in
the upstream tree but are not currently `include_str!`'d by any shipping crate.
We catalog them under `prompts/orphan/` with explicit "not shipped" frontmatter
so a reader can find them but won't mistake them for canonical content.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import pass2_denylist
from .frontmatter import render as render_frontmatter
from .tokens import count_o200k_base

# File extensions that COULD plausibly carry a prompt.
PROMPT_EXTENSIONS = {".md", ".markdown", ".lark", ".toml", ".txt", ".xml"}

# Files that look prompt-shaped by extension but aren't prompts.
NON_PROMPT_FILENAMES = {
    "Cargo.toml",
    "Cargo.lock",
    "rust-toolchain.toml",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "LICENSE.md",
    "NOTICE",
    ".gitignore",
    ".gitattributes",
    "AGENTS.md",  # codex's own AGENTS.md is config codex consumes (SPEC §1.3)
    ".markdownlint-cli2.yaml",
}


@dataclass
class OrphanResult:
    written: list[Path]
    skipped_empty: list[Path]


def walk_orphans(
    codex_rs: Path,
    captured_paths: set[Path],
    denylist: dict,
) -> list[Path]:
    """Find prompt-shaped files in codex-rs/ NOT in captured_paths and not denied."""
    found: list[Path] = []
    for path in codex_rs.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in PROMPT_EXTENSIONS:
            continue
        if path.name in NON_PROMPT_FILENAMES:
            continue
        rel = path.relative_to(codex_rs)
        # Skip test/bench/example paths
        if any(p in {"tests", "benches", "examples"} for p in rel.parts):
            continue
        if rel.name in {"tests.rs", "test.rs"}:
            continue
        if pass2_denylist.is_denied(rel, denylist):
            continue
        if path.resolve() in captured_paths:
            continue
        found.append(path)
    return sorted(found, key=lambda p: str(p))


def _orphan_filename(rel: Path) -> str:
    """Flatten relative path → kebab-case filename."""
    parts = list(rel.with_suffix("").parts)
    flat = "-".join(parts).replace("_", "-").replace(".", "-")
    if len(flat) > 100:
        flat = flat[:100]
    return f"orphan-{flat}.md"


def emit(
    orphans: list[Path],
    codex_rs: Path,
    out_root: Path,
    codex_version: str,
    codex_commit: str,
) -> OrphanResult:
    written: list[Path] = []
    skipped_empty: list[Path] = []
    for orphan in orphans:
        rel = orphan.relative_to(codex_rs)
        try:
            body = orphan.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if not body.strip():
            skipped_empty.append(orphan)
            continue

        token_count = count_o200k_base(body)
        filename = _orphan_filename(rel)

        fm = render_frontmatter(
            name=f"Orphan: codex-rs/{rel}",
            category="orphan",
            codex_version=codex_version,
            codex_commit=codex_commit,
            source_path=Path("codex-rs") / rel,
            source_kind="orphan_unreferenced",
            callsite=None,
            extraction_pass=3,
            extraction_method="orphan_walk",
            tokens_o200k_base=token_count,
            description=f"Orphan: `codex-rs/{rel}` (not `include_str!`'d).",
            extra={"source": {"shipping_status": "not_shipped"}},
        )

        out_path = out_root / "prompts" / "orphan" / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(fm + body)
        written.append(out_path.relative_to(out_root))

    return OrphanResult(written=written, skipped_empty=skipped_empty)
