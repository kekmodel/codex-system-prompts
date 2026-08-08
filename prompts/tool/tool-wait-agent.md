---
name: 'Tool: wait_agent'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:201
  tool_name: wait_agent
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 99
description: '`wait_agent` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "wait_agent",
  "description": "Wait for agents to reach a final status. Completed statuses may include the agent's final message. Returns empty status when timed out. Once the agent reaches a final status, a notification message will be received containing the same completed status.",
  "parameters": {
    "type": "object",
    "properties": {},
    "additionalProperties": false
  }
}
```
