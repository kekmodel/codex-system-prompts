---
name: 'Context fragment: ModelSwitchInstructions'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/model_switch_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/model_switch_instructions.rs:16
  struct: ModelSwitchInstructions
  role: developer
  start_marker: <model_switch>
  end_marker: </model_switch>
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 28
description: '`ModelSwitchInstructions` ContextualUserFragment from `codex-rs/core/src/context/model_switch_instructions.rs`.
  Role: ''developer''. Markers: ''<model_switch>'' … ''</model_switch>''. body() captured
  as template.'
---
<model_switch>

The user was previously using a different model. Please continue the conversation according to the following instructions:

{}

</model_switch>
