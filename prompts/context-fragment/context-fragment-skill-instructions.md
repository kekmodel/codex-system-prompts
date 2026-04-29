---
name: 'Context fragment: SkillInstructions'
category: context-fragment
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
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
description: '`SkillInstructions` ContextualUserFragment from `codex-rs/core/src/context/skill_instructions.rs`.
  Role: ''user''. Markers: ''<skill>'' … ''</skill>''. body() captured as template.'
---
<skill>

<name>{}</name>
<path>{}</path>
{}

</skill>
