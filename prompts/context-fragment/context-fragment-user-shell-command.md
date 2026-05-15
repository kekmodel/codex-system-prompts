---
name: 'Context fragment: UserShellCommand'
category: context-fragment
codex_version: rust-v0.129.0-alpha.2
codex_commit: 4a68cd56fbc355a8726f6410f890e1840d5ff74a
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
description: '`UserShellCommand` ContextualUserFragment.'
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
