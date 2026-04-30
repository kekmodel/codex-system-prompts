---
name: 'Context fragment: SubagentNotification'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/subagent_notification.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/subagent_notification.rs:20
  struct: SubagentNotification
  role: user
  start_marker: <subagent_notification>
  end_marker: </subagent_notification>
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 11
description: '`SubagentNotification` ContextualUserFragment from `codex-rs/core/src/context/subagent_notification.rs`.
  Role: ''user''. Markers: ''<subagent_notification>'' … ''</subagent_notification>''.
  body() captured as template.'
---
<subagent_notification>

{}

</subagent_notification>
