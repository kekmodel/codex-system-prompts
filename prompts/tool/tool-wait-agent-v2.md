---
name: 'Tool: wait_agent'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:213
  tool_name: wait_agent
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 103
description: '`wait_agent` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "wait_agent",
  "description": "Wait for a mailbox update from any live agent, including queued messages and final-status notifications. Does not return the content; returns either a summary of which agents have updates (if any), or a timeout summary if no mailbox update arrives before the deadline.",
  "parameters": {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
}
```
