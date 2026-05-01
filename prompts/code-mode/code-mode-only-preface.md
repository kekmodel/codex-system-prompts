---
name: 'Code-mode: code-mode-only-preface'
category: code-mode
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/code-mode/src/description.rs
  kind: rust_const
  reached_from:
  - code-mode/src/description.rs:10
  symbol: CODE_MODE_ONLY_PREFACE
extraction:
  pass: 1.5
  method: rust_const_str
variables: []
tokens:
  o200k_base: 76
description: '`codex-rs/code-mode/src/description.rs::CODE_MODE_ONLY_PREFACE`'
---
Some nested MCP/app tools may be omitted from this description. They are still available on the global `tools` object and listed in `ALL_TOOLS`.
To find one, filter `ALL_TOOLS` by `name` and `description`; do not print the full `ALL_TOOLS` array. Print only a small set of relevant matches if you need to inspect them.