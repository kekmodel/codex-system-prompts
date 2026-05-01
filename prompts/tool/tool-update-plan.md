---
name: 'Tool: update_plan'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/plan_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/plan_tool.rs:33
  tool_name: update_plan
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 123
description: '`update_plan` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "update_plan",
  "description": "Updates the task plan.\nProvide an optional explanation and a list of plan items, each with a step and status.\nAt most one step can be in_progress at a time.\n",
  "parameters": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "description": "One of: pending, in_progress, completed"
      }
    },
    "additionalProperties": false
  }
}
```
