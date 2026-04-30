---
name: 'Tool: request_permissions parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/local_tool.rs:280
  tool_name: request_permissions
  parameter_count: 1
  parameters:
  - name: reason
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 69
description: Per-parameter `JsonSchema` descriptions for `request_permissions` (1
  parameter). Pass 1.7 (M9).
---
# Tool: `request_permissions` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/local_tool.rs:280`). The model sees each `description` field on each parameter at tool-spec time.

## `reason` (string)

Optional short explanation for why additional permissions are needed.
