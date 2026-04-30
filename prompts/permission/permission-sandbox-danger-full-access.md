---
name: 'Permission: permission-sandbox-danger-full-access'
category: permission
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
