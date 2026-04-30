---
name: 'Tool: create_goal'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/goal_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/goal_tool.rs:45
  tool_name: create_goal
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 193
description: '`create_goal` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "create_goal",
  "description": "Create a goal only when explicitly requested by the user or system/developer instructions; do not infer goals from ordinary tasks.\nSet token_budget only when an explicit token budget is requested. Fails if a goal exists; use {UPDATE_GOAL_TOOL_NAME} only for status.",
  "parameters": {
    "type": "object",
    "properties": {
      "objective": {
        "type": "string",
        "description": "Required. The concrete objective to start pursuing. This starts a new active goal only when no goal is currently defined; if a goal already exists, this tool fails."
      },
      "token_budget": {
        "type": "integer",
        "description": "Optional positive token budget for the new active goal."
      }
    },
    "additionalProperties": false
  }
}
```
