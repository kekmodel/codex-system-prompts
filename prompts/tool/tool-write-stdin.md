---
name: 'Tool: write_stdin'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
  o200k_base: 192
description: '`write_stdin` ToolSpec.'
---
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
