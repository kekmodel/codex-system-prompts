---
name: 'Tool: test_sync_tool parameters'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/utility_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/utility_tool.rs:87
  tool_name: test_sync_tool
  parameter_count: 5
  parameters:
  - name: id
    schema_type: string
  - name: participants
    schema_type: number
  - name: timeout_ms
    schema_type: number
  - name: sleep_before_ms
    schema_type: number
  - name: sleep_after_ms
    schema_type: number
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 144
description: Per-parameter `JsonSchema` descriptions for `test_sync_tool` (5 parameters).
  Pass 1.7 (M9).
---
# Tool: `test_sync_tool` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/utility_tool.rs:87`). The model sees each `description` field on each parameter at tool-spec time.

## `id` (string)

Identifier shared by concurrent calls that should rendezvous

## `participants` (number)

Number of tool calls that must arrive before the barrier opens

## `timeout_ms` (number)

Maximum time in milliseconds to wait at the barrier

## `sleep_before_ms` (number)

Optional delay in milliseconds before any other action

## `sleep_after_ms` (number)

Optional delay in milliseconds after completing the barrier
