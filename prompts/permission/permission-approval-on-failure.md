---
name: 'Permission: permission-approval-on-failure'
category: permission
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/context/prompts/permissions/approval_policy/on_failure.md
  kind: include_str
  reached_from:
  - permissions_instructions.rs:21
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 60
description: '`codex-rs/core/src/context/prompts/permissions/approval_policy/on_failure.md`'
---
Approvals are your mechanism to get user consent to run shell commands without the sandbox. `approval_policy` is `on-failure`: The harness will allow all commands to run in the sandbox (if enabled), and failures will be escalated to the user for approval to run again without the sandbox.
