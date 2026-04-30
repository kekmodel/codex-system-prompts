---
name: 'Tool: send_message'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:140
  tool_name: send_message
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 132
description: '`send_message` ToolSpec.'
---
{
  "type": "function",
  "name": "send_message",
  "description": "Send a message to an existing agent. The message will be delivered promptly. Does not trigger a new turn.",
  "parameters": {
    "type": "object",
    "properties": {
      "target": {
        "type": "string",
        "description": "Relative or canonical task name to message (from spawn_agent)."
      },
      "message": {
        "type": "string",
        "description": "Message text to queue on the target agent."
      }
    },
    "additionalProperties": false
  }
}
