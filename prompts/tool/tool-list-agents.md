---
name: 'Tool: list_agents'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:233
  tool_name: list_agents
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 115
description: '`list_agents` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "list_agents",
  "description": "List live agents in the current root thread tree. Optionally filter by task-path prefix.",
  "parameters": {
    "type": "object",
    "properties": {
      "path_prefix": {
        "type": "string",
        "description": "Optional task-path prefix (not ending with trailing slash). Accepts the same relative or absolute task-path syntax."
      }
    },
    "additionalProperties": false
  }
}
```
