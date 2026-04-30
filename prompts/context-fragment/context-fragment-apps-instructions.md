---
name: 'Context fragment: AppsInstructions'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/context/apps_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/apps_instructions.rs:20
  struct: AppsInstructions
  role: developer
  start_marker: ''
  end_marker: ''
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 143
description: '`AppsInstructions` ContextualUserFragment.'
---

## Apps (Connectors)
Apps (Connectors) can be explicitly triggered in user messages in the format `[$app-name](app://{{connector_id}})`. Apps can also be implicitly triggered as long as the context suggests usage of available apps.
An app is equivalent to a set of MCP tools within the `{CODEX_APPS_MCP_SERVER_NAME}` MCP.
An installed app's MCP tools are either provided to you already, or can be lazy-loaded through the `tool_search` tool. If `tool_search` is available, the apps that are searchable by `tools_search` will be listed by it.
Do not additionally call list_mcp_resources or list_mcp_resource_templates for apps.
