---
name: 'Permission: permission-sandbox-workspace-write'
category: permission
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/core/src/context/prompts/permissions/sandbox_mode/workspace_write.md
  kind: include_str
  reached_from:
  - permissions_instructions.rs:31
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 57
description: '`codex-rs/core/src/context/prompts/permissions/sandbox_mode/workspace_write.md`'
---
Filesystem sandboxing defines which files can be read or written. `sandbox_mode` is `workspace-write`: The sandbox permits reading files, and editing files in `cwd` and `writable_roots`. Editing files in other directories requires approval. Network access is {{network_access}}.
