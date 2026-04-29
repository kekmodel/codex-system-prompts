# codex-system-prompts CHANGELOG

> Per-mirror-tag prompt diffs, newest first. Format mirrors Piebald's [`claude-code-system-prompts/CHANGELOG.md`](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/CHANGELOG.md). See [SPEC §3.5](./SPEC.md#35-changelog-strategy).

_Awaiting first extraction. M6 will populate the first entry._

---

## Format

```markdown
# [rust-vX.Y.Z[-alpha.N]](https://github.com/openai/codex/releases/tag/rust-vX.Y.Z[-alpha.N])

_+/-N tokens_

- **NEW:** Category: name — `prompts/<category>/<file>.md`. (entirely new prompt files)
- Category: name — Token Δ +N. (modification — always include token Δ inline)
- **MOVED:** `old/path.md` → `new/path.md` (relocations; preserve token Δ if body unchanged)
- **REMOVED:** `prompts/<category>/<file>.md` — reason. (deletions)
```

When upstream tags are silently skipped (no prompt diff), the next material entry's header opens with `Spans upstream rust-vA..B; no prompt change in intermediate.` See SPEC §3.5 (T2.4).

The complete upstream tag log (including silent skips) is at [`data/upstream-tags.md`](./data/upstream-tags.md).
