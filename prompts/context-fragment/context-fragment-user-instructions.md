---
name: 'Context fragment: UserInstructions'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/context/user_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/user_instructions.rs:9
  struct: UserInstructions
  role: user
  start_marker: '# AGENTS.md instructions for '
  end_marker: </INSTRUCTIONS>
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 17
description: '`UserInstructions` ContextualUserFragment.'
---
# AGENTS.md instructions for 
{}

<INSTRUCTIONS>
{}

</INSTRUCTIONS>
