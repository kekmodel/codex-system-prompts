---
name: 'Tool: test_sync_tool'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/utility_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/utility_tool.rs:87
  tool_name: test_sync_tool
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 216
description: '`test_sync_tool` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "test_sync_tool",
  "description": "Internal synchronization helper used by Codex integration tests.",
  "parameters": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "description": "Identifier shared by concurrent calls that should rendezvous"
      },
      "participants": {
        "type": "number",
        "description": "Number of tool calls that must arrive before the barrier opens"
      },
      "timeout_ms": {
        "type": "number",
        "description": "Maximum time in milliseconds to wait at the barrier"
      },
      "sleep_before_ms": {
        "type": "number",
        "description": "Optional delay in milliseconds before any other action"
      },
      "sleep_after_ms": {
        "type": "number",
        "description": "Optional delay in milliseconds after completing the barrier"
      }
    },
    "additionalProperties": false
  }
}
```
