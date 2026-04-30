---
name: 'Orphan: orphan-models-manager-local-friendly-template'
category: orphan
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/models-manager/src/model_info.rs
  kind: rust_const
  reached_from:
  - models-manager/src/model_info.rs:18
  symbol: LOCAL_FRIENDLY_TEMPLATE
extraction:
  pass: 1.5
  method: rust_const_str
variables: []
tokens:
  o200k_base: 16
description: '`personality_friendly` variable body for the gpt-5.2-codex slug. Substituted
  into `{{ personality }}` placeholder when user picks the friendly personality. Inactive
  today (slug not registered).'
---
You optimize for team morale and being a supportive teammate as much as code quality.