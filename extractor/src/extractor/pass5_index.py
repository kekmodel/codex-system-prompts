"""Pass 5: README + CHANGELOG generation (SPEC §3.4, §3.5)."""

from __future__ import annotations

import collections
from dataclasses import dataclass
from pathlib import Path

import yaml

from .pass4_verify import VerifyReport


# SPEC §3.2 prefix order, plus orphan/feature-gated last.
CATEGORY_ORDER = [
    "base-instructions",
    "mode",
    "permission",
    "context-fragment",
    "tool",
    "agent",
    "memory",
    "code-mode",
    "tui",
    "personality",
    "data",
    "feature-gated",
    "orphan",
]

CATEGORY_DESCRIPTIONS = {
    "base-instructions": "Per-model `base_instructions` (fanned out from `models.json`) + fallbacks.",
    "mode": "Mode-specific prompts: review, compact, realtime, goals, guardian, collaboration.",
    "permission": "Approval-policy and sandbox-mode prompt fragments.",
    "context-fragment": "ContextualUserFragment wrappers — XML-tagged user-message injections.",
    "tool": "Built-in tool descriptions (apply_patch, spawn_agent guidance, MCP message templates).",
    "agent": "Built-in agent roles + agent_names list + hierarchical-agent message.",
    "memory": "/memories skill prompts.",
    "code-mode": "Code-mode (JS-orchestration tool) description constants.",
    "tui": "TUI-injected prompts (e.g. /init).",
    "personality": "Personality template fragments.",
    "data": "Static reference data embedded in the binary (apply_patch grammar, agent_names list, etc.).",
    "feature-gated": "Non-default-feature prompts (e.g. `child_agents_md`-gated).",
    "orphan": "Prompt-shaped files in upstream that are NOT `include_str!`'d. Historical/unshipped per SPEC §1.3.",
}


AUTOGEN_START = "<!-- AUTO-GENERATED-START -->"
AUTOGEN_END = "<!-- AUTO-GENERATED-END -->"


@dataclass
class IndexResult:
    file_count: int
    total_tokens: int
    by_category: dict[str, list[dict]]


def _collect(out_root: Path) -> dict[str, list[dict]]:
    """Walk prompts/ and group frontmatter records by category."""
    by_cat: dict[str, list[dict]] = collections.defaultdict(list)
    for md in (out_root / "prompts").rglob("*.md"):
        if md.name == ".gitkeep":
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        try:
            end = text.index("\n---\n", 4)
            fm = yaml.safe_load(text[4:end])
        except (ValueError, yaml.YAMLError):
            continue
        cat = fm.get("category", "uncategorized")
        tokens = fm.get("tokens", {}).get("o200k_base", 0)
        desc = (fm.get("description") or "").replace("\n", " ").strip()
        if len(desc) > 240:
            desc = desc[:240].rstrip() + "…"
        by_cat[cat].append(
            {
                "path": md.relative_to(out_root),
                "filename": md.name,
                "tokens": tokens,
                "description": desc,
                "name": fm.get("name", ""),
            }
        )
    return by_cat


def _render_corpus_section(
    by_cat: dict[str, list[dict]], codex_version: str
) -> str:
    total_files = sum(len(v) for v in by_cat.values())
    total_tokens = sum(sum(f["tokens"] for f in files) for files in by_cat.values())
    out: list[str] = []
    out.append("## Captured prompt corpus")
    out.append("")
    out.append(
        f"**{total_files} files** at codex `{codex_version}`, totaling "
        f"**{total_tokens:,} tokens** (o200k_base, template counts — "
        "see *Token-count caveat* above)."
    )
    out.append("")
    for cat in CATEGORY_ORDER:
        if cat not in by_cat or not by_cat[cat]:
            continue
        files = sorted(by_cat[cat], key=lambda f: f["filename"])
        cat_total = sum(f["tokens"] for f in files)
        cat_desc = CATEGORY_DESCRIPTIONS.get(cat, "")
        out.append(f"### `prompts/{cat}/` — {len(files)} files, {cat_total:,} tokens")
        if cat_desc:
            out.append("")
            out.append(f"_{cat_desc}_")
        out.append("")
        for f in files:
            out.append(
                f"- [`{f['filename']}`](./{f['path']}) — **{f['tokens']:,}** tokens — {f['description']}"
            )
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def _render_coverage_section(verify_report: VerifyReport) -> str:
    """Per SPEC §2.5 + §3.4: report Layer A + Layer B + auxiliary."""
    rep = verify_report
    captured_static = len(rep.placeholders_static_ok)
    runtime = len(rep.placeholders_runtime)
    out_of_scope = len(rep.placeholders_out_of_scope)
    deferred = len(rep.placeholders_deferred_m5)
    unmapped = len(rep.placeholders_unmapped)
    static_missing = len(rep.placeholders_static_missing)
    total_ph = len(rep.placeholders_seen)

    out = ["## Coverage", ""]
    out.append("Per [SPEC §2.5](./SPEC.md#25-verification--two-layers-t13-refined-v05).")
    out.append("")
    out.append("### Layer A — Structural mapping")
    out.append("")
    out.append(
        f"**{rep.snapshot_files} snapshots**, **{total_ph} unique placeholders** "
        f"({captured_static} captured-static, {runtime} runtime, "
        f"{out_of_scope} out-of-scope, {deferred} deferred, {unmapped} unmapped)"
    )
    if unmapped:
        out.append("")
        out.append(
            f"⚠ **{unmapped} placeholder(s) unmapped — spec bug, see verify --output for details.**"
        )
    if static_missing:
        out.append("")
        out.append(
            f"⚠ **{static_missing} static-mapped placeholder(s) point at empty/missing target.**"
        )
    out.append("")
    out.append("### Layer B — Completeness")
    out.append("")
    out.append("| Source | Captured | Total | Missing |")
    out.append("|---|---:|---:|---:|")
    out.append(
        f"| Auto-include (`include_str!`/`include_bytes!`) | "
        f"{rep.autoinclude_count - len(rep.autoinclude_missing)} | "
        f"{rep.autoinclude_count} | {len(rep.autoinclude_missing)} |"
    )
    out.append(
        f"| `models.json` fan-out | "
        f"{rep.models_count - len(rep.models_missing)} | "
        f"{rep.models_count} | {len(rep.models_missing)} |"
    )
    out.append(
        f"| Allow-list (Pass 1.5) | "
        f"{rep.allowlist_count - len(rep.allowlist_missing)} | "
        f"{rep.allowlist_count} | {len(rep.allowlist_missing)} |"
    )
    out.append("")
    out.append("### Auxiliary")
    out.append("")
    out.append("| Check | Files | Issues |")
    out.append("|---|---:|---:|")
    out.append(f"| Token-count drift | {rep.token_check_count} | {len(rep.token_drift)} |")
    out.append(
        f"| Frontmatter schema | {rep.frontmatter_check_count} | {len(rep.frontmatter_invalid)} |"
    )
    out.append("")
    if rep.passed:
        out.append("**✓ All verification checks passed.**")
    else:
        out.append("**✗ Verification FAILED. See `extractor verify` output for details.**")
    out.append("")
    out.append(
        "> Neither layer proves complete capture. Layer A only validates *what tests "
        "exercise*; Layer B is bounded by allow-list curation. See SPEC §2.5 for limits."
    )
    return "\n".join(out).rstrip() + "\n"


