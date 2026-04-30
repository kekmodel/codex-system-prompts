---
name: 'Mode: mode-review-exit-success'
category: mode
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_success.xml`.
  Category: mode. Description will be refined at M5 review.'
---
<user_action>
  <context>User initiated a review task. Here's the full review output from reviewer model. User may select one or more comments to resolve.</context>
  <action>review</action>
  <results>
  {{results}}
  </results>
  </user_action>
