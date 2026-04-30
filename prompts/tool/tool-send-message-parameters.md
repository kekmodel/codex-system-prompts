---
name: 'Tool: send_message parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/agent_tool.rs:140
  tool_name: send_message
  parameter_count: 2
  parameters:
  - name: target
    schema_type: string
  - name: message
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 88
description: Per-parameter `JsonSchema` descriptions for `send_message` (2 parameters).
  Pass 1.7 (M9).
---
# Tool: `send_message` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/agent_tool.rs:140`). The model sees each `description` field on each parameter at tool-spec time.

## `target` (string)

Relative or canonical task name to message (from spawn_agent).

## `message` (string)

Message text to queue on the target agent.
