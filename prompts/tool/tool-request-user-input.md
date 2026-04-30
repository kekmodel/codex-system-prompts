---
name: 'Tool: request_user_input'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
  o200k_base: 226
description: '`request_user_input` ToolSpec.'
---
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
