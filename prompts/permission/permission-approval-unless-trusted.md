---
name: 'Permission: permission-approval-unless-trusted'
category: permission
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/context/prompts/permissions/approval_policy/unless_trusted.md
  kind: include_str
  reached_from:
  - permissions_instructions.rs:19
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 50
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/unless_trusted.md`.
  Category: permission. Description will be refined at M5 review.'
---
 Approvals are your mechanism to get user consent to run shell commands without the sandbox. `approval_policy` is `unless-trusted`: The harness will escalate most commands for user approval, apart from a limited allowlist of safe "read" commands.
