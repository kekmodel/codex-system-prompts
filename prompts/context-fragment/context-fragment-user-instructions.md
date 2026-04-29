---
name: 'Context fragment: UserInstructions'
category: context-fragment
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
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
description: '`UserInstructions` ContextualUserFragment from `codex-rs/core/src/context/user_instructions.rs`.
  Role: ''user''. Markers: ''# AGENTS.md instructions for '' … ''</INSTRUCTIONS>''.
  body() captured as template.'
---
# AGENTS.md instructions for 
{}

<INSTRUCTIONS>
{}

</INSTRUCTIONS>
