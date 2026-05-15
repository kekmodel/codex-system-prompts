---
name: 'Context fragment: SubagentNotification'
category: context-fragment
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
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
description: '`SubagentNotification` ContextualUserFragment.'
---
<subagent_notification>

{}

</subagent_notification>
