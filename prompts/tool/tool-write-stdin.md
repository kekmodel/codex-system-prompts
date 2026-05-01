---
name: 'Tool: write_stdin'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/local_tool.rs:120
  tool_name: write_stdin
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 197
description: '`write_stdin` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "write_stdin",
  "description": "Writes characters to an existing unified exec session and returns recent output.",
  "parameters": {
    "type": "object",
    "properties": {
      "session_id": {
        "type": "number",
        "description": "Identifier of the running unified exec session."
      },
      "chars": {
        "type": "string",
        "description": "Bytes to write to stdin (may be empty to poll)."
      },
      "yield_time_ms": {
        "type": "number",
        "description": "How long to wait (in milliseconds) for output before yielding."
      },
      "max_output_tokens": {
        "type": "number",
        "description": "Maximum number of tokens to return. Excess output will be truncated."
      }
    },
    "additionalProperties": false
  }
}
```
