---
name: 'Tool: list_agents description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:233
  tool_name: list_agents
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 18
description: Inline ToolSpec description for `list_agents` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
List live agents in the current root thread tree. Optionally filter by task-path prefix.
