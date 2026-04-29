---
name: 'Data: data-apply-patch-grammar'
category: data
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/tools/src/tool_apply_patch.lark
  kind: include_str
  reached_from:
  - tools/src/apply_patch_tool.rs:10
extraction:
  pass: 1
  method: file
variables: []
tokens:
  o200k_base: 173
description: 'Auto-extracted by Pass 3 (M2) from `codex-rs/tools/src/tool_apply_patch.lark`.
  Category: data. Description will be refined at M5 review.'
---
start: begin_patch hunk+ end_patch
begin_patch: "*** Begin Patch" LF
end_patch: "*** End Patch" LF?

hunk: add_hunk | delete_hunk | update_hunk
add_hunk: "*** Add File: " filename LF add_line+
delete_hunk: "*** Delete File: " filename LF
update_hunk: "*** Update File: " filename LF change_move? change?

filename: /(.+)/
add_line: "+" /(.*)/ LF -> line

change_move: "*** Move to: " filename LF
change: (change_context | change_line)+ eof_line?
change_context: ("@@" | "@@ " /(.+)/) LF
change_line: ("+" | "-" | " ") /(.*)/ LF
eof_line: "*** End of File" LF

%import common.LF
