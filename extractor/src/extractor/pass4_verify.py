"""Pass 4: verification (SPEC §2.5).

Two layers:

- **Layer A — Structural mapping**: every angle-bracket placeholder appearing
  in codex's `model_visible_layout__*.snap`, `compact*.snap`, `guardian/*.snap`
  files maps to either (a) a captured corpus file/category, (b) a runtime
  variable, (c) an out-of-scope-per-spec exclusion, or (d) an explicitly
  deferred-to-M5 programmatic prompt. Unmapped placeholders are spec bugs.

  *Note*: codex snapshots are placeholder-redacted, NOT raw-content. The v0.3
  SPEC §2.5 wording assumed line-level trace-back; v0.5 amends to structural
  mapping (the operationally feasible check given the actual snapshot format).

- **Layer B — Completeness**: every Pass 1 auto-include candidate, every
  models.json fan-out entry, and every Pass 1.5 allow-list entry must produce
  ≥1 captured file in `prompts/`.

Plus auxiliary checks:

- **Token-count drift**: recorded `tokens.o200k_base` matches recomputed.
- **Frontmatter schema**: every captured file has the §3.3 required fields.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import pass1_5_allowlist, pass1_autoinclude, pass1_models, pass2_denylist
from .tokens import count_o200k_base

# Map snapshot placeholder name → expected corpus presence.
# Values:
#   "<path>"            — a path under <out_root> that must exist (file or non-empty dir)
#   "runtime_variable"  — runtime-injected (e.g. cwd, current time)
#   "runtime_generated" — runtime-produced (e.g. compaction summary)
#   "runtime_content"   — runtime user content (e.g. image attachments)
#   "out_of_scope"      — explicitly excluded per SPEC §10.4 etc.
#   "deferred_m5"       — programmatic prompt, captured at M5 via shim
PLACEHOLDER_MAP: dict[str, str] = {
    # Captured at M2/M3 (static)
    "PERMISSIONS_INSTRUCTIONS": "prompts/permission/",
    "SUMMARIZATION_PROMPT": "prompts/mode/mode-compact-prompt.md",
    # Out-of-scope per SPEC §10.4 (skills are project-local, not built-in)
    "SKILLS_INSTRUCTIONS": "out_of_scope",
    # Runtime-injected
    "CWD": "runtime_variable",
    "COMPACTION_SUMMARY": "runtime_generated",
    "image": "runtime_content",
    "input_image": "runtime_content",
    # Captured at M5b via Pass 1.6 ContextualUserFragment auto-discovery.
    # Each placeholder ↔ a context-fragment file derived from the impl block's struct name.
    "ENVIRONMENT_CONTEXT": "prompts/context-fragment/context-fragment-environment-context.md",
    "personality_spec": "prompts/context-fragment/context-fragment-personality-spec-instructions.md",
    "model_switch": "prompts/context-fragment/context-fragment-model-switch-instructions.md",
    "realtime_conversation": "prompts/context-fragment/context-fragment-realtime-start-instructions.md",
    "collaboration_mode": "prompts/context-fragment/context-fragment-collaboration-mode-instructions.md",
}

# Matches angle-bracket placeholders. Captures placeholder name (before `:`).
PLACEHOLDER_RX = re.compile(r"<([a-zA-Z_][a-zA-Z_0-9]*)(?::[^>]*)?>")

# Frontmatter schema (per SPEC §3.3) — required top-level keys.
REQUIRED_FIELDS = {
    "name",
    "category",
    "codex_version",
    "codex_commit",
    "source",
    "extraction",
    "variables",
    "tokens",
    "description",
}


@dataclass
class VerifyReport:
    # Layer A — placeholder mapping
    snapshot_files: int = 0
    placeholders_seen: dict[str, int] = field(default_factory=dict)
    placeholders_unmapped: list[str] = field(default_factory=list)
    placeholders_deferred_m5: list[str] = field(default_factory=list)
    placeholders_static_missing: list[tuple[str, str]] = field(default_factory=list)
    placeholders_runtime: list[str] = field(default_factory=list)
    placeholders_out_of_scope: list[str] = field(default_factory=list)
    placeholders_static_ok: list[tuple[str, str]] = field(default_factory=list)

    # Layer B — completeness
    autoinclude_count: int = 0
    autoinclude_missing: list[Path] = field(default_factory=list)
    models_count: int = 0
    models_missing: list[str] = field(default_factory=list)
    allowlist_count: int = 0
    allowlist_missing: list[tuple[str, str]] = field(default_factory=list)  # (symbol_or_marker, expected_path)

    # Token drift
    token_check_count: int = 0
    token_drift: list[tuple[Path, int, int]] = field(default_factory=list)

    # Frontmatter schema
    frontmatter_check_count: int = 0
    frontmatter_invalid: list[tuple[Path, str]] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not (
            self.placeholders_unmapped
            or self.placeholders_static_missing
            or self.autoinclude_missing
            or self.models_missing
            or self.allowlist_missing
            or self.token_drift
            or self.frontmatter_invalid
        )


def find_snapshots(codex_rs: Path) -> list[Path]:
    """Find the snapshot files used by Layer A verification (SPEC §2.5)."""
    paths: list[Path] = []
    suite = codex_rs / "core" / "tests" / "suite" / "snapshots"
    if suite.is_dir():
        for pat in ("*model_visible_layout*.snap", "*compact*.snap"):
            paths.extend(sorted(suite.glob(pat)))
    guardian = codex_rs / "core" / "src" / "guardian" / "snapshots"
    if guardian.is_dir():
        paths.extend(sorted(guardian.glob("*.snap")))
    return paths


def extract_placeholders(snap_text: str) -> set[str]:
    """Extract angle-bracket placeholder names from a snapshot's body (post-frontmatter)."""
    parts = snap_text.split("---\n", 2)
    body = parts[2] if len(parts) >= 3 else snap_text
    return set(PLACEHOLDER_RX.findall(body))


