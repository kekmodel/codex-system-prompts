"""Pass 1 (cont.): models.json fan-out — one captured prompt per model slug (SPEC §2.4)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelEntry:
    slug: str                     # e.g. "gpt-5.2-codex"
    base_instructions: str        # the prompt body
    json_pointer: str             # source pointer into models.json


def fan_out(codex_rs: Path) -> list[ModelEntry]:
    """Read models.json and return one ModelEntry per model slug with non-empty base_instructions.

    Actual structure (verified at rust-v0.126.0-alpha.12):
        {"models": [ {..., "slug": "gpt-5.5", "base_instructions": "..."}, ... ]}
    """
    p = codex_rs / "models-manager" / "models.json"
    if not p.is_file():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))

    out: list[ModelEntry] = []
    if not isinstance(data, dict):
        return out
    models = data.get("models")
    if not isinstance(models, list):
        return out
    for idx, entry in enumerate(models):
        if not isinstance(entry, dict):
            continue
        slug = entry.get("slug") or entry.get("name") or entry.get("id")
        body = entry.get("base_instructions")
        if not isinstance(slug, str) or not isinstance(body, str) or not body.strip():
            continue
        out.append(
            ModelEntry(
                slug=slug,
                base_instructions=body,
                json_pointer=f"/models/{idx}/base_instructions",
            )
        )
    return out
