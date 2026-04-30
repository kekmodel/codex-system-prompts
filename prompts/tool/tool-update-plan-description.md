---
name: 'Tool: update_plan description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/plan_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/plan_tool.rs:33
  tool_name: update_plan
  description_kind: static_raw
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 35
description: Inline ToolSpec description for `update_plan` (literal `static_raw`).
  Captured by Pass 1.7 (M9).
---
Updates the task plan.
Provide an optional explanation and a list of plan items, each with a step and status.
At most one step can be in_progress at a time.
