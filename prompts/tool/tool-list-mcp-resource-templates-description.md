---
name: 'Tool: list_mcp_resource_templates description'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/mcp_resource_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/mcp_resource_tool.rs:52
  tool_name: list_mcp_resource_templates
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 48
description: Inline ToolSpec description for `list_mcp_resource_templates` (literal
  `static_plain`). Captured by Pass 1.7 (M9).
---
Lists resource templates provided by MCP servers. Parameterized resource templates allow servers to share data that takes parameters and provides context to language models, such as files, database schemas, or application-specific information. Prefer resource templates over web search when possible.
