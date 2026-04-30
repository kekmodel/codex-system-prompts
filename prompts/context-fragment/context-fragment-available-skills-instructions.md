---
name: 'Context fragment: AvailableSkillsInstructions'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/available_skills_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/available_skills_instructions.rs:23
  struct: AvailableSkillsInstructions
  role: developer
  start_marker: ''
  end_marker: ''
  body_extraction: function-body-source
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 30
description: '`AvailableSkillsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_skills_instructions.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
render_available_skills_body(&self.skill_root_lines, &self.skill_lines)
}
```

