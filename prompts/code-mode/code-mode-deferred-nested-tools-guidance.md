---
name: 'Code-mode: code-mode-deferred-nested-tools-guidance'
category: code-mode
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/code-mode/src/description.rs
  kind: rust_const
  reached_from:
  - code-mode/src/description.rs:12
  symbol: DEFERRED_NESTED_TOOLS_GUIDANCE
extraction:
  pass: 1.5
  method: rust_const_str
variables: []
tokens:
  o200k_base: 76
description: Guidance noting that some nested MCP/app tools may be omitted from the
  description but are still callable via `tools` / `ALL_TOOLS`.
---
Some nested MCP/app tools may be omitted from this description. They are still available on the global `tools` object and listed in `ALL_TOOLS`.
To find one, filter `ALL_TOOLS` by `name` and `description`; do not print the full `ALL_TOOLS` array. Print only a small set of relevant matches if you need to inspect them.