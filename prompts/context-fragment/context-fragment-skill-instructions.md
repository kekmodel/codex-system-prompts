---
name: 'Context fragment: SkillInstructions'
category: context-fragment
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/core/src/context/skill_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/skill_instructions.rs:22
  struct: SkillInstructions
  role: user
  start_marker: <skill>
  end_marker: </skill>
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 19
description: '`SkillInstructions` ContextualUserFragment.'
---
<skill>

<name>{}</name>
<path>{}</path>
{}

</skill>
