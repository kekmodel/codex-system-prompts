---
name: 'Mode: mode-compact-prompt'
category: mode
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/templates/compact/prompt.md
  kind: include_str
  reached_from:
  - compact.rs:42
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 89
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/compact/prompt.md`.
  Category: mode. Description will be refined at M5 review.'
---
You are performing a CONTEXT CHECKPOINT COMPACTION. Create a handoff summary for another LLM that will resume the task.

Include:
- Current progress and key decisions made
- Important context, constraints, or user preferences
- What remains to be done (clear next steps)
- Any critical data, examples, or references needed to continue

Be concise, structured, and focused on helping the next LLM seamlessly continue the work.