def _parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, None
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return None, None
    try:
        fm = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None, None
    body = text[end + 5 :]
    return fm, body


def _captured_source_paths(out_root: Path) -> set[Path]:
    """Collect every source.path recorded in captured frontmatters, relative to codex-rs."""
    out: set[Path] = set()
    for md in (out_root / "prompts").rglob("*.md"):
        if md.name == ".gitkeep":
            continue
        text = md.read_text(encoding="utf-8")
        fm, _ = _parse_frontmatter(text)
        if not fm:
            continue
        sp = fm.get("source", {}).get("path", "")
        if isinstance(sp, str) and sp.startswith("codex-rs/"):
            out.add(Path(sp[len("codex-rs/") :]))
    return out


def verify(codex_root: Path, out_root: Path, extractor_dir: Path) -> VerifyReport:
    codex_rs = codex_root / "codex-rs"
    report = VerifyReport()

    # ============ Layer A — Structural mapping ============
    snapshots = find_snapshots(codex_rs)
    report.snapshot_files = len(snapshots)
    all_placeholders: set[str] = set()
    for snap in snapshots:
        try:
            text = snap.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for p in extract_placeholders(text):
            all_placeholders.add(p)
            report.placeholders_seen[p] = report.placeholders_seen.get(p, 0) + 1

    for ph in sorted(all_placeholders):
        target = PLACEHOLDER_MAP.get(ph)
        if target is None:
            report.placeholders_unmapped.append(ph)
            continue
        if target == "deferred_m5":
            report.placeholders_deferred_m5.append(ph)
            continue
        if target.startswith("runtime_"):
            report.placeholders_runtime.append(ph)
            continue
        if target == "out_of_scope":
            report.placeholders_out_of_scope.append(ph)
            continue
        # target is a path under out_root
        full = out_root / target
        ok = False
        if full.is_file():
            ok = True
        elif full.is_dir():
            ok = any(f.name != ".gitkeep" for f in full.glob("*.md"))
        if ok:
            report.placeholders_static_ok.append((ph, target))
        else:
            report.placeholders_static_missing.append((ph, target))

    # ============ Layer B — Completeness ============
    candidates = pass1_autoinclude.walk(codex_rs)
    denylist = pass2_denylist.load(extractor_dir)
    kept, _ = pass2_denylist.filter_candidates(candidates, denylist)

    expected_paths: set[Path] = set()
    seen_targets: set[Path] = set()
    for c in kept:
        if c.target_path in seen_targets:
            continue
        seen_targets.add(c.target_path)
        expected_paths.add(c.target_rel)
    report.autoinclude_count = len(expected_paths)

    captured_sources = _captured_source_paths(out_root)
    for rel in sorted(expected_paths, key=str):
        if rel in captured_sources:
            continue
        # Empty source files (e.g. agent/builtins/explorer.toml) are legitimately skipped
        full = codex_rs / rel
        if full.is_file() and not full.read_text(encoding="utf-8").strip():
            continue
        report.autoinclude_missing.append(rel)

    # Models fan-out
    model_entries = pass1_models.fan_out(codex_rs)
    report.models_count = len(model_entries)
    bi_dir = out_root / "prompts" / "base-instructions"
    for me in model_entries:
        slug_safe = me.slug.replace("/", "-").replace(" ", "-")
        expected_file = bi_dir / f"base-instructions-{slug_safe}.md"
        if not expected_file.exists():
            report.models_missing.append(me.slug)

    # Allow-list — per-entry completeness (M5a)
    allow_entries = pass1_5_allowlist.load(extractor_dir)
    report.allowlist_count = len(allow_entries)
    for entry in allow_entries:
        category = entry.get("category", "")
        filename = entry.get("filename", "")
        expected_path = out_root / "prompts" / category / f"{filename}.md"
        if not expected_path.exists():
            ident = entry.get("symbol") or entry.get("marker") or "?"
            report.allowlist_missing.append(
                (ident, str(expected_path.relative_to(out_root)))
            )

    # ============ Token-drift check ============
    for md in (out_root / "prompts").rglob("*.md"):
        if md.name == ".gitkeep":
            continue
        text = md.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)
        if not fm:
            continue
        recorded = fm.get("tokens", {}).get("o200k_base")
        if recorded is None or body is None:
            continue
        report.token_check_count += 1
        recomputed = count_o200k_base(body)
        if recomputed != recorded:
            report.token_drift.append(
                (md.relative_to(out_root), recorded, recomputed)
            )

    # ============ Frontmatter schema check ============
    for md in (out_root / "prompts").rglob("*.md"):
        if md.name == ".gitkeep":
            continue
        text = md.read_text(encoding="utf-8")
        fm, _ = _parse_frontmatter(text)
        if fm is None:
            report.frontmatter_invalid.append((md.relative_to(out_root), "missing or unparseable frontmatter"))
            continue
        if not isinstance(fm, dict):
            report.frontmatter_invalid.append((md.relative_to(out_root), "frontmatter is not a YAML mapping"))
            continue
        report.frontmatter_check_count += 1
        missing = REQUIRED_FIELDS - set(fm.keys())
        if missing:
            report.frontmatter_invalid.append(
                (md.relative_to(out_root), f"missing fields: {sorted(missing)}")
            )

    return report
