"""CLI entry point. M2 wires `extract` to the pipeline (Passes 1, 2, 3)."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from . import pipeline

console = Console()


@click.group()
@click.version_option(package_name="codex-prompts-extractor")
def main() -> None:
    """codex-prompts-extractor — see /SPEC.md."""


@main.command()
@click.option("--codex-root", required=True, type=click.Path(exists=True, file_okay=False))
@click.option("--tag", default=None, help="Upstream tag (default: latest rust-v*).")
@click.option("--out", required=True, type=click.Path(file_okay=False))
@click.option("--mode", type=click.Choice(["write", "dry-run"]), default="dry-run",
              help="dry-run prints what would happen; write emits files (M2 currently always writes).")
def extract(codex_root: str, tag: str | None, out: str, mode: str) -> None:
    """Extract Codex prompts at a given upstream tag (SPEC §8.1)."""
    if mode == "dry-run":
        console.print(
            "[yellow]Note:[/yellow] M2 dry-run currently writes files anyway "
            "(no diff infrastructure yet — that's M5/M6). Files will be written."
        )

    report = pipeline.run(Path(codex_root), Path(out), tag)

    table = Table(title=f"Extraction report — codex {report.codex_version} ({report.codex_commit[:10]})")
    table.add_column("Pass / metric", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_row("Pass 1: include_str! candidates", str(report.pass1_count))
    table.add_row("Pass 1: models.json fan-out entries", str(report.pass1_models_count))
    table.add_row("Pass 2: kept after denylist", str(report.pass2_kept))
    table.add_row("Pass 2: dropped by denylist", str(report.pass2_dropped))
    table.add_row("Pass 3: files written", str(report.pass3_written))
    table.add_row("Pass 3: orphans (uncategorized)", str(report.pass3_orphans))
    console.print(table)


@main.command()
@click.option("--category", required=True, help="Category prefix (e.g., 'tool', 'mode').")
def diff(category: str) -> None:
    """Show diff for a specific category from the most recent dry-run (SPEC §8.2)."""
    raise NotImplementedError("M5/M6 will implement.")


if __name__ == "__main__":
    main()
