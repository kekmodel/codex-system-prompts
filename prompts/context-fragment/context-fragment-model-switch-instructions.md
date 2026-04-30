---
name: 'Context fragment: ModelSwitchInstructions'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
description: '`ModelSwitchInstructions` ContextualUserFragment.'
---
<model_switch>

The user was previously using a different model. Please continue the conversation according to the following instructions:

{}

</model_switch>
