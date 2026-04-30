---
name: 'Tool: view_image parameters'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/view_image.rs
  kind: rust_jsonschema_property
  reached_from:
  - tools/src/view_image.rs:28
  tool_name: view_image
  parameter_count: 2
  parameters:
  - name: path
    schema_type: string
  - name: detail
    schema_type: string
extraction:
  pass: 1.7
  method: rust_jsonschema_property
variables: []
tokens:
  o200k_base: 132
description: Per-parameter `JsonSchema` descriptions for `view_image` (2 parameters).
  Pass 1.7 (M9).
---
# Tool: `view_image` — parameters

Per-parameter descriptions extracted from the `JsonSchema` properties bag in the enclosing fn (`tools/src/view_image.rs:28`). The model sees each `description` field on each parameter at tool-spec time.

## `path` (string)

Local filesystem path to an image file

## `detail` (string)

Optional detail override. The only supported value is `original`; omit this field for default resized behavior. Use `original` to preserve the file's original resolution instead of resizing to fit. This is important when high-fidelity image perception or precise localization is needed, especially for CUA agents.
