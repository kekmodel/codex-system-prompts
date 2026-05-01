---
name: 'Permission: permission-sandbox-danger-full-access'
category: permission
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
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
description: '`codex-rs/core/src/context/prompts/permissions/sandbox_mode/danger_full_access.md`'
---
Filesystem sandboxing defines which files can be read or written. `sandbox_mode` is `danger-full-access`: No filesystem sandboxing - all commands are permitted. Network access is {{network_access}}.
