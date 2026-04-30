# Upstream tag registry

Per [SPEC §12.3](../SPEC.md#123-per-version-management-structure-piebald-style-v03-selective--t24), this file is the **lossless record** of every upstream `rust-v*` tag and its mirror status. It exists because the mirror's own git tags are a *sparse subset* — only material-prompt-diff tags get mirrored — so we need a separate registry to preserve the full upstream history.

This table is hand-maintained for now: the M8 baseline row was seeded by hand, and each auto-mirror PR opened by `.github/workflows/extract.yml` is expected to append its own row in the same commit (the workflow does not yet write this file automatically — wiring upstream-tag-row append into Pass 5 is a tracked post-M8 enhancement).

## Status legend

| Status | Meaning |
|---|---|
| `extracted` | Material prompt diff vs. previous extracted tag; mirror commit + mirror tag created |
| `skipped_no_prompt_diff` | Upstream tag had no captured-prompt diff; no mirror commit |
| `skipped_other` | Upstream tag intentionally not processed (build failure, extractor incompatibility, etc.); see Note |

## Registry

| Upstream tag | Date (UTC) | Status | Mirror commit | Note |
|---|---|---|---|---|
| `rust-v0.126.0-alpha.12` | 2026-04-29 | `extracted` | (M8 baseline; mirror tag `rust-v0.126.0-alpha.12`) | Initial extraction baseline. Codex commit `ebdf3a878c8c7253504599bd384cd421a4e548c1`. All 91 captured files are NEW. Earlier upstream tags (`rust-v0.24.0-alpha.9`..`rust-v0.126.0-alpha.11`) are not backfilled per SPEC §13.6 (deferred post-M8 task). |

> **Forward updates**: rows for `rust-v0.126.0-alpha.13` and later are added in the auto-mirror PR for each upstream tag. Non-material tags get a `skipped_no_prompt_diff` row and no mirror commit (per §3.5 selective tagging). Today this row is added by hand to the auto-mirror PR before merge; auto-append is a post-M8 enhancement.
