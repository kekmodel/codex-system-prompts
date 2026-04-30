---
name: 'Tool: shell_command parameters'
category: tool
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/tools/src/local_tool.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/local_tool.rs:255
  tool_name: shell_command
  parameter_count: 4
  parameters:
  - name: command
    schema_type: string
  - name: workdir
    schema_type: string
  - name: timeout_ms
    schema_type: number
  - name: login
    schema_type: boolean
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 124
description: Per-parameter `JsonSchema` descriptions for `shell_command` (4 parameters).
  Pass 1.7 (M9).
---
# Tool: `shell_command` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/local_tool.rs:255`). The model sees each `description` field on each parameter at tool-spec time.

## `command` (string)

The shell script to execute in the user's default shell

## `workdir` (string)

The working directory to execute the command in

## `timeout_ms` (number)

The timeout for the command in milliseconds

## `login` (boolean)

Whether to run the shell with login shell semantics. Defaults to true.
