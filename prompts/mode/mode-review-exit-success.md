---
name: 'Mode: mode-review-exit-success'
category: mode
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/core/templates/review/exit_success.xml
  kind: include_bytes
  reached_from:
  - client_common.rs:22
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 59
description: '`codex-rs/core/templates/review/exit_success.xml`'
---
<user_action>
  <context>User initiated a review task. Here's the full review output from reviewer model. User may select one or more comments to resolve.</context>
  <action>review</action>
  <results>
  {{results}}
  </results>
  </user_action>
