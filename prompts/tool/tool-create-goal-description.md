---
name: 'Tool: create_goal description'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/goal_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/goal_tool.rs:45
  tool_name: create_goal
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 55
description: Inline ToolSpec description for `create_goal` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Create a goal only when explicitly requested by the user or system/developer instructions; do not infer goals from ordinary tasks.
Set token_budget only when an explicit token budget is requested. Fails if a goal exists; use {UPDATE_GOAL_TOOL_NAME} only for status.
