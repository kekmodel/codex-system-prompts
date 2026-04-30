---
name: 'Tool: list_mcp_resources'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/mcp_resource_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/mcp_resource_tool.rs:24
  tool_name: list_mcp_resources
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 166
description: '`list_mcp_resources` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "list_mcp_resources",
  "description": "Lists resources provided by MCP servers. Resources allow servers to share data that provides context to language models, such as files, database schemas, or application-specific information. Prefer resources over web search when possible.",
  "parameters": {
    "type": "object",
    "properties": {
      "server": {
        "type": "string",
        "description": "Optional MCP server name. When omitted, lists resources from every configured server."
      },
      "cursor": {
        "type": "string",
        "description": "Opaque cursor returned by a previous list_mcp_resources call for the same server."
      }
    },
    "additionalProperties": false
  }
}
```
