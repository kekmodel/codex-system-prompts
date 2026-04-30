---
name: 'Permission: permission-approval-never'
category: permission
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
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
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/never.md`.
  Category: permission. Description will be refined at M5 review.'
---
Approval policy is currently never. Do not provide the `sandbox_permissions` for any reason, commands will be rejected.
