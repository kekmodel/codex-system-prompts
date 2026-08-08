---
name: 'Tool: tool-spawn-agent-inherited-model-guidance'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_const
  reached_from:
  - tools/src/agent_tool.rs:9
  symbol: SPAWN_AGENT_INHERITED_MODEL_GUIDANCE
extraction:
  pass: 1.5
  method: rust_const_str
variables: []
tokens:
  o200k_base: 33
description: '`codex-rs/tools/src/agent_tool.rs::SPAWN_AGENT_INHERITED_MODEL_GUIDANCE`'
---
Spawned agents inherit your current model by default. Omit `model` to use that preferred default; set `model` only when an explicit override is needed.