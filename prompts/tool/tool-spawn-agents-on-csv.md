---
name: 'Tool: spawn_agents_on_csv'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_job_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_job_tool.rs:55
  tool_name: spawn_agents_on_csv
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 374
description: '`spawn_agents_on_csv` ToolSpec.'
---
{
  "type": "function",
  "name": "spawn_agents_on_csv",
  "description": "Process a CSV by spawning one worker sub-agent per row. The instruction string is a template where `{column}` placeholders are replaced with row values. Each worker must call `report_agent_job_result` with a JSON object (matching `output_schema` when provided); missing reports are treated as failures. This call blocks until all rows finish and automatically exports results to `output_csv_path` (or a default path).",
  "parameters": {
    "type": "object",
    "properties": {
      "csv_path": {
        "type": "string",
        "description": "Path to the CSV file containing input rows."
      },
      "instruction": {
        "type": "string",
        "description": "Instruction template to apply to each CSV row. Use {column_name} placeholders to inject values from the row."
      },
      "id_column": {
        "type": "string",
        "description": "Optional column name to use as stable item id."
      },
      "output_csv_path": {
        "type": "string",
        "description": "Optional output CSV path for exported results."
      },
      "max_concurrency": {
        "type": "number",
        "description": "Maximum concurrent workers for this job. Defaults to 16 and is capped by config."
      },
      "max_workers": {
        "type": "number",
        "description": "Alias for max_concurrency. Set to 1 to run sequentially."
      },
      "max_runtime_seconds": {
        "type": "number",
        "description": "Maximum runtime per worker before it is failed. Defaults to 1800 seconds."
      }
    },
    "additionalProperties": false
  }
}
