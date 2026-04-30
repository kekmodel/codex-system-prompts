---
name: 'Context fragment: HookAdditionalContext'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/hook_additional_context.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/hook_additional_context.rs:14
  struct: HookAdditionalContext
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
description: '`HookAdditionalContext` ContextualUserFragment from `codex-rs/core/src/context/hook_additional_context.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
self.text.clone()
}
```

