"""Token counting via tiktoken (SPEC §7)."""

from __future__ import annotations

import tiktoken

_ENCODER = None


def _enc():
    global _ENCODER
    if _ENCODER is None:
        _ENCODER = tiktoken.get_encoding("o200k_base")
    return _ENCODER


def count_o200k_base(text: str) -> int:
    """Token count under o200k_base. Used for both static and template prompts (SPEC §7)."""
    return len(_enc().encode(text))
