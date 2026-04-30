---
name: 'Tool: send_message description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:140
  tool_name: send_message
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 22
description: Inline ToolSpec description for `send_message` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Send a message to an existing agent. The message will be delivered promptly. Does not trigger a new turn.
