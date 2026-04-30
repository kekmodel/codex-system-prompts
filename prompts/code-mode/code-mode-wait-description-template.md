---
name: 'Code-mode: code-mode-wait-description-template'
category: code-mode
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/code-mode/src/description.rs
  kind: rust_const
  reached_from:
  - code-mode/src/description.rs:37
  symbol: WAIT_DESCRIPTION_TEMPLATE
extraction:
  pass: 1.5
  method: rust_const_str
variables: []
tokens:
  o200k_base: 162
description: '`codex-rs/code-mode/src/description.rs::WAIT_DESCRIPTION_TEMPLATE`'
---
- Use `wait` only after `exec` returns `Script running with cell ID ...`.
- `cell_id` identifies the running `exec` cell to resume.
- `yield_time_ms` controls how long to wait for more output before yielding again. If omitted, `wait` uses its default wait timeout.
- `max_tokens` limits how much new output this wait call returns.
- `terminate: true` stops the running cell instead of waiting for more output.
- `wait` returns only the new output since the last yield, or the final completion or termination result for that cell.
- If the cell is still running, `wait` may yield again with the same `cell_id`.
- If the cell has already finished, `wait` returns the completed result and closes the cell.