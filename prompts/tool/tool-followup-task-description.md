---
name: 'Tool: followup_task description'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:171
  tool_name: followup_task
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 48
description: Inline ToolSpec description for `followup_task` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Send a message to an existing non-root target agent and trigger a turn in that target. If the target is currently mid-turn, the message is queued and will be used to start the target's next turn, after the current turn completes.
