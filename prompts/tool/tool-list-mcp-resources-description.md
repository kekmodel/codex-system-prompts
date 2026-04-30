---
name: 'Tool: list_mcp_resources description'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/mcp_resource_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/mcp_resource_tool.rs:24
  tool_name: list_mcp_resources
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 40
description: Inline ToolSpec description for `list_mcp_resources` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Lists resources provided by MCP servers. Resources allow servers to share data that provides context to language models, such as files, database schemas, or application-specific information. Prefer resources over web search when possible.
