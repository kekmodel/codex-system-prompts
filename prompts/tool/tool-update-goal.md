---
name: 'Tool: update_goal'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/goal_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/goal_tool.rs:74
  tool_name: update_goal
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 165
description: '`update_goal` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "update_goal",
  "description": "Update the existing goal.\nUse this tool only to mark the goal achieved.\nSet status to `complete` only when the objective has actually been achieved and no required work remains.\nDo not mark a goal complete merely because its budget is nearly exhausted or because you are stopping work.\nYou cannot use this tool to pause, resume, or budget-limit a goal; those status changes are controlled by the user or system.\nWhen marking a budgeted goal achieved with status `complete`, report the final token usage from the tool result to the user.",
  "parameters": {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
}
```
