---
name: 'Tool: get_goal'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/goal_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/goal_tool.rs:17
  tool_name: get_goal
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 72
description: '`get_goal` ToolSpec.'
---
{
  "type": "function",
  "name": "get_goal",
  "description": "Get the current goal for this thread, including status, budgets, token and elapsed-time usage, and remaining token budget.",
  "parameters": {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
}
