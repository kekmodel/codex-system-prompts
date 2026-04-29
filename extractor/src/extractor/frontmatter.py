"""Generate YAML frontmatter for captured prompts (SPEC §3.3)."""

from __future__ import annotations

from pathlib import Path

import yaml


def render(
    name: str,
    category: str,
    codex_version: str,
    codex_commit: str,
    source_path: Path,
    source_kind: str,
    callsite: str | None,
    extraction_pass: int,
    extraction_method: str,
    tokens_o200k_base: int,
    description: str,
    extra: dict | None = None,
) -> str:
    """Render YAML frontmatter (between --- markers) per SPEC §3.3."""
    data: dict = {
        "name": name,
        "category": category,
        "codex_version": codex_version,
        "codex_commit": codex_commit,
        "source": {
            "path": str(source_path).replace("\\", "/"),
            "kind": source_kind,
        },
        "extraction": {
            "pass": extraction_pass,
            "method": extraction_method,
        },
        "variables": [],
        "tokens": {
            "o200k_base": tokens_o200k_base,
        },
        "description": description,
    }
    if callsite:
        data["source"]["reached_from"] = [callsite]
    if extra:
        # Merge nested keys instead of clobbering.
        for k, v in extra.items():
            if k in data and isinstance(data[k], dict) and isinstance(v, dict):
                data[k].update(v)
            else:
                data[k] = v

    yaml_body = yaml.safe_dump(
        data, sort_keys=False, allow_unicode=True, default_flow_style=False
    )
    return f"---\n{yaml_body}---\n"
