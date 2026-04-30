---
name: 'Context fragment: TurnAborted'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
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
description: '`TurnAborted` ContextualUserFragment from `codex-rs/core/src/context/turn_aborted.rs`.
  Role: ''user''. Markers: ''<turn_aborted>'' … ''</turn_aborted>''. body() captured
  as template.'
---
<turn_aborted>

{}

</turn_aborted>
