---
name: 'Tool: list_mcp_resources parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/mcp_resource_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/mcp_resource_tool.rs:24
  tool_name: list_mcp_resources
  parameter_count: 2
  parameters:
  - name: server
    schema_type: string
  - name: cursor
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 101
description: Per-parameter `JsonSchema` descriptions for `list_mcp_resources` (2 parameters).
  Pass 1.7 (M9).
---
# Tool: `list_mcp_resources` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/mcp_resource_tool.rs:24`). The model sees each `description` field on each parameter at tool-spec time.

## `server` (string)

Optional MCP server name. When omitted, lists resources from every configured server.

## `cursor` (string)

Opaque cursor returned by a previous list_mcp_resources call for the same server.
