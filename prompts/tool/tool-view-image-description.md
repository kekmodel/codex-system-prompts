---
name: 'Tool: view_image description'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/view_image.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/view_image.rs:28
  tool_name: view_image
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 36
description: Inline ToolSpec description for `view_image` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
View a local image from the filesystem (only use if given a full filepath by the user, and the image isn't already attached to the thread context within <image ...> tags).
