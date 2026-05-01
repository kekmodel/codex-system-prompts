---
name: 'Tool: shell_command'
category: tool
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/local_tool.rs:255
  tool_name: shell_command
  cfg_branch: unix
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 211
description: '`shell_command` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "shell_command",
  "description": "Runs a shell command and returns its output.\n- Always set the `workdir` param when using the shell_command function. Do not use `cd` unless absolutely necessary.",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "The shell script to execute in the user's default shell"
      },
      "workdir": {
        "type": "string",
        "description": "The working directory to execute the command in"
      },
      "timeout_ms": {
        "type": "number",
        "description": "The timeout for the command in milliseconds"
      },
      "login": {
        "type": "boolean",
        "description": "Whether to run the shell with login shell semantics. Defaults to true."
      }
    },
    "additionalProperties": false
  }
}
```
