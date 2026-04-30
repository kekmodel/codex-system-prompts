---
name: 'Tool: shell parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/local_tool.rs:185
  tool_name: shell
  parameter_count: 2
  parameters:
  - name: workdir
    schema_type: string
  - name: timeout_ms
    schema_type: number
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 84
description: Per-parameter `JsonSchema` descriptions for `shell` (2 parameters). Pass
  1.7 (M9).
---
# Tool: `shell` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/local_tool.rs:185`). The model sees each `description` field on each parameter at tool-spec time.

## `workdir` (string)

The working directory to execute the command in

## `timeout_ms` (number)

The timeout for the command in milliseconds
