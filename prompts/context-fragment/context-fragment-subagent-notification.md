---
name: 'Context fragment: SubagentNotification'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
