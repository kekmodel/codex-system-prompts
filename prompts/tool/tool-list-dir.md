---
name: 'Tool: list_dir'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/utility_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/utility_tool.rs:30
  tool_name: list_dir
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 190
description: '`list_dir` ToolSpec.'
---
{
  "type": "function",
  "name": "list_dir",
  "description": "Lists entries in a local directory with 1-indexed entry numbers and simple type labels.",
  "parameters": {
    "type": "object",
    "properties": {
      "dir_path": {
        "type": "string",
        "description": "Absolute path to the directory to list."
      },
      "offset": {
        "type": "number",
        "description": "The entry number to start listing from. Must be 1 or greater."
      },
      "limit": {
        "type": "number",
        "description": "The maximum number of entries to return."
      },
      "depth": {
        "type": "number",
        "description": "The maximum directory depth to traverse. Must be 1 or greater."
      }
    },
    "additionalProperties": false
  }
}
