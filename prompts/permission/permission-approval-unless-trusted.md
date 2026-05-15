---
name: 'Permission: permission-approval-unless-trusted'
category: permission
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
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
description: '`codex-rs/core/src/context/prompts/permissions/approval_policy/unless_trusted.md`'
---
 Approvals are your mechanism to get user consent to run shell commands without the sandbox. `approval_policy` is `unless-trusted`: The harness will escalate most commands for user approval, apart from a limited allowlist of safe "read" commands.
