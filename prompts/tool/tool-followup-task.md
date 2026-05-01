---
name: 'Tool: followup_task'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:171
  tool_name: followup_task
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 165
description: '`followup_task` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "followup_task",
  "description": "Send a message to an existing non-root target agent and trigger a turn in that target. If the target is currently mid-turn, the message is queued and will be used to start the target's next turn, after the current turn completes.",
  "parameters": {
    "type": "object",
    "properties": {
      "target": {
        "type": "string",
        "description": "Agent id or canonical task name to message (from spawn_agent)."
      },
      "message": {
        "type": "string",
        "description": "Message text to send to the target agent."
      }
    },
    "additionalProperties": false
  }
}
```
