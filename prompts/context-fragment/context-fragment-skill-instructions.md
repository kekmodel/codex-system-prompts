---
name: 'Context fragment: SkillInstructions'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
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
