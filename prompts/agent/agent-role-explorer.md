---
name: 'Agent: agent-role-explorer'
category: agent
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/agent/role.rs
  kind: rust_inline
  reached_from:
  - core/src/agent/role.rs:368
  marker: '"explorer".to_string(),'
extraction:
  pass: 1.5
  method: rust_inline_at_marker
variables: []
tokens:
  o200k_base: 188
description: '`codex-rs/core/src/agent/role.rs`'
---
Use `explorer` for specific codebase questions.
Explorers are fast and authoritative.
They must be used to ask specific, well-scoped questions on the codebase.
Rules:
- In order to avoid redundant work, you should avoid exploring the same problem that explorers have already covered. Typically, you should trust the explorer results without additional verification. You are still allowed to inspect the code yourself to gain the needed context!
- You are encouraged to spawn up multiple explorers in parallel when you have multiple distinct questions to ask about the codebase that can be answered independently. This allows you to get more information faster without waiting for one question to finish before asking the next. While waiting for the explorer results, you can continue working on other local tasks that do not depend on those results. This parallelism is a key advantage of delegation, so use it whenever you have multiple questions to ask.
- Reuse existing explorers for related questions.