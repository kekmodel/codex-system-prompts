---
name: 'Tool: tool-spawn-agent-inherited-model-guidance'
category: tool
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
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
description: Guidance attached to spawn_agent's `model` parameter — inheritance default
  rule.
---
Spawned agents inherit your current model by default. Omit `model` to use that preferred default; set `model` only when an explicit override is needed.