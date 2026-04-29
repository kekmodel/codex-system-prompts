---
name: 'Context fragment: PersonalitySpecInstructions'
category: context-fragment
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
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
description: '`PersonalitySpecInstructions` ContextualUserFragment from `codex-rs/core/src/context/personality_spec_instructions.rs`.
  Role: ''developer''. Markers: ''<personality_spec>'' … ''</personality_spec>''.
  body() captured as template.'
---
<personality_spec>
 The user has requested a new communication style. Future messages should adhere to the following personality: 
{} 
</personality_spec>
