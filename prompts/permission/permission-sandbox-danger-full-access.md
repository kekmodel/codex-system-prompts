---
name: 'Permission: permission-sandbox-danger-full-access'
category: permission
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/prompts/permissions/sandbox_mode/danger_full_access.md
  kind: include_str
  reached_from:
  - permissions_instructions.rs:29
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 40
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/danger_full_access.md`.
  Category: permission. Description will be refined at M5 review.'
---
Filesystem sandboxing defines which files can be read or written. `sandbox_mode` is `danger-full-access`: No filesystem sandboxing - all commands are permitted. Network access is {{network_access}}.
