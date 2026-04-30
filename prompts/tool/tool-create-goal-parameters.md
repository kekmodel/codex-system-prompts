---
name: 'Tool: create_goal parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/goal_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/goal_tool.rs:45
  tool_name: create_goal
  parameter_count: 2
  parameters:
  - name: objective
    schema_type: string
  - name: token_budget
    schema_type: integer
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 111
description: Per-parameter `JsonSchema` descriptions for `create_goal` (2 parameters).
  Pass 1.7 (M9).
---
# Tool: `create_goal` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/goal_tool.rs:45`). The model sees each `description` field on each parameter at tool-spec time.

## `objective` (string)

Required. The concrete objective to start pursuing. This starts a new active goal only when no goal is currently defined; if a goal already exists, this tool fails.

## `token_budget` (integer)

Optional positive token budget for the new active goal.
