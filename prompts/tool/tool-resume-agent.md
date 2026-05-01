---
name: 'Tool: resume_agent'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:188
  tool_name: resume_agent
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 97
description: '`resume_agent` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "resume_agent",
  "description": "Resume a previously closed agent by id so it can receive send_input and wait_agent calls.",
  "parameters": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "description": "Agent id to resume."
      }
    },
    "additionalProperties": false
  }
}
```
