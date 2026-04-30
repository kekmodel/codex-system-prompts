---
name: 'Permission: permission-approval-never'
category: permission
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
