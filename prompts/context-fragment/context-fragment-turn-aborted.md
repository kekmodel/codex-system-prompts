---
name: 'Context fragment: TurnAborted'
category: context-fragment
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/core/src/context/turn_aborted.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/turn_aborted.rs:19
  struct: TurnAborted
  role: user
  start_marker: <turn_aborted>
  end_marker: </turn_aborted>
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 11
description: '`TurnAborted` ContextualUserFragment.'
---
<turn_aborted>

{}

</turn_aborted>
