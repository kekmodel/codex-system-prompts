---
name: 'Tool: get_goal'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
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
  o200k_base: 77
description: '`get_goal` ToolSpec.'
---
```json
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
```
