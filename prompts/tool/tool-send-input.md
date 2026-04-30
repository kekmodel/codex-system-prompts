---
name: 'Tool: send_input'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:113
  tool_name: send_input
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 197
description: '`send_input` ToolSpec.'
---
{
  "type": "function",
  "name": "send_input",
  "description": "Send a message to an existing agent. Use interrupt=true to redirect work immediately. You should reuse the agent by send_input if you believe your assigned task is highly dependent on the context of a previous task.",
  "parameters": {
    "type": "object",
    "properties": {
      "target": {
        "type": "string",
        "description": "Agent id to message (from spawn_agent)."
      },
      "message": {
        "type": "string",
        "description": "Legacy plain-text message to send to the agent. Use either message or items."
      },
      "interrupt": {
        "type": "boolean",
        "description": "When true, stop the agent's current task and handle this immediately. When false (default), queue this message."
      }
    },
    "additionalProperties": false
  }
}
