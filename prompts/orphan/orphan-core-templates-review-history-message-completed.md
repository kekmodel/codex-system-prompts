---
name: 'Orphan: codex-rs/core/templates/review/history_message_completed.md'
category: orphan
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/templates/review/history_message_completed.md
  kind: orphan_unreferenced
  shipping_status: not_shipped
extraction:
  pass: 3
  method: orphan_walk
variables: []
tokens:
  o200k_base: 59
description: 'Orphan: `codex-rs/core/templates/review/history_message_completed.md`
  (not `include_str!`''d).'
---
<user_action>
  <context>User initiated a review task. Here's the full review output from reviewer model. User may select one or more comments to resolve.</context>
  <action>review</action>
  <results>
  {findings}
  </results>
</user_action>

