"""Pass 2: apply denylist filter (SPEC §2.1 (C))."""

from __future__ import annotations

import fnmatch
import tomllib
from pathlib import Path

from .pass1_autoinclude import Candidate


def load(extractor_dir: Path) -> dict:
    with open(extractor_dir / "denylist.toml", "rb") as f:
        return tomllib.load(f)


def _match(rel: str, pattern: str) -> bool:
    """gitignore-style glob: `**/` means zero or more directory components.

    fnmatch alone can't represent "zero or more dir components"; it conflates
    with `*` (which matches any chars). So we generate the 2^N expansions of
    each `**/` boundary (either empty or `*/`) and try each.
    """
    parts = pattern.split("**/")
    n = len(parts) - 1
    if n == 0:
        return fnmatch.fnmatch(rel, pattern.replace("**", "*"))
    for combo in range(1 << n):
        result = parts[0]
        for i in range(n):
            result += ("*/" if (combo >> i) & 1 else "") + parts[i + 1]
        if fnmatch.fnmatch(rel, result.replace("**", "*")):
            return True
    return False


def is_denied(target_rel: Path, denylist: dict) -> bool:
    rel = str(target_rel).replace("\\", "/")
    for pattern in denylist.get("paths", {}).get("exclude", []):
        if _match(rel, pattern):
            return True
    return False


def filter_candidates(
    candidates: list[Candidate], denylist: dict
) -> tuple[list[Candidate], list[Candidate]]:
    kept: list[Candidate] = []
    dropped: list[Candidate] = []
    for c in candidates:
        if is_denied(c.target_rel, denylist):
            dropped.append(c)
        else:
            kept.append(c)
    return kept, dropped
