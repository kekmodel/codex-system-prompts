---
name: 'Tool: exec_command description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/local_tool.rs:70
  tool_name: exec_command
  description_kind: cfg_conditional
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 69
description: Inline ToolSpec description for `exec_command` — `cfg!(windows)` conditional.
  Both branches captured side-by-side. Pass 1.7 (M9).
---
## Windows branch (`cfg!(windows)` true)

Runs a command in a PTY, returning output or a session ID for ongoing interaction.

{}

_format!() args: `windows_shell_guidance()`_

## Unix branch (`cfg!(windows)` false)

Runs a command in a PTY, returning output or a session ID for ongoing interaction.
