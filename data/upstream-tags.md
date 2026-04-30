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
| `rust-v0.126.0-alpha.13` | 2026-05-01 | `skipped_other` | — | Rolled up into `rust-v0.128.0-alpha.1` mirror commit (#2). The pre-§6.1-fix `extract.yml` jumped straight from upstream's latest to upstream's newest material tag without iterating intermediates, so we never extracted against this tag and don't know whether its captured-prompt diff was material. Recorded for historical lossless-mapping completeness; cannot be backfilled without rolling `main` back. |
| `rust-v0.126.0-alpha.14` | 2026-05-01 | `skipped_other` | — | Same as `rust-v0.126.0-alpha.13`. |
| `rust-v0.126.0-alpha.15` | 2026-05-01 | `skipped_other` | — | Same as `rust-v0.126.0-alpha.13`. |
| `rust-v0.126.0-alpha.16` | 2026-05-01 | `skipped_other` | — | Same as `rust-v0.126.0-alpha.13`. |
| `rust-v0.126.0-alpha.17` | 2026-05-01 | `skipped_other` | — | Same as `rust-v0.126.0-alpha.13`. |
| `rust-v0.127.0` | 2026-05-01 | `skipped_other` | — | Same as `rust-v0.126.0-alpha.13`. (First stable upstream tag; rolled up rather than mirrored because of the same workflow defect.) |
| `rust-v0.128.0-alpha.1` | 2026-05-01 | `extracted` | `e02dafd` (PR #2); retagged to `912b3ab` (post-PR #12) on 2026-05-01 | Second material extraction. 93 files changed (+408 / −273) vs. `rust-v0.126.0-alpha.12`. Diff conflates real prompt changes from alpha.12→alpha.1 with any unmirrored intermediate changes; the SPEC §6.1 multi-tag iteration fix (tracked as a future PR) prevents this in future runs. Mirror tag `rust-v0.128.0-alpha.1` was created by hand because `extract.yml` lacked a tagging step (added by `tag-on-merge.yml` in this PR). Force-retagged to main HEAD after PR #12 (fn_call ToolSpec resolution) so the next mirror baseline reflects the latest extractor output — without this, every extractor improvement merged between mirror tags would surface as a phantom NEW/MODIFIED in the next upstream tag's CHANGELOG entry. |
| `rust-v0.128.0` | 2026-05-01 | `skipped_no_prompt_diff` | — | Codex source diff vs. `rust-v0.128.0-alpha.1` is Cargo.toml only; no prompt-content change. Per SPEC §3.5/§6.1 selective tagging, no mirror commit and no mirror tag. |

> **Forward updates**: rows for `rust-v0.126.0-alpha.13` and later are added in the auto-mirror PR for each upstream tag. Non-material tags get a `skipped_no_prompt_diff` row and no mirror commit (per §3.5 selective tagging). Today this row is added by hand to the auto-mirror PR before merge; auto-append is a post-M8 enhancement.
