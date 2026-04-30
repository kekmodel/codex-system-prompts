---
name: 'Tool: list_dir parameters'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/utility_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/utility_tool.rs:30
  tool_name: list_dir
  parameter_count: 4
  parameters:
  - name: dir_path
    schema_type: string
  - name: offset
    schema_type: number
  - name: limit
    schema_type: number
  - name: depth
    schema_type: number
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 127
description: Per-parameter `JsonSchema` descriptions for `list_dir` (4 parameters).
  Pass 1.7 (M9).
---
# Tool: `list_dir` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/utility_tool.rs:30`). The model sees each `description` field on each parameter at tool-spec time.

## `dir_path` (string)

Absolute path to the directory to list.

## `offset` (number)

The entry number to start listing from. Must be 1 or greater.

## `limit` (number)

The maximum number of entries to return.

## `depth` (number)

The maximum directory depth to traverse. Must be 1 or greater.
