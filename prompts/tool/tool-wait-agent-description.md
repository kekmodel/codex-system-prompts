---
name: 'Tool: wait_agent description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:201
  tool_name: wait_agent
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 46
description: Inline ToolSpec description for `wait_agent` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Wait for agents to reach a final status. Completed statuses may include the agent's final message. Returns empty status when timed out. Once the agent reaches a final status, a notification message will be received containing the same completed status.
