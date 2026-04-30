---
name: 'Tool: report_agent_job_result parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_job_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/agent_job_tool.rs:89
  tool_name: report_agent_job_result
  parameter_count: 3
  parameters:
  - name: job_id
    schema_type: string
  - name: item_id
    schema_type: string
  - name: stop
    schema_type: boolean
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 107
description: Per-parameter `JsonSchema` descriptions for `report_agent_job_result`
  (3 parameters). Pass 1.7 (M9).
---
# Tool: `report_agent_job_result` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/agent_job_tool.rs:89`). The model sees each `description` field on each parameter at tool-spec time.

## `job_id` (string)

Identifier of the job.

## `item_id` (string)

Identifier of the job item.

## `stop` (boolean)

Optional. When true, cancels the remaining job items after this result is recorded.
