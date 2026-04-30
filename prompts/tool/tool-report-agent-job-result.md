---
name: 'Tool: report_agent_job_result'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_job_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_job_tool.rs:89
  tool_name: report_agent_job_result
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 164
description: '`report_agent_job_result` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "report_agent_job_result",
  "description": "Worker-only tool to report a result for an agent job item. Main agents should not call this.",
  "parameters": {
    "type": "object",
    "properties": {
      "job_id": {
        "type": "string",
        "description": "Identifier of the job."
      },
      "item_id": {
        "type": "string",
        "description": "Identifier of the job item."
      },
      "stop": {
        "type": "boolean",
        "description": "Optional. When true, cancels the remaining job items after this result is recorded."
      }
    },
    "additionalProperties": false
  }
}
```
