---
name: 'Tool: spawn_agents_on_csv description'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/agent_job_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_job_tool.rs:55
  tool_name: spawn_agents_on_csv
  description_kind: static_plain
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 82
description: Inline ToolSpec description for `spawn_agents_on_csv` (literal `static_plain`).
  Captured by Pass 1.7 (M9).
---
Process a CSV by spawning one worker sub-agent per row. The instruction string is a template where `{column}` placeholders are replaced with row values. Each worker must call `report_agent_job_result` with a JSON object (matching `output_schema` when provided); missing reports are treated as failures. This call blocks until all rows finish and automatically exports results to `output_csv_path` (or a default path).
