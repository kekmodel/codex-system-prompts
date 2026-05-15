---
name: 'Mode: mode-review-exit-success'
category: mode
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
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
