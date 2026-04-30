---
name: 'Permission: permission-approval-on-failure'
category: permission
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
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
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_failure.md`.
  Category: permission. Description will be refined at M5 review.'
---
Approvals are your mechanism to get user consent to run shell commands without the sandbox. `approval_policy` is `on-failure`: The harness will allow all commands to run in the sandbox (if enabled), and failures will be escalated to the user for approval to run again without the sandbox.
