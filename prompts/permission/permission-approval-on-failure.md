---
name: 'Permission: permission-approval-on-failure'
category: permission
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
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
