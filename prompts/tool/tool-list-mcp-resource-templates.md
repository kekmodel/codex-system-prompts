---
name: 'Tool: list_mcp_resource_templates'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/mcp_resource_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/mcp_resource_tool.rs:52
  tool_name: list_mcp_resource_templates
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 177
description: '`list_mcp_resource_templates` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "list_mcp_resource_templates",
  "description": "Lists resource templates provided by MCP servers. Parameterized resource templates allow servers to share data that takes parameters and provides context to language models, such as files, database schemas, or application-specific information. Prefer resource templates over web search when possible.",
  "parameters": {
    "type": "object",
    "properties": {
      "server": {
        "type": "string",
        "description": "Optional MCP server name. When omitted, lists resource templates from all configured servers."
      },
      "cursor": {
        "type": "string",
        "description": "Opaque cursor returned by a previous list_mcp_resource_templates call for the same server."
      }
    },
    "additionalProperties": false
  }
}
```
