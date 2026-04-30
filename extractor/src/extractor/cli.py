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
    table.add_row("Pass 1.5: allow-list entries", str(report.pass1_5_allowlist_entries))
    table.add_row("Pass 1.6: ContextualUserFragment impls", str(report.pass1_6_fragments_count))
    table.add_row("Pass 1.7: ToolSpec inline blocks", str(report.pass1_7_toolspec_count))
    table.add_row("Pass 2: kept after denylist", str(report.pass2_kept))
    table.add_row("Pass 2: dropped by denylist", str(report.pass2_dropped))
    table.add_row("Pass 3: files written (total)", str(report.pass3_written))
    table.add_row("Pass 3:   from allow-list", str(report.pass3_allowlist_written))
    table.add_row("Pass 3:   from ContextualUserFragments", str(report.pass3_fragments_written))
    table.add_row("Pass 3:   from ToolSpec captures", str(report.pass3_toolspec_written))
    table.add_row("Pass 3:   from ToolSpec parameters", str(report.pass3_toolspec_params_written))
    table.add_row("Pass 3: uncategorized (rule miss)", str(report.pass3_uncategorized))
    table.add_row("Pass 3 (orphan audit): files written", str(report.orphan_written))
    table.add_row("Pass 3 (orphan audit): empty skipped", str(report.orphan_skipped_empty))
    table.add_row(
        "Pass 4: verification",
        "[green]passed[/green]" if report.pass5_verify_passed else "[red]FAILED[/red]",
    )
    table.add_row("Pass 5: README + CHANGELOG indexed", str(report.pass5_indexed_files))
    table.add_row("Pass 5: total tokens", f"{report.pass5_total_tokens:,}")
    console.print(table)


@main.command()
@click.option("--category", required=True, help="Category prefix (e.g., 'tool', 'mode').")
def diff(category: str) -> None:
    """Show diff for a specific category from the most recent dry-run (SPEC §8.2)."""
    raise NotImplementedError("M5/M6 will implement.")


@main.command()
@click.option("--codex-root", required=True, type=click.Path(exists=True, file_okay=False))
@click.option("--out", required=True, type=click.Path(exists=True, file_okay=False))
def verify(codex_root: str, out: str) -> None:
    """Run Pass 4 verification — Layer A (placeholder mapping) + Layer B (completeness) + token drift + frontmatter schema (SPEC §2.5)."""
    import sys

    from . import codex as codex_mod
    from . import pass4_verify

    codex_rs_root = codex_mod.resolve_codex_root(codex_root)
    out_root = Path(out).resolve()
    extractor_dir = out_root / "extractor"
    report = pass4_verify.verify(codex_rs_root, out_root, extractor_dir)

    # ===== Layer A =====
    table_a = Table(title=f"Layer A — Structural mapping ({report.snapshot_files} snapshots)")
    table_a.add_column("Placeholder", style="cyan")
    table_a.add_column("Status", style="green")
    table_a.add_column("Snap count", justify="right")
    rows: list[tuple[str, str, int]] = []
    for ph in sorted(report.placeholders_seen):
        target = pass4_verify.PLACEHOLDER_MAP.get(ph)
        n = report.placeholders_seen[ph]
        if target is None:
            rows.append((ph, "[red]UNMAPPED[/red]", n))
        elif target == "deferred_m5":
            rows.append((ph, "[yellow]deferred to M5[/yellow]", n))
        elif target.startswith("runtime_"):
            rows.append((ph, f"runtime ({target})", n))
        elif target == "out_of_scope":
            rows.append((ph, "[blue]out of scope (SPEC §10.4)[/blue]", n))
        else:
            ok = (ph, target) in report.placeholders_static_ok
            rows.append((ph, f"[green]captured @ {target}[/green]" if ok else f"[red]MISSING @ {target}[/red]", n))
    for r in rows:
        table_a.add_row(r[0], r[1], str(r[2]))
    console.print(table_a)

    # ===== Layer B + auxiliary =====
    table_b = Table(title="Layer B — Completeness + auxiliary checks")
    table_b.add_column("Check", style="cyan")
    table_b.add_column("Result", style="green")
    table_b.add_row("auto-include candidates", str(report.autoinclude_count))
    table_b.add_row(
        "auto-include missing",
        f"[red]{len(report.autoinclude_missing)}[/red]" if report.autoinclude_missing else "[green]0[/green]",
    )
    table_b.add_row("models.json entries", str(report.models_count))
    table_b.add_row(
        "models missing",
        f"[red]{len(report.models_missing)}[/red]" if report.models_missing else "[green]0[/green]",
    )
    table_b.add_row("allow-list entries", str(report.allowlist_count))
    table_b.add_row(
        "allow-list missing",
        f"[red]{len(report.allowlist_missing)}[/red]" if report.allowlist_missing else "[green]0[/green]",
    )
    table_b.add_row("token-count check_files", str(report.token_check_count))
    table_b.add_row(
        "token-count drift",
        f"[red]{len(report.token_drift)}[/red]" if report.token_drift else "[green]0[/green]",
    )
    table_b.add_row("frontmatter check_files", str(report.frontmatter_check_count))
    table_b.add_row(
        "frontmatter schema fail",
        f"[red]{len(report.frontmatter_invalid)}[/red]" if report.frontmatter_invalid else "[green]0[/green]",
    )
    console.print(table_b)

    # ===== Detail dumps for failures =====
    if report.placeholders_unmapped:
        console.print("\n[red]Unmapped placeholders (Layer A spec bug):[/red]")
        for p in report.placeholders_unmapped:
            console.print(f"  • [yellow]{p}[/yellow] (used in {report.placeholders_seen[p]} snapshots)")
    if report.placeholders_static_missing:
        console.print("\n[red]Static-mapped placeholders with empty/missing target:[/red]")
        for ph, target in report.placeholders_static_missing:
            console.print(f"  • {ph} → {target}")
    if report.autoinclude_missing:
        console.print("\n[red]Auto-include candidates not captured:[/red]")
        for p in report.autoinclude_missing[:20]:
            console.print(f"  • codex-rs/{p}")
    if report.models_missing:
        console.print(f"\n[red]Model entries not captured:[/red] {report.models_missing}")
    if report.allowlist_missing:
        console.print("\n[red]Allow-list entries not captured:[/red]")
        for ident, path in report.allowlist_missing:
            console.print(f"  • {ident} → expected at {path}")
    if report.token_drift:
        console.print("\n[red]Token-count drift:[/red]")
        for f, recorded, recomputed in report.token_drift[:20]:
            console.print(f"  • {f}: recorded={recorded}, recomputed={recomputed}")
    if report.frontmatter_invalid:
        console.print("\n[red]Frontmatter schema failures:[/red]")
        for f, msg in report.frontmatter_invalid[:20]:
            console.print(f"  • {f}: {msg}")

    # ===== Final verdict =====
    if report.passed:
        console.print("\n[bold green]✓ All verification checks passed.[/bold green]")
        sys.exit(0)
    else:
        console.print("\n[bold red]✗ Verification FAILED.[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
