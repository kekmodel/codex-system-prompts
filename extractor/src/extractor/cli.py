"""CLI entry point. M1 ships only stubs; M2+ populates."""

from __future__ import annotations

import click


@click.group()
@click.version_option(package_name="codex-prompts-extractor")
def main() -> None:
    """codex-prompts-extractor — see /SPEC.md."""


@main.command()
@click.option("--codex-root", required=True, type=click.Path(exists=True, file_okay=False))
@click.option("--tag", default=None, help="Upstream tag (default: latest rust-v*).")
@click.option("--out", required=True, type=click.Path(file_okay=False))
@click.option("--mode", type=click.Choice(["write", "dry-run"]), default="dry-run")
def extract(codex_root: str, tag: str | None, out: str, mode: str) -> None:
    """Extract Codex prompts at a given upstream tag (SPEC §8.1)."""
    raise NotImplementedError("M2 will implement Passes 1, 1.5, 2, 3.")


@main.command()
@click.option("--category", required=True, help="Category prefix (e.g., 'tool', 'mode').")
def diff(category: str) -> None:
    """Show diff for a specific category from the most recent dry-run (SPEC §8.2)."""
    raise NotImplementedError("M5/M6 will implement.")


if __name__ == "__main__":
    main()
