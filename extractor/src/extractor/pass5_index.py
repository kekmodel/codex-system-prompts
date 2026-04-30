"""Pass 5: README + CHANGELOG generation (SPEC §3.4, §3.5)."""

from __future__ import annotations

import collections
import hashlib
import re
import subprocess
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


# ---------------------------------------------------------------------------
# Frontmatter / file-tree collection (current + at-prior-commit)
# ---------------------------------------------------------------------------


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter (--- ... ---) from body. Returns (fm, body)."""
    if not text.startswith("---\n"):
        return {}, text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}, text
    try:
        fm = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        fm = {}
    body = text[end + len("\n---\n"):]
    return fm, body


def _record_from_text(text: str, rel_path: str) -> dict | None:
    """Extract the per-file record we need for both README + CHANGELOG."""
    fm, body = _split_frontmatter(text)
    if not fm:
        return None
    cat = fm.get("category", "uncategorized")
    tokens = fm.get("tokens", {}).get("o200k_base", 0)
    desc = (fm.get("description") or "").replace("\n", " ").strip()
    if len(desc) > 240:
        desc = desc[:240].rstrip() + "…"
    return {
        "path": rel_path,
        "filename": Path(rel_path).name,
        "category": cat,
        "tokens": tokens,
        "description": desc,
        "name": fm.get("name", ""),
        "body_hash": hashlib.sha256(body.encode("utf-8")).hexdigest(),
    }


def _collect(out_root: Path) -> dict[str, list[dict]]:
    """Walk current prompts/ and group records by category."""
    by_cat: dict[str, list[dict]] = collections.defaultdict(list)
    for md in (out_root / "prompts").rglob("*.md"):
        if md.name == ".gitkeep":
            continue
        rec = _record_from_text(
            md.read_text(encoding="utf-8"),
            str(md.relative_to(out_root)),
        )
        if rec is not None:
            by_cat[rec["category"]].append(rec)
    return by_cat


def _by_filename(by_cat: dict[str, list[dict]]) -> dict[str, dict]:
    """Flatten {cat: [recs]} → {filename: rec} for diffing."""
    out: dict[str, dict] = {}
    for recs in by_cat.values():
        for r in recs:
            out[r["filename"]] = r
    return out


def _git(out_root: Path, *args: str) -> str:
    """Run a git command in out_root; return stdout, raise on nonzero."""
    result = subprocess.run(
        ["git", "-C", str(out_root), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def _git_safe(out_root: Path, *args: str) -> str | None:
    """Run a git command; return stdout on success, None on any failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(out_root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def _previous_mirror_tag(out_root: Path, current_tag: str) -> str | None:
    """
    Most recent mirror tag prior to current_tag, by creator-date.

    Returns the tag *string* (e.g. "rust-v0.126.0-alpha.12"), or None for
    the baseline case (no prior tag).
    """
    out = _git_safe(out_root, "tag", "--sort=-creatordate")
    if out is None:
        return None
    for t in out.splitlines():
        if t.startswith("rust-v") and t != current_tag:
            return t
    return None


def _collect_at_commit_or_tag(out_root: Path, ref: str) -> dict[str, dict]:
    """
    Read prompts/*.md tree at the given git ref via `git ls-tree` + `git show`.

    Files without parseable frontmatter are silently skipped, matching the
    behavior of _collect() for the live working tree.
    """
    out = _git_safe(out_root, "ls-tree", "-r", "--name-only", ref, "--", "prompts/")
    if out is None:
        return {}
    by_filename: dict[str, dict] = {}
    for path in out.splitlines():
        if not path.endswith(".md") or path.endswith(".gitkeep"):
            continue
        text = _git_safe(out_root, "show", f"{ref}:{path}")
        if text is None:
            continue
        rec = _record_from_text(text, path)
        if rec is not None:
            by_filename[rec["filename"]] = rec
    return by_filename


# ---------------------------------------------------------------------------
# Diff classification (SPEC §3.5)
# ---------------------------------------------------------------------------


@dataclass
class ChangelogDiff:
    new: list[dict]                                # records from curr
    modified: list[dict]                           # {filename, category, delta, prev_tokens, curr_tokens, description}
    moved: list[dict]                              # {old_path, new_path, category, tokens}
    removed: list[dict]                            # records from prev

    def net_token_delta(self) -> int:
        net = sum(r["tokens"] for r in self.new)
        net += sum(r["delta"] for r in self.modified)
        net -= sum(r["tokens"] for r in self.removed)
        return net

    def has_changes(self) -> bool:
        return bool(self.new or self.modified or self.moved or self.removed)


def _classify_diff(prev: dict[str, dict], curr: dict[str, dict]) -> ChangelogDiff:
    prev_names = set(prev.keys())
    curr_names = set(curr.keys())

    only_curr = curr_names - prev_names
    only_prev = prev_names - curr_names
    common = prev_names & curr_names

    # MOVED = body-identical file under a different filename.
    # Match only between only_curr and only_prev (a rename, not an in-place edit).
    prev_unmatched_by_hash: dict[str, str] = {}
    for name in only_prev:
        prev_unmatched_by_hash.setdefault(prev[name]["body_hash"], name)

    moved: list[dict] = []
    truly_new_names: list[str] = []
    matched_prev: set[str] = set()
    for name in sorted(only_curr):
        h = curr[name]["body_hash"]
        old_name = prev_unmatched_by_hash.get(h)
        if old_name and old_name not in matched_prev:
            matched_prev.add(old_name)
            moved.append(
                {
                    "old_path": prev[old_name]["path"],
                    "new_path": curr[name]["path"],
                    "category": curr[name]["category"],
                    "tokens": curr[name]["tokens"],
                }
            )
        else:
            truly_new_names.append(name)

    truly_removed = [prev[n] for n in sorted(only_prev) if n not in matched_prev]
    truly_new = [curr[n] for n in truly_new_names]

    modified: list[dict] = []
    for name in sorted(common):
        if prev[name]["body_hash"] != curr[name]["body_hash"]:
            modified.append(
                {
                    "filename": name,
                    "path": curr[name]["path"],
                    "category": curr[name]["category"],
                    "prev_tokens": prev[name]["tokens"],
                    "curr_tokens": curr[name]["tokens"],
                    "delta": curr[name]["tokens"] - prev[name]["tokens"],
                    "description": curr[name]["description"],
                }
            )

    return ChangelogDiff(
        new=truly_new, modified=modified, moved=moved, removed=truly_removed
    )


# ---------------------------------------------------------------------------
# README rendering (unchanged; current-state snapshot)
# ---------------------------------------------------------------------------


def _render_corpus_section(
    by_cat: dict[str, list[dict]], codex_version: str
) -> str:
    total_files = sum(len(v) for v in by_cat.values())
    total_tokens = sum(sum(f["tokens"] for f in files) for files in by_cat.values())
    out: list[str] = []
    out.append(AUTOGEN_START)
    out.append(
        f"_Auto-generated by `extractor pass5` (M6) at codex `{codex_version}`._"
    )
    out.append("")
    out.append(f"**{total_files} captured files** across {len([c for c in CATEGORY_ORDER if by_cat.get(c)])} categories — ")
    out.append(
        f"**{total_tokens:,} tokens** (o200k_base, template counts — "
        "runtime values are placeholder-redacted, see SPEC §2.5 Layer A)."
    )
    out.append("")

    for cat in CATEGORY_ORDER:
        if cat not in by_cat or not by_cat[cat]:
            continue
        files = sorted(by_cat[cat], key=lambda f: f["filename"])
        cat_total = sum(f["tokens"] for f in files)
        out.append(f"### `prompts/{cat}/` — {len(files)} files, {cat_total:,} tokens")
        out.append("")
        out.append(CATEGORY_DESCRIPTIONS.get(cat, ""))
        out.append("")
        out.append("| File | Tokens | Description |")
        out.append("|---|---:|---|")
        for f in files:
            out.append(
                f"| [`{f['filename']}`](./{f['path']}) | **{f['tokens']:,}** | {f['description']} |"
            )
        out.append("")
    out.append(AUTOGEN_END)
    return "\n".join(out)


def _render_coverage_section(verify_report: VerifyReport) -> str:
    out: list[str] = []
    out.append(AUTOGEN_START)
    out.append("_Layer A (placeholder mapping) + Layer B (completeness) coverage report._")
    out.append("")
    if verify_report.passed:
        out.append("✅ **Pass 4 verification: PASSED**")
    else:
        out.append("❌ **Pass 4 verification: FAILED**")
    out.append("")
    out.append(
        f"- Layer A unmapped placeholders: **{len(verify_report.placeholders_unmapped)}**"
    )
    out.append(
        f"- Layer B autoinclude misses:    **{len(verify_report.autoinclude_missing)}**"
    )
    out.append(
        f"- Layer B model-fanout misses:   **{len(verify_report.models_missing)}**"
    )
    out.append(
        f"- Layer B allow-list misses:     **{len(verify_report.allowlist_missing)}**"
    )
    out.append(
        f"- Frontmatter schema fails:      **{len(verify_report.frontmatter_invalid)}**"
    )
    out.append(
        f"- Token-count drifts:            **{len(verify_report.token_drift)}**"
    )
    out.append(AUTOGEN_END)
    return "\n".join(out)


def update_readme(
    out_root: Path,
    codex_version: str,
    by_cat: dict[str, list[dict]],
    verify_report: VerifyReport,
) -> None:
    readme = out_root / "README.md"
    text = readme.read_text(encoding="utf-8")

    corpus = _render_corpus_section(by_cat, codex_version)
    coverage = _render_coverage_section(verify_report)

    text = _replace_block(text, "## Captured corpus (auto-generated)", corpus)
    text = _replace_block(text, "## Coverage (auto-generated)", coverage)
    readme.write_text(text)


def _replace_block(text: str, header: str, body: str) -> str:
    """Replace the AUTOGEN block under `header`, or insert it if missing."""
    if header not in text:
        return text.rstrip() + "\n\n" + header + "\n\n" + body + "\n"
    head_idx = text.index(header)
    tail = text[head_idx + len(header):]
    start = tail.find(AUTOGEN_START)
    end = tail.find(AUTOGEN_END)
    if start == -1 or end == -1 or end < start:
        # No existing block; insert one after the header.
        before = text[: head_idx + len(header)]
        after = tail
        return before + "\n\n" + body + "\n" + after
    abs_start = head_idx + len(header) + start
    abs_end = head_idx + len(header) + end + len(AUTOGEN_END)
    return text[:abs_start] + body + text[abs_end:]


# ---------------------------------------------------------------------------
# CHANGELOG rendering (SPEC §3.5)
# ---------------------------------------------------------------------------


def _changelog_header(codex_version: str, net_delta: int, header_suffix: str) -> list[str]:
    sign = "+" if net_delta >= 0 else "−"
    abs_delta = abs(net_delta)
    out = [
        f"# [{codex_version}](https://github.com/openai/codex/releases/tag/{codex_version})",
        "",
        f"_{sign}{abs_delta:,} tokens_{header_suffix}",
        "",
    ]
    return out


def _spans_line(skipped_predecessors: list[str] | None, current_tag: str) -> str | None:
    """SPEC §3.5: 'Spans upstream rust-vA..B; no prompt change in intermediate.'"""
    if not skipped_predecessors:
        return None
    if len(skipped_predecessors) == 1:
        return (
            f"Spans upstream `{skipped_predecessors[0]}`..`{current_tag}`; "
            f"no prompt change in `{skipped_predecessors[0]}`."
        )
    first, last = skipped_predecessors[0], skipped_predecessors[-1]
    return (
        f"Spans upstream `{first}`..`{current_tag}`; "
        f"no prompt change in `{first}`..`{last}` ({len(skipped_predecessors)} intermediate tags)."
    )


def _category_buckets(
    diff: ChangelogDiff,
) -> dict[str, dict[str, list]]:
    """Group each diff axis by category for emission."""
    buckets: dict[str, dict[str, list]] = collections.defaultdict(
        lambda: {"new": [], "modified": [], "moved": [], "removed": []}
    )
    for r in diff.new:
        buckets[r["category"]]["new"].append(r)
    for r in diff.modified:
        buckets[r["category"]]["modified"].append(r)
    for r in diff.moved:
        buckets[r["category"]]["moved"].append(r)
    for r in diff.removed:
        buckets[r["category"]]["removed"].append(r)
    return buckets


def _render_changelog_entry_incremental(
    diff: ChangelogDiff,
    codex_version: str,
    codex_commit: str,
    prev_tag: str,
    skipped_predecessors: list[str] | None = None,
) -> str:
    out = _changelog_header(codex_version, diff.net_token_delta(), header_suffix="")
    out.append(
        f"Diff vs. previous mirror tag `{prev_tag}` at codex commit `{codex_commit}`. "
        f"NEW: {len(diff.new)}, MODIFIED: {len(diff.modified)}, "
        f"MOVED: {len(diff.moved)}, REMOVED: {len(diff.removed)}."
    )
    out.append("")
    spans = _spans_line(skipped_predecessors, codex_version)
    if spans:
        out.append(spans)
        out.append("")

    buckets = _category_buckets(diff)
    for cat in CATEGORY_ORDER:
        bucket = buckets.get(cat)
        if not bucket or not any(bucket.values()):
            continue
        out.append(f"## `prompts/{cat}/`")
        out.append("")
        for r in sorted(bucket["new"], key=lambda x: x["filename"]):
            short = r["description"]
            if len(short) > 160:
                short = short[:160].rstrip() + "…"
            out.append(f"- **NEW:** `{r['filename']}` (**{r['tokens']:,}** tk) — {short}")
        for r in sorted(bucket["modified"], key=lambda x: x["filename"]):
            sign = "+" if r["delta"] >= 0 else "−"
            out.append(
                f"- `{r['filename']}` — token Δ {sign}{abs(r['delta']):,} "
                f"({r['prev_tokens']:,} → {r['curr_tokens']:,})."
            )
        for r in sorted(bucket["moved"], key=lambda x: x["new_path"]):
            out.append(
                f"- **MOVED:** `{r['old_path']}` → `{r['new_path']}` "
                f"(body unchanged; **{r['tokens']:,}** tk)."
            )
        for r in sorted(bucket["removed"], key=lambda x: x["filename"]):
            out.append(
                f"- **REMOVED:** `{r['filename']}` "
                f"(was **{r['tokens']:,}** tk) — no longer present in upstream."
            )
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _render_changelog_entry_baseline(
    by_cat: dict[str, list[dict]],
    codex_version: str,
    codex_commit: str,
) -> str:
    total_files = sum(len(v) for v in by_cat.values())
    total_tokens = sum(sum(f["tokens"] for f in files) for files in by_cat.values())
    out = _changelog_header(codex_version, total_tokens, header_suffix=" (first extraction)")
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


_FIRST_ENTRY_RX = re.compile(r"^# \[rust-v[^\]]+\]", re.MULTILINE)
_FORMAT_MARKER = "## Format"
_PLACEHOLDER = "_Awaiting first extraction. M6 will populate the first entry._"


def _strip_existing_top_entry(text: str, codex_version: str) -> str:
    """
    If the topmost `# [rust-v...]` entry is for codex_version, strip it out
    (along with its trailing `---` separator). Lets re-extraction at the
    same tag overwrite its previous entry instead of accumulating duplicates.
    """
    first = _FIRST_ENTRY_RX.search(text)
    if not first:
        return text
    header_line_end = text.find("\n", first.start())
    header_line = text[first.start():header_line_end] if header_line_end != -1 else text[first.start():]
    if f"[{codex_version}]" not in header_line:
        return text

    # Find the end of this entry: the next `# [rust-v...]` header or `## Format`
    # marker. Include the `---\n\n` separator that sits between this entry and
    # the next one so we don't leave a stray separator behind.
    next_entry = _FIRST_ENTRY_RX.search(text, pos=first.end())
    fmt_idx = text.find(_FORMAT_MARKER, first.end())
    candidates = [c for c in (next_entry.start() if next_entry else -1, fmt_idx) if c != -1]
    cut_end = min(candidates) if candidates else len(text)
    return text[:first.start()] + text[cut_end:]


def _insert_changelog_entry(text: str, codex_version: str, entry: str) -> str:
    """
    Idempotent prepend: if a previous entry for the same `codex_version` is
    already at the top, strip it first (re-extraction overwrites itself).
    Then insert `entry` so it becomes the newest top entry.

    Insertion priority for the prepend step:
      1. If the M1 placeholder is still present, replace it (baseline).
      2. Else, insert immediately before the first existing `# [rust-v...]` entry.
      3. Else (no entries yet, no placeholder), insert before `## Format`.
      4. Else, append to file end.
    """
    text = _strip_existing_top_entry(text, codex_version)

    if _PLACEHOLDER in text:
        return text.replace(_PLACEHOLDER, entry, 1)

    m = _FIRST_ENTRY_RX.search(text)
    if m:
        idx = m.start()
        return text[:idx] + entry + "\n---\n\n" + text[idx:]

    if _FORMAT_MARKER in text:
        before, _, after = text.partition(_FORMAT_MARKER)
        return before + entry + "\n---\n\n" + _FORMAT_MARKER + after

    return text.rstrip() + "\n\n" + entry


def update_changelog(
    out_root: Path,
    codex_version: str,
    codex_commit: str,
    by_cat: dict[str, list[dict]],
    skipped_predecessors: list[str] | None = None,
) -> None:
    """
    Render either an incremental (NEW/MODIFIED/MOVED/REMOVED) or baseline
    entry depending on whether a prior mirror tag exists, then prepend it
    so the newest entry is always at the top.
    """
    cl = out_root / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8")

    prev_tag = _previous_mirror_tag(out_root, codex_version)
    if prev_tag is None:
        entry = _render_changelog_entry_baseline(by_cat, codex_version, codex_commit)
    else:
        prev = _collect_at_commit_or_tag(out_root, prev_tag)
        curr = _by_filename(by_cat)
        diff = _classify_diff(prev, curr)
        if not diff.has_changes():
            # No captured-prompt diff vs. previous tag. Per SPEC §3.5 selective
            # tagging, we record nothing — the auto-mirror workflow is expected
            # to skip this tag (it just won't produce a commit).
            return
        entry = _render_changelog_entry_incremental(
            diff,
            codex_version=codex_version,
            codex_commit=codex_commit,
            prev_tag=prev_tag,
            skipped_predecessors=skipped_predecessors,
        )

    text = _insert_changelog_entry(text, codex_version, entry)
    cl.write_text(text)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def run(
    out_root: Path,
    codex_version: str,
    codex_commit: str,
    verify_report: VerifyReport,
    skipped_predecessors: list[str] | None = None,
) -> IndexResult:
    by_cat = _collect(out_root)
    update_readme(out_root, codex_version, by_cat, verify_report)
    update_changelog(
        out_root, codex_version, codex_commit, by_cat,
        skipped_predecessors=skipped_predecessors,
    )
    file_count = sum(len(v) for v in by_cat.values())
    total_tokens = sum(sum(f["tokens"] for f in files) for files in by_cat.values())
    return IndexResult(file_count=file_count, total_tokens=total_tokens, by_category=by_cat)
