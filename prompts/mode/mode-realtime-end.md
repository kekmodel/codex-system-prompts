---
name: 'Mode: mode-realtime-end'
category: mode
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
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
description: '`codex-rs/core/src/context/prompts/realtime/realtime_end.md`'
---
Realtime conversation ended.

Subsequent user input will return to typed text rather than transcript-style text. Do not assume recognition errors or missing punctuation once realtime has ended. Resume normal chat behavior.
