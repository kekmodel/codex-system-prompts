---
name: 'Orphan: codex-rs/core/templates/search_tool/tool_description.md'
category: orphan
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/templates/search_tool/tool_description.md
  kind: orphan_unreferenced
  shipping_status: not_shipped
extraction:
  pass: 3
  method: orphan_walk
variables: []
tokens:
  o200k_base: 119
description: Orphan file at `codex-rs/core/templates/search_tool/tool_description.md`.
  Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of
  `rust-v0.126.0-alpha.12`. Per SPEC §1.3 boundary cases, preserved here for historical
  reference. NOT part of the canonical shipping prompt corpus.
---
# Apps (Connectors) tool discovery

Searches over apps/connectors tool metadata with BM25 and exposes matching tools for the next model call.

You have access to all the tools of the following apps/connectors:
{{app_descriptions}}
Some of the tools may not have been provided to you upfront, and you should use this tool (`tool_search`) to search for the required tools and load them for the apps mentioned above. For the apps mentioned above, always use `tool_search` instead of `list_mcp_resources` or `list_mcp_resource_templates` for tool discovery.
