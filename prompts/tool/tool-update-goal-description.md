---
name: 'Tool: update_goal description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/goal_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/goal_tool.rs:74
  tool_name: update_goal
  description_kind: static_raw
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 107
description: Inline ToolSpec description for `update_goal` (literal `static_raw`).
  Captured by Pass 1.7 (M9).
---
Update the existing goal.
Use this tool only to mark the goal achieved.
Set status to `complete` only when the objective has actually been achieved and no required work remains.
Do not mark a goal complete merely because its budget is nearly exhausted or because you are stopping work.
You cannot use this tool to pause, resume, or budget-limit a goal; those status changes are controlled by the user or system.
When marking a budgeted goal achieved with status `complete`, report the final token usage from the tool result to the user.
