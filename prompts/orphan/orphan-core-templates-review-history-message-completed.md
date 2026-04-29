---
name: 'Orphan: codex-rs/core/templates/review/history_message_completed.md'
category: orphan
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
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
description: Orphan file at `codex-rs/core/templates/review/history_message_completed.md`.
  Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of
  `rust-v0.126.0-alpha.12`. Per SPEC §1.3 boundary cases, preserved here for historical
  reference. NOT part of the canonical shipping prompt corpus.
---
<user_action>
  <context>User initiated a review task. Here's the full review output from reviewer model. User may select one or more comments to resolve.</context>
  <action>review</action>
  <results>
  {findings}
  </results>
</user_action>

