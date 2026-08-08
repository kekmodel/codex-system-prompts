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
  cfg_branch: windows
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 384
description: '`shell` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "shell",
  "description": "Runs a Powershell command (Windows) and returns its output. Arguments to `shell` will be passed to CreateProcessW(). Most commands should be prefixed with [\"powershell.exe\", \"-Command\"].\n\nExamples of valid command strings:\n\n- ls -a (show hidden): [\"powershell.exe\", \"-Command\", \"Get-ChildItem -Force\"]\n- recursive find by name: [\"powershell.exe\", \"-Command\", \"Get-ChildItem -Recurse -Filter *.py\"]\n- recursive grep: [\"powershell.exe\", \"-Command\", \"Get-ChildItem -Path C:\\\\myrepo -Recurse | Select-String -Pattern 'TODO' -CaseSensitive\"]\n- ps aux | grep python: [\"powershell.exe\", \"-Command\", \"Get-Process | Where-Object {{ $_.ProcessName -like '*python*' }}\"]\n- setting an env var: [\"powershell.exe\", \"-Command\", \"$env:FOO='bar'; echo $env:FOO\"]\n- running an inline Python script: [\"powershell.exe\", \"-Command\", \"@'\\\\nprint('Hello, world!')\\\\n'@ | python -\"]\n\n{}",
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
