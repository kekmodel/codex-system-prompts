---
name: 'Permission: permission-sandbox-workspace-write'
category: permission
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
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
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/workspace_write.md`.
  Category: permission. Description will be refined at M5 review.'
---
Filesystem sandboxing defines which files can be read or written. `sandbox_mode` is `workspace-write`: The sandbox permits reading files, and editing files in `cwd` and `writable_roots`. Editing files in other directories requires approval. Network access is {{network_access}}.
