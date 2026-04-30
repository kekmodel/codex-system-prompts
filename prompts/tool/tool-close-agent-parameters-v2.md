---
name: 'Tool: close_agent parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/agent_tool.rs:269
  tool_name: close_agent
  parameter_count: 1
  parameters:
  - name: target
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 73
description: Per-parameter `JsonSchema` descriptions for `close_agent` (1 parameter).
  Pass 1.7 (M9).
---
# Tool: `close_agent` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/agent_tool.rs:269`). The model sees each `description` field on each parameter at tool-spec time.

## `target` (string)

Agent id or canonical task name to close (from spawn_agent).
