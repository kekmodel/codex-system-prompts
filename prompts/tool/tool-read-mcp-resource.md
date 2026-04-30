---
name: 'Tool: read_mcp_resource'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/mcp_resource_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/mcp_resource_tool.rs:80
  tool_name: read_mcp_resource
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 147
description: '`read_mcp_resource` ToolSpec.'
---
{
  "type": "function",
  "name": "read_mcp_resource",
  "description": "Read a specific resource from an MCP server given the server name and resource URI.",
  "parameters": {
    "type": "object",
    "properties": {
      "server": {
        "type": "string",
        "description": "MCP server name exactly as configured. Must match the 'server' field returned by list_mcp_resources."
      },
      "uri": {
        "type": "string",
        "description": "Resource URI to read. Must be one of the URIs returned by list_mcp_resources."
      }
    },
    "additionalProperties": false
  }
}
