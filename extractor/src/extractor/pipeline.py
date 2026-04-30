"""Pipeline orchestrator — runs M2/M3 passes (1, 1.5, 2, 3, 3-orphan) end-to-end (SPEC §2.2)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import (
    codex,
    pass1_autoinclude,
    pass1_5_allowlist,
    pass1_7_toolspec,
    pass1_fragments,
    pass1_models,
    pass2_denylist,
    pass3_emit,
    pass3_orphans,
    pass4_verify,
    pass5_index,
)


@dataclass
class RunReport:
    pass1_count: int
    pass1_models_count: int
    pass1_5_allowlist_entries: int
    pass1_6_fragments_count: int
    pass1_7_toolspec_count: int
    pass2_kept: int
    pass2_dropped: int
    pass3_written: int
    pass3_allowlist_written: int
    pass3_fragments_written: int
    pass3_toolspec_written: int
    pass3_toolspec_params_written: int
    pass3_uncategorized: int      # candidates with no rule match (separate from orphan-walk)
    orphan_written: int
    orphan_skipped_empty: int
    pass5_indexed_files: int
    pass5_total_tokens: int
    pass5_verify_passed: bool
    codex_version: str
    codex_commit: str


def run(codex_root: Path, out_root: Path, tag: str | None) -> RunReport:
    """Execute the M2/M3 pipeline and emit captured + orphan prompts."""
    codex_root = codex.resolve_codex_root(codex_root)
    out_root = Path(out_root).resolve()
    if not (out_root / "prompts").is_dir():
        raise ValueError(
            f"{out_root} doesn't look like a mirror repo (missing prompts/). "
            "Run M1 setup first."
        )
    codex_rs = codex_root / "codex-rs"
    extractor_dir = out_root / "extractor"

    version, commit = codex.resolve_baseline(codex_root, tag)

    # Pass 1: auto-include enumeration
    candidates = pass1_autoinclude.walk(codex_rs)

    # Pass 1 (cont.): models.json fan-out
    model_entries = pass1_models.fan_out(codex_rs)

    # Pass 1.5: allow-list resolution (M5a — Rust source static parsing)
    allow_entries = pass1_5_allowlist.load(extractor_dir)
    allow_captures = pass1_5_allowlist.resolve(allow_entries, codex_rs)

    # Pass 1.6: ContextualUserFragment auto-discovery (M5b)
    fragment_captures = pass1_fragments.walk(codex_rs)

    # Pass 1.7: ToolSpec auto-discovery (M9 — SPEC §1.1 (a)-(d), §2.2)
    toolspec_captures = pass1_7_toolspec.walk(codex_rs)

    # Pass 2: denylist filter
    denylist = pass2_denylist.load(extractor_dir)
    kept, dropped = pass2_denylist.filter_candidates(candidates, denylist)

    # Pass 3: categorize & emit (auto-include + models + allow-list +
    # fragments + toolspec)
    emitted = pass3_emit.emit(
        kept,
        model_entries,
        allow_captures,
        fragment_captures,
        toolspec_captures,
        out_root,
        codex_version=version,
        codex_commit=commit,
    )

    # Pass 3 (orphan audit): walk codex-rs/ for prompt-shaped files NOT captured.
    captured_paths = {c.target_path for c in kept}
    # Also include models.json itself so we don't orphan-walk it (handled by fan-out).
    captured_paths.add((codex_rs / "models-manager" / "models.json").resolve())
    orphans = pass3_orphans.walk_orphans(codex_rs, captured_paths, denylist)
    orphan_result = pass3_orphans.emit(
        orphans, codex_rs, out_root, codex_version=version, codex_commit=commit
    )

    # Pass 4: verification (used as input to Pass 5 coverage section)
    verify_report = pass4_verify.verify(codex_root, out_root, extractor_dir)

    # Pass 5: index generation (README + CHANGELOG)
    index_result = pass5_index.run(out_root, version, commit, verify_report)

    return RunReport(
        pass1_count=len(candidates),
        pass1_models_count=len(model_entries),
        pass1_5_allowlist_entries=len(allow_entries),
        pass1_6_fragments_count=len(fragment_captures),
        pass1_7_toolspec_count=len(toolspec_captures),
        pass2_kept=len(kept),
        pass2_dropped=len(dropped),
        pass3_written=len(emitted.written),
        pass3_allowlist_written=emitted.allowlist_written,
        pass3_fragments_written=emitted.fragment_written,
        pass3_toolspec_written=emitted.toolspec_written,
        pass3_toolspec_params_written=emitted.toolspec_params_written,
        pass3_uncategorized=len(emitted.orphans),
        orphan_written=len(orphan_result.written),
        orphan_skipped_empty=len(orphan_result.skipped_empty),
        pass5_indexed_files=index_result.file_count,
        pass5_total_tokens=index_result.total_tokens,
        pass5_verify_passed=verify_report.passed,
        codex_version=version,
        codex_commit=commit,
    )
