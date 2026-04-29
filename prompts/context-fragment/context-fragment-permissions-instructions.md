---
name: 'Context fragment: PermissionsInstructions'
category: context-fragment
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/src/context/permissions_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/permissions_instructions.rs:169
  struct: PermissionsInstructions
  role: developer
  start_marker: <permissions instructions>
  end_marker: </permissions instructions>
  body_extraction: function-body-source
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 26
description: '`PermissionsInstructions` ContextualUserFragment from `codex-rs/core/src/context/permissions_instructions.rs`.
  Role: ''developer''. Markers: ''<permissions instructions>'' … ''</permissions instructions>''.
  body() captured as function-body-source.'
---
<permissions instructions>

```rust
fn body(&self) -> String {
self.text.clone()
}
```

</permissions instructions>
