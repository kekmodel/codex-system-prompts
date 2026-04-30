---
name: 'Mode: mode-review-exit-interrupted'
category: mode
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/core/templates/review/exit_interrupted.xml
  kind: include_bytes
  reached_from:
  - client_common.rs:24
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 67
description: '`codex-rs/core/templates/review/exit_interrupted.xml`'
---
<user_action>
  <context>User initiated a review task, but was interrupted. If user asks about this, tell them to re-initiate a review with `/review` and wait for it to complete.</context>
  <action>review</action>
  <results>
  None.
  </results>
</user_action>

