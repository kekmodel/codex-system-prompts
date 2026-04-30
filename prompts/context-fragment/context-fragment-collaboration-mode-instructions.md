---
name: 'Context fragment: CollaborationModeInstructions'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/context/collaboration_mode_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/collaboration_mode_instructions.rs:24
  struct: CollaborationModeInstructions
  role: developer
  start_marker: ''
  end_marker: ''
  body_extraction: function-body-source
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 18
description: '`CollaborationModeInstructions` ContextualUserFragment from `codex-rs/core/src/context/collaboration_mode_instructions.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
self.instructions.clone()
}
```

