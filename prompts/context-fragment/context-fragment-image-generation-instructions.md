---
name: 'Context fragment: ImageGenerationInstructions'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/context/image_generation_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/image_generation_instructions.rs:19
  struct: ImageGenerationInstructions
  role: developer
  start_marker: ''
  end_marker: ''
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 41
description: '`ImageGenerationInstructions` ContextualUserFragment from `codex-rs/core/src/context/image_generation_instructions.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as template.'
---
Generated images are saved to {} as {} by default.
If you need to use a generated image at another path, copy it and leave the original in place unless the user explicitly asks you to delete it.
