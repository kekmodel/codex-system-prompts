---
name: 'Tool: shell'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/local_tool.rs:185
  tool_name: shell
  cfg_branch: unix
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 179
description: '`shell` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "shell",
  "description": "Runs a shell command and returns its output.\n- The arguments to `shell` will be passed to execvp(). Most terminal commands should be prefixed with [\"bash\", \"-lc\"].\n- Always set the `workdir` param when using the shell function. Do not use `cd` unless absolutely necessary.",
  "parameters": {
    "type": "object",
    "properties": {
      "workdir": {
        "type": "string",
        "description": "The working directory to execute the command in"
      },
      "timeout_ms": {
        "type": "number",
        "description": "The timeout for the command in milliseconds"
      }
    },
    "additionalProperties": false
  }
}
```
