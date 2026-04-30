---
name: 'Tool: list_mcp_resource_templates'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
