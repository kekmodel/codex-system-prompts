# codex-system-prompts

> **STATUS: M1 skeleton — extraction not yet performed.**
> First extraction targets upstream Codex tag `rust-v0.126.0-alpha.12`.
> Track progress in [SPEC.md §11](./SPEC.md) (Implementation roadmap).

Unofficial, version-tracked mirror of the prompt strings shipped by OpenAI's [Codex CLI](https://github.com/openai/codex). See [DISCLAIMER.md](./DISCLAIMER.md) for legal context and [SPEC.md](./SPEC.md) for the full specification.

Modeled on Piebald AI's [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) philosophy, adapted to Codex's hybrid prompt architecture.

## Layout

| Path | Purpose |
|---|---|
| `prompts/` | Extracted prompt files, by category (populated at M5) |
| `prompts/feature-gated/<flag>/` | Non-default-feature prompts (per SPEC §2.1.1) |
| `extractor/` | Extraction tooling — Python orchestrator + Rust shim |
| `data/upstream-tags.md` | Upstream→mirror tag mapping (lossless, including skipped tags) |
| `tests/snapshot-cross-check/` | Snapshot-based verification (SPEC §2.5) |
| `SPEC.md` | Specification (v0.3 current) |
| `SPEC_REVIEW_v0.2.md` | Review history that drove v0.3 hardening |
| `CHANGELOG.md` | Per-mirror-tag prompt diffs, Piebald-style (populated at M6) |

## How updates happen

Per [SPEC §8](./SPEC.md#8-automation), two equivalent paths trigger re-extraction on a new upstream `rust-v*` tag, both sharing the same deterministic extractor entry:

- **Manual (Claude-driven)** — ask Claude in this repo: *"Codex 최신 버전으로 업데이트해."* Claude runs the extractor in dry-run, presents a paginated summary, and on approval commits + (selectively) tags.
- **Automated (GH Action)** — hourly poll of upstream tags, opens auto-PR for human merge.

## Versioning model

- Mirror tags are a **sparse subset** of upstream tags — only tags with material prompt diff get a mirror commit + tag (SPEC §12.3 / T2.4).
- The complete upstream tag history (including silent skips) lives in [`data/upstream-tags.md`](./data/upstream-tags.md).
- Working tree is always at the latest extracted tag; historical inspection via `git checkout <tag>`.

## Coverage

(Populated at M6 after first extraction.)

- **Accuracy**: % of `model_visible_layout__*.snap` lines traced (SPEC §2.5 Layer A).
- **Completeness**: % of allow-list + auto-include entries captured (SPEC §2.5 Layer B).

> Neither metric proves "all shipping prompts captured." Layer A only validates prompts exercised by upstream tests; Layer B is bounded by allow-list curation. See SPEC §2.5.

## Token-count caveat

For variable-bearing prompts (most of Codex's content), README index shows *template* token counts (placeholders intact). Real session tokens can be **2–5× higher** when variables expand (e.g., personality slot ~100 tokens, AGENTS.md content can be thousands). For programmatic prompts, both `tokens.template_*` and `tokens.rendered_*` are shown side-by-side. See [SPEC §7](./SPEC.md#7-token-accounting-v03-reframed--t23).

## Contributing

The mirror is auto-generated. Manual edits to `prompts/**/*.md` will be overwritten on next extraction. To change the *spec* (categorization, frontmatter, extractor logic), edit `SPEC.md` and the `extractor/` tooling.
