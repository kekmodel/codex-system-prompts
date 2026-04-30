---
name: 'Tool: list_agents parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/agent_tool.rs:233
  tool_name: list_agents
  parameter_count: 1
  parameters:
  - name: path_prefix
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 83
description: Per-parameter `JsonSchema` descriptions for `list_agents` (1 parameter).
  Pass 1.7 (M9).
---
# Tool: `list_agents` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/agent_tool.rs:233`). The model sees each `description` field on each parameter at tool-spec time.

## `path_prefix` (string)

Optional task-path prefix (not ending with trailing slash). Accepts the same relative or absolute task-path syntax.
