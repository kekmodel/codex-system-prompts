---
name: 'Tool: get_goal description'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/goal_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/goal_tool.rs:17
  tool_name: get_goal
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 24
description: Inline ToolSpec description for `get_goal` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Get the current goal for this thread, including status, budgets, token and elapsed-time usage, and remaining token budget.
