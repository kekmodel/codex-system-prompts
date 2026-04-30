---
name: 'Tool: view_image'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/view_image.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/view_image.rs:28
  tool_name: view_image
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 196
description: '`view_image` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "view_image",
  "description": "View a local image from the filesystem (only use if given a full filepath by the user, and the image isn't already attached to the thread context within <image ...> tags).",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Local filesystem path to an image file"
      },
      "detail": {
        "type": "string",
        "description": "Optional detail override. The only supported value is `original`; omit this field for default resized behavior. Use `original` to preserve the file's original resolution instead of resizing to fit. This is important when high-fidelity image perception or precise localization is needed, especially for CUA agents."
      }
    },
    "additionalProperties": false
  }
}
```
