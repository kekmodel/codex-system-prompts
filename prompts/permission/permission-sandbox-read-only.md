---
name: 'Permission: permission-sandbox-read-only'
category: permission
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/core/src/context/prompts/permissions/sandbox_mode/read_only.md
  kind: include_str
  reached_from:
  - permissions_instructions.rs:32
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 36
description: '`codex-rs/core/src/context/prompts/permissions/sandbox_mode/read_only.md`'
---
Filesystem sandboxing defines which files can be read or written. `sandbox_mode` is `read-only`: The sandbox only permits reading files. Network access is {{network_access}}.
