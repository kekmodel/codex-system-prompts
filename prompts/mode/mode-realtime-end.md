---
name: 'Mode: mode-realtime-end'
category: mode
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/prompts/realtime/realtime_end.md
  kind: include_str
  reached_from:
  - realtime_end_instructions.rs:5
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 38
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/realtime/realtime_end.md`.
  Category: mode. Description will be refined at M5 review.'
---
Realtime conversation ended.

Subsequent user input will return to typed text rather than transcript-style text. Do not assume recognition errors or missing punctuation once realtime has ended. Resume normal chat behavior.
