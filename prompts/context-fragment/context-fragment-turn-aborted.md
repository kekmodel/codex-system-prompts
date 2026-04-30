---
name: 'Context fragment: TurnAborted'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
