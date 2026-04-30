---
name: 'Tool: update_plan parameters'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/plan_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/plan_tool.rs:33
  tool_name: update_plan
  parameter_count: 1
  parameters:
  - name: status
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 70
description: Per-parameter `JsonSchema` descriptions for `update_plan` (1 parameter).
  Pass 1.7 (M9).
---
# Tool: `update_plan` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/plan_tool.rs:33`). The model sees each `description` field on each parameter at tool-spec time.

## `status` (string)

One of: pending, in_progress, completed
