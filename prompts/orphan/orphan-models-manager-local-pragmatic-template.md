---
name: 'Orphan: orphan-models-manager-local-pragmatic-template'
category: orphan
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/models-manager/src/model_info.rs
  kind: rust_const
  reached_from:
  - models-manager/src/model_info.rs:20
  symbol: LOCAL_PRAGMATIC_TEMPLATE
extraction:
  pass: 1.5
  method: rust_const_str
variables: []
tokens:
  o200k_base: 10
description: '`personality_pragmatic` variable body for the gpt-5.2-codex slug. Substituted
  into `{{ personality }}` placeholder when user picks the pragmatic personality.
  Inactive today (slug not registered).'
---
You are a deeply pragmatic, effective software engineer.