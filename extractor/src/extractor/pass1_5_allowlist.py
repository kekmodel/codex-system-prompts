"""Pass 1.5: allow-list resolution (SPEC §2.1 (B), §2.2).

M3 ships only the skeleton: read `extractor/allow_list.toml` and return its
entries. M5 will implement actual resolution via the in-workspace shim crate
(§2.3.1) for programmatic prompts and direct symbol-finding for inline raw-
string constants.
"""

from __future__ import annotations

import tomllib
from pathlib import Path


def load(extractor_dir: Path) -> list[dict]:
    """Load entries from allow_list.toml. Returns [] if file has no [[entry]] entries."""
    with open(extractor_dir / "allow_list.toml", "rb") as f:
        data = tomllib.load(f)
    return data.get("entry", [])


def resolve(entries: list[dict], codex_rs: Path):
    """Stub. M5 will resolve entries to captured fragments via the shim (SPEC §2.3.1)."""
    if not entries:
        return []
    raise NotImplementedError(
        "Allow-list resolution requires the M5 shim. "
        "Currently allow_list.toml has no [[entry]] items, so this code is unreachable."
    )
