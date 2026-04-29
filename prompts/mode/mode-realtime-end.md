---
name: 'Mode: mode-realtime-end'
category: mode
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/src/context/prompts/realtime/realtime_end.md
  kind: include_str
  reached_from:
  - core/src/context/realtime_end_instructions.rs:5
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
