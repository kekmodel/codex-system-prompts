---
name: 'Tool: exec_command parameters'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/local_tool.rs:70
  tool_name: exec_command
  parameter_count: 7
  parameters:
  - name: cmd
    schema_type: string
  - name: workdir
    schema_type: string
  - name: shell
    schema_type: string
  - name: tty
    schema_type: boolean
  - name: yield_time_ms
    schema_type: number
  - name: max_output_tokens
    schema_type: number
  - name: login
    schema_type: boolean
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 211
description: Per-parameter `JsonSchema` descriptions for `exec_command` (7 parameters).
  Pass 1.7 (M9).
---
# Tool: `exec_command` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/local_tool.rs:70`). The model sees each `description` field on each parameter at tool-spec time.

## `cmd` (string)

Shell command to execute.

## `workdir` (string)

Optional working directory to run the command in; defaults to the turn cwd.

## `shell` (string)

Shell binary to launch. Defaults to the user's default shell.

## `tty` (boolean)

Whether to allocate a TTY for the command. Defaults to false (plain pipes); set to true to open a PTY and access TTY process.

## `yield_time_ms` (number)

How long to wait (in milliseconds) for output before yielding.

## `max_output_tokens` (number)

Maximum number of tokens to return. Excess output will be truncated.

## `login` (boolean)

Whether to run the shell with -l/-i semantics. Defaults to true.
