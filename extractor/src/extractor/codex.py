"""Codex repo introspection helpers (SPEC §6, §8.1)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def resolve_codex_root(path: str | Path) -> Path:
    """Validate path looks like a codex checkout and return canonical absolute path."""
    p = Path(path).expanduser().resolve()
    if not (p / "codex-rs" / "Cargo.toml").exists():
        raise ValueError(
            f"{p} does not look like a codex checkout "
            "(missing codex-rs/Cargo.toml)"
        )
    return p


def current_head(codex_root: Path) -> str:
    """Returns the SHA of HEAD."""
    return subprocess.check_output(
        ["git", "-C", str(codex_root), "rev-parse", "HEAD"], text=True
    ).strip()


def latest_rust_tag(codex_root: Path) -> str | None:
    """Returns the most-recently-created rust-v* tag, or None if none exist."""
    out = subprocess.check_output(
        ["git", "-C", str(codex_root), "tag", "--sort=-creatordate"], text=True
    )
    for line in out.splitlines():
        if line.startswith("rust-v"):
            return line
    return None


def resolve_baseline(codex_root: Path, tag: str | None) -> tuple[str, str]:
    """Resolve (tag, sha) for extraction baseline.

    If tag is None, uses latest rust-v* tag if present, else HEAD with synthetic tag.
    Per SPEC §6: baseline = latest tag (NOT main).
    """
    sha = current_head(codex_root)
    if tag is not None:
        # User explicitly named a tag; ensure HEAD is at that tag (M2: warn only).
        return (tag, sha)
    discovered = latest_rust_tag(codex_root)
    if discovered is None:
        return ("HEAD", sha)
    return (discovered, sha)
