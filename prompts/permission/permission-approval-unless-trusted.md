---
name: 'Permission: permission-approval-unless-trusted'
category: permission
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/src/context/prompts/permissions/approval_policy/unless_trusted.md
  kind: include_str
  reached_from:
  - core/src/context/permissions_instructions.rs:19
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