def update_readme(
    out_root: Path,
    codex_version: str,
    by_cat: dict[str, list[dict]],
    verify_report: VerifyReport,
) -> None:
    readme = out_root / "README.md"
    text = readme.read_text(encoding="utf-8")
    coverage_block = _render_coverage_section(verify_report)
    corpus_block = _render_corpus_section(by_cat, codex_version)
    autogen = (
        f"{AUTOGEN_START}\n\n"
        f"{coverage_block}\n"
        f"{corpus_block}\n"
        f"{AUTOGEN_END}\n"
    )

    if AUTOGEN_START in text and AUTOGEN_END in text:
        before, _, rest = text.partition(AUTOGEN_START)
        _, _, after = rest.partition(AUTOGEN_END)
        new = before + autogen + after.lstrip("\n")
    else:
        # First run — replace M1's "## Coverage" placeholder section through end of file
        if "## Coverage" in text:
            before = text.split("## Coverage", 1)[0].rstrip() + "\n\n"
            # Try to keep "## Contributing" footer if present
            footer = ""
            if "## Contributing" in text:
                footer = "## Contributing" + text.split("## Contributing", 1)[1]
            new = before + autogen + ("\n" + footer if footer else "")
        else:
            new = text.rstrip() + "\n\n" + autogen

    readme.write_text(new)


def _render_changelog_entry(
    by_cat: dict[str, list[dict]],
    codex_version: str,
    codex_commit: str,
) -> str:
    total_files = sum(len(v) for v in by_cat.values())
    total_tokens = sum(sum(f["tokens"] for f in files) for files in by_cat.values())
    out: list[str] = []
    out.append(
        f"# [{codex_version}](https://github.com/openai/codex/releases/tag/{codex_version})"
    )
    out.append("")
    out.append(f"_+{total_tokens:,} tokens_ (first extraction)")
    out.append("")
    out.append(
        f"Initial extraction baseline at codex commit `{codex_commit}`. "
        f"All {total_files} captured files are NEW (no prior mirror snapshot)."
    )
    out.append("")
    for cat in CATEGORY_ORDER:
        if cat not in by_cat or not by_cat[cat]:
            continue
        files = sorted(by_cat[cat], key=lambda f: f["filename"])
        cat_total = sum(f["tokens"] for f in files)
        out.append(f"## `prompts/{cat}/` ({len(files)} files, {cat_total:,} tokens)")
        out.append("")
        for f in files:
            short = f["description"]
            if len(short) > 160:
                short = short[:160].rstrip() + "…"
            out.append(f"- **NEW:** `{f['filename']}` (**{f['tokens']:,}** tk) — {short}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def update_changelog(
    out_root: Path,
    codex_version: str,
    codex_commit: str,
    by_cat: dict[str, list[dict]],
) -> None:
    cl = out_root / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8")
    entry = _render_changelog_entry(by_cat, codex_version, codex_commit)
    placeholder = "_Awaiting first extraction. M6 will populate the first entry._"
    if placeholder in text:
        text = text.replace(placeholder, entry, 1)
    else:
        # Insert after the intro before any existing entry.
        marker = "## Format"
        if marker in text:
            before, _, after = text.partition(marker)
            text = before + entry + "\n---\n\n" + marker + after
        else:
            text = text.rstrip() + "\n\n" + entry
    cl.write_text(text)


def run(
    out_root: Path,
    codex_version: str,
    codex_commit: str,
    verify_report: VerifyReport,
) -> IndexResult:
    by_cat = _collect(out_root)
    update_readme(out_root, codex_version, by_cat, verify_report)
    update_changelog(out_root, codex_version, codex_commit, by_cat)
    file_count = sum(len(v) for v in by_cat.values())
    total_tokens = sum(sum(f["tokens"] for f in files) for files in by_cat.values())
    return IndexResult(file_count=file_count, total_tokens=total_tokens, by_category=by_cat)
