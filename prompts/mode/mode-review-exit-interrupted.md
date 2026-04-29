---
name: 'Mode: mode-review-exit-interrupted'
category: mode
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/templates/review/exit_interrupted.xml
  kind: include_bytes
  reached_from:
  - core/src/client_common.rs:24
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 67
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_interrupted.xml`.
  Category: mode. Description will be refined at M5 review.'
---
<user_action>
  <context>User initiated a review task, but was interrupted. If user asks about this, tell them to re-initiate a review with `/review` and wait for it to complete.</context>
  <action>review</action>
  <results>
  None.
  </results>
</user_action>

