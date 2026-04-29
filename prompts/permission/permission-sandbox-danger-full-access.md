---
name: 'Permission: permission-sandbox-danger-full-access'
category: permission
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/src/context/prompts/permissions/sandbox_mode/danger_full_access.md
  kind: include_str
  reached_from:
  - core/src/context/permissions_instructions.rs:29
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
