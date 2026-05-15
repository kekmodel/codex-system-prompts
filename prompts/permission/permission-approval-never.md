---
name: 'Permission: permission-approval-never'
category: permission
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/core/src/context/prompts/permissions/approval_policy/never.md
  kind: include_str
  reached_from:
  - permissions_instructions.rs:17
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 23
description: '`codex-rs/core/src/context/prompts/permissions/approval_policy/never.md`'
---
Approval policy is currently never. Do not provide the `sandbox_permissions` for any reason, commands will be rejected.
