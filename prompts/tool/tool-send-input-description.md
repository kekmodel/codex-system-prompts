---
name: 'Tool: send_input description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:113
  tool_name: send_input
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 41
description: Inline ToolSpec description for `send_input` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Send a message to an existing agent. Use interrupt=true to redirect work immediately. You should reuse the agent by send_input if you believe your assigned task is highly dependent on the context of a previous task.
