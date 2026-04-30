---
name: 'Tool: request_user_input parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/request_user_input_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/request_user_input_tool.rs:85
  tool_name: request_user_input
  parameter_count: 5
  parameters:
  - name: label
    schema_type: string
  - name: description
    schema_type: string
  - name: id
    schema_type: string
  - name: header
    schema_type: string
  - name: question
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 141
description: Per-parameter `JsonSchema` descriptions for `request_user_input` (5 parameters).
  Pass 1.7 (M9).
---
# Tool: `request_user_input` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/request_user_input_tool.rs:85`). The model sees each `description` field on each parameter at tool-spec time.

## `label` (string)

User-facing label (1-5 words).

## `description` (string)

One short sentence explaining impact/tradeoff if selected.

## `id` (string)

Stable identifier for mapping answers (snake_case).

## `header` (string)

Short header label shown in the UI (12 or fewer chars).

## `question` (string)

Single-sentence prompt shown to the user.
