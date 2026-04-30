---
name: 'Tool: read_mcp_resource parameters'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/mcp_resource_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/mcp_resource_tool.rs:80
  tool_name: read_mcp_resource
  parameter_count: 2
  parameters:
  - name: server
    schema_type: string
  - name: uri
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 111
description: Per-parameter `JsonSchema` descriptions for `read_mcp_resource` (2 parameters).
  Pass 1.7 (M9).
---
# Tool: `read_mcp_resource` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/mcp_resource_tool.rs:80`). The model sees each `description` field on each parameter at tool-spec time.

## `server` (string)

MCP server name exactly as configured. Must match the 'server' field returned by list_mcp_resources.

## `uri` (string)

Resource URI to read. Must be one of the URIs returned by list_mcp_resources.
