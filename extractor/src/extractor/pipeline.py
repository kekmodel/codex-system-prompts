"""Pipeline orchestrator — runs M2 passes (1, 2, 3) end-to-end (SPEC §2.2)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import codex, pass1_autoinclude, pass1_models, pass2_denylist, pass3_emit


@dataclass
class RunReport:
    pass1_count: int
    pass1_models_count: int
    pass2_kept: int
    pass2_dropped: int
    pass3_written: int
    pass3_orphans: int
    codex_version: str
    codex_commit: str


def run(codex_root: Path, out_root: Path, tag: str | None) -> RunReport:
    """Execute Passes 1, 2, 3 and emit captured prompts under out_root/prompts/."""
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

    # Pass 2: denylist filter
    denylist = pass2_denylist.load(extractor_dir)
    kept, dropped = pass2_denylist.filter_candidates(candidates, denylist)

    # Pass 3: categorize & emit (auto-include + models fan-out)
    emitted = pass3_emit.emit(
        kept, model_entries, out_root, codex_version=version, codex_commit=commit
    )

    return RunReport(
        pass1_count=len(candidates),
        pass1_models_count=len(model_entries),
        pass2_kept=len(kept),
        pass2_dropped=len(dropped),
        pass3_written=len(emitted.written),
        pass3_orphans=len(emitted.orphans),
        codex_version=version,
        codex_commit=commit,
    )
