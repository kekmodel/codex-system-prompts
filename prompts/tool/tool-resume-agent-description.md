---
name: 'Tool: resume_agent description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:188
  tool_name: resume_agent
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 18
description: Inline ToolSpec description for `resume_agent` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Resume a previously closed agent by id so it can receive send_input and wait_agent calls.
