---
name: 'Tool: spawn_agent parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/agent_tool.rs:69
  tool_name: spawn_agent
  parameter_count: 1
  parameters:
  - name: task_name
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 77
description: Per-parameter `JsonSchema` descriptions for `spawn_agent` (1 parameter).
  Pass 1.7 (M9).
---
# Tool: `spawn_agent` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/agent_tool.rs:69`). The model sees each `description` field on each parameter at tool-spec time.

## `task_name` (string)

Task name for the new agent. Use lowercase letters, digits, and underscores.
