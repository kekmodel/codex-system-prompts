---
name: 'Tool: write_stdin parameters'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/local_tool.rs:120
  tool_name: write_stdin
  parameter_count: 4
  parameters:
  - name: session_id
    schema_type: number
  - name: chars
    schema_type: string
  - name: yield_time_ms
    schema_type: number
  - name: max_output_tokens
    schema_type: number
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 132
description: Per-parameter `JsonSchema` descriptions for `write_stdin` (4 parameters).
  Pass 1.7 (M9).
---
# Tool: `write_stdin` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/local_tool.rs:120`). The model sees each `description` field on each parameter at tool-spec time.

## `session_id` (number)

Identifier of the running unified exec session.

## `chars` (string)

Bytes to write to stdin (may be empty to poll).

## `yield_time_ms` (number)

How long to wait (in milliseconds) for output before yielding.

## `max_output_tokens` (number)

Maximum number of tokens to return. Excess output will be truncated.
