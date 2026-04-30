---
name: 'Context fragment: UserShellCommand'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/user_shell_command.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/user_shell_command.rs:29
  struct: UserShellCommand
  role: user
  start_marker: <user_shell_command>
  end_marker: </user_shell_command>
  body_extraction: template
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 37
description: '`UserShellCommand` ContextualUserFragment from `codex-rs/core/src/context/user_shell_command.rs`.
  Role: ''user''. Markers: ''<user_shell_command>'' … ''</user_shell_command>''. body()
  captured as template.'
---
<user_shell_command>

<command>
{}
</command>
<result>
Exit code: {}
Duration: {:.4} seconds
Output:
{}
</result>

</user_shell_command>
