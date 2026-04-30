---
name: 'Tool: request_user_input'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/request_user_input_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/request_user_input_tool.rs:85
  tool_name: request_user_input
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 231
description: '`request_user_input` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "request_user_input",
  "description": "Request user input for one to three short questions and wait for the response. This tool is only available in {allowed_modes}.",
  "parameters": {
    "type": "object",
    "properties": {
      "label": {
        "type": "string",
        "description": "User-facing label (1-5 words)."
      },
      "description": {
        "type": "string",
        "description": "One short sentence explaining impact/tradeoff if selected."
      },
      "id": {
        "type": "string",
        "description": "Stable identifier for mapping answers (snake_case)."
      },
      "header": {
        "type": "string",
        "description": "Short header label shown in the UI (12 or fewer chars)."
      },
      "question": {
        "type": "string",
        "description": "Single-sentence prompt shown to the user."
      }
    },
    "additionalProperties": false
  }
}
```
