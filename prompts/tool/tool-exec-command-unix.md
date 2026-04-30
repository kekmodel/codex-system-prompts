---
name: 'Tool: exec_command'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/local_tool.rs:70
  tool_name: exec_command
  cfg_branch: unix
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 316
description: '`exec_command` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "exec_command",
  "description": "Runs a command in a PTY, returning output or a session ID for ongoing interaction.",
  "parameters": {
    "type": "object",
    "properties": {
      "cmd": {
        "type": "string",
        "description": "Shell command to execute."
      },
      "workdir": {
        "type": "string",
        "description": "Optional working directory to run the command in; defaults to the turn cwd."
      },
      "shell": {
        "type": "string",
        "description": "Shell binary to launch. Defaults to the user's default shell."
      },
      "tty": {
        "type": "boolean",
        "description": "Whether to allocate a TTY for the command. Defaults to false (plain pipes); set to true to open a PTY and access TTY process."
      },
      "yield_time_ms": {
        "type": "number",
        "description": "How long to wait (in milliseconds) for output before yielding."
      },
      "max_output_tokens": {
        "type": "number",
        "description": "Maximum number of tokens to return. Excess output will be truncated."
      },
      "login": {
        "type": "boolean",
        "description": "Whether to run the shell with -l/-i semantics. Defaults to true."
      }
    },
    "additionalProperties": false
  }
}
```
