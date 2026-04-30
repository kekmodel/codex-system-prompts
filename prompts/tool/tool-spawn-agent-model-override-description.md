---
name: 'Tool: tool-spawn-agent-model-override-description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_const
  reached_from:
  - tools/src/agent_tool.rs:10
  symbol: SPAWN_AGENT_MODEL_OVERRIDE_DESCRIPTION
extraction:
  pass: 1.5
  method: rust_const_str
variables: []
tokens:
  o200k_base: 44
description: '`codex-rs/tools/src/agent_tool.rs::SPAWN_AGENT_MODEL_OVERRIDE_DESCRIPTION`'
---
Optional model override for the new agent. Leave unset to inherit the same model as the parent, which is the preferred default. Only set this when the user explicitly asks for a different model or the task clearly requires one.