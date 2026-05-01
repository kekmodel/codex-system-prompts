---
name: 'Tool: close_agent'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:269
  tool_name: close_agent
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 129
description: '`close_agent` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "close_agent",
  "description": "Close an agent and any open descendants when they are no longer needed, and return the target agent's previous status before shutdown was requested. Don't keep agents open for too long if they are not needed anymore.",
  "parameters": {
    "type": "object",
    "properties": {
      "target": {
        "type": "string",
        "description": "Agent id or canonical task name to close (from spawn_agent)."
      }
    },
    "additionalProperties": false
  }
}
```
