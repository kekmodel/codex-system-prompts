---
name: 'Tool: request_permissions'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/local_tool.rs:280
  tool_name: request_permissions
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 91
description: '`request_permissions` ToolSpec.'
---
{
  "type": "function",
  "name": "request_permissions",
  "description": "(no `let description = ...` found in enclosing fn)",
  "parameters": {
    "type": "object",
    "properties": {
      "reason": {
        "type": "string",
        "description": "Optional short explanation for why additional permissions are needed."
      }
    },
    "additionalProperties": false
  }
}
