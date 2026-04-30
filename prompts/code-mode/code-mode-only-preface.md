---
name: 'Code-mode: code-mode-only-preface'
category: code-mode
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
description: Preface added when code-mode is the only tool exposure (no other MCP
  tools listed).
---
Some nested MCP/app tools may be omitted from this description. They are still available on the global `tools` object and listed in `ALL_TOOLS`.
To find one, filter `ALL_TOOLS` by `name` and `description`; do not print the full `ALL_TOOLS` array. Print only a small set of relevant matches if you need to inspect them.