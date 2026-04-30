---
name: 'Tool: tool_suggest parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/tool_discovery.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/tool_discovery.rs:305
  tool_name: tool_suggest
  parameter_count: 4
  parameters:
  - name: tool_type
    schema_type: string
  - name: action_type
    schema_type: string
  - name: tool_id
    schema_type: string
  - name: suggest_reason
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 136
description: Per-parameter `JsonSchema` descriptions for `tool_suggest` (4 parameters).
  Pass 1.7 (M9).
---
# Tool: `tool_suggest` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/tool_discovery.rs:305`). The model sees each `description` field on each parameter at tool-spec time.

## `tool_type` (string)

Type of discoverable tool to suggest. Use "connector" or "plugin".

## `action_type` (string)

Suggested action for the tool. Use "install".

## `tool_id` (string)

Connector or plugin id to suggest.

## `suggest_reason` (string)

Concise one-line user-facing reason why this tool can help with the current request.
