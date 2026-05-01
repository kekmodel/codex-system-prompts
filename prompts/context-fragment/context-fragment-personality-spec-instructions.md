---
name: 'Context fragment: PersonalitySpecInstructions'
category: context-fragment
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/core/src/context/personality_spec_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/personality_spec_instructions.rs:14
  struct: PersonalitySpecInstructions
  role: developer
  start_marker: <personality_spec>
  end_marker: </personality_spec>
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 31
description: '`PersonalitySpecInstructions` ContextualUserFragment.'
---
<personality_spec>
 The user has requested a new communication style. Future messages should adhere to the following personality: 
{} 
</personality_spec>
