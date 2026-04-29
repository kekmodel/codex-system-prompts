"""Pipeline orchestrator — runs M2/M3 passes (1, 1.5, 2, 3, 3-orphan) end-to-end (SPEC §2.2)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import (
    codex,
    pass1_autoinclude,
    pass1_5_allowlist,
    pass1_models,
    pass2_denylist,
    pass3_emit,
    pass3_orphans,
)


@dataclass
class RunReport:
    pass1_count: int
    pass1_models_count: int
    pass1_5_allowlist_entries: int
    pass2_kept: int
    pass2_dropped: int
    pass3_written: int
    pass3_uncategorized: int      # candidates with no rule match (separate from orphan-walk)
    orphan_written: int
    orphan_skipped_empty: int
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

    # Pass 1.5: allow-list resolution (M3 skeleton: empty until M5 shim)
    allow_entries = pass1_5_allowlist.load(extractor_dir)
    pass1_5_allowlist.resolve(allow_entries, codex_rs)  # raises if non-empty

    # Pass 2: denylist filter
    denylist = pass2_denylist.load(extractor_dir)
    kept, dropped = pass2_denylist.filter_candidates(candidates, denylist)

    # Pass 3: categorize & emit (auto-include + models fan-out)
    emitted = pass3_emit.emit(
        kept, model_entries, out_root, codex_version=version, codex_commit=commit
    )

    # Pass 3 (orphan audit): walk codex-rs/ for prompt-shaped files NOT captured.
    captured_paths = {c.target_path for c in kept}
    # Also include models.json itself so we don't orphan-walk it (handled by fan-out).
    captured_paths.add((codex_rs / "models-manager" / "models.json").resolve())
    orphans = pass3_orphans.walk_orphans(codex_rs, captured_paths, denylist)
    orphan_result = pass3_orphans.emit(
        orphans, codex_rs, out_root, codex_version=version, codex_commit=commit
    )

    return RunReport(
        pass1_count=len(candidates),
        pass1_models_count=len(model_entries),
        pass1_5_allowlist_entries=len(allow_entries),
        pass2_kept=len(kept),
        pass2_dropped=len(dropped),
        pass3_written=len(emitted.written),
        pass3_uncategorized=len(emitted.orphans),
        orphan_written=len(orphan_result.written),
        orphan_skipped_empty=len(orphan_result.skipped_empty),
        codex_version=version,
        codex_commit=commit,
    )
