---
name: 'Tool: spawn_agents_on_csv parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_job_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/agent_job_tool.rs:55
  tool_name: spawn_agents_on_csv
  parameter_count: 7
  parameters:
  - name: csv_path
    schema_type: string
  - name: instruction
    schema_type: string
  - name: id_column
    schema_type: string
  - name: output_csv_path
    schema_type: string
  - name: max_concurrency
    schema_type: number
  - name: max_workers
    schema_type: number
  - name: max_runtime_seconds
    schema_type: number
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 211
description: Per-parameter `JsonSchema` descriptions for `spawn_agents_on_csv` (7
  parameters). Pass 1.7 (M9).
---
# Tool: `spawn_agents_on_csv` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/agent_job_tool.rs:55`). The model sees each `description` field on each parameter at tool-spec time.

## `csv_path` (string)

Path to the CSV file containing input rows.

## `instruction` (string)

Instruction template to apply to each CSV row. Use {column_name} placeholders to inject values from the row.

## `id_column` (string)

Optional column name to use as stable item id.

## `output_csv_path` (string)

Optional output CSV path for exported results.

## `max_concurrency` (number)

Maximum concurrent workers for this job. Defaults to 16 and is capped by config.

## `max_workers` (number)

Alias for max_concurrency. Set to 1 to run sequentially.

## `max_runtime_seconds` (number)

Maximum runtime per worker before it is failed. Defaults to 1800 seconds.
