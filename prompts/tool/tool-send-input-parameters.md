---
name: 'Tool: send_input parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/agent_tool.rs:113
  tool_name: send_input
  parameter_count: 3
  parameters:
  - name: target
    schema_type: string
  - name: message
    schema_type: string
  - name: interrupt
    schema_type: boolean
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 122
description: Per-parameter `JsonSchema` descriptions for `send_input` (3 parameters).
  Pass 1.7 (M9).
---
# Tool: `send_input` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/agent_tool.rs:113`). The model sees each `description` field on each parameter at tool-spec time.

## `target` (string)

Agent id to message (from spawn_agent).

## `message` (string)

Legacy plain-text message to send to the agent. Use either message or items.

## `interrupt` (boolean)

When true, stop the agent's current task and handle this immediately. When false (default), queue this message.
