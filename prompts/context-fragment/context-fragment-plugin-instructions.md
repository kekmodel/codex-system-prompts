---
name: 'Context fragment: PluginInstructions'
category: context-fragment
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/src/context/plugin_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/plugin_instructions.rs:14
  struct: PluginInstructions
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
description: '`PluginInstructions` ContextualUserFragment from `codex-rs/core/src/context/plugin_instructions.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
self.text.clone()
}
```

