---
name: 'Context fragment: AvailablePluginsInstructions'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/available_plugins_instructions.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/available_plugins_instructions.rs:24
  struct: AvailablePluginsInstructions
  role: developer
  start_marker: ''
  end_marker: ''
  body_extraction: function-body-source
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 332
description: '`AvailablePluginsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_plugins_instructions.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
let mut lines = vec![
            "## Plugins".to_string(),
            "A plugin is a local bundle of skills, MCP servers, and apps. Below is the list of plugins that are enabled and available in this session.".to_string(),
            "### Available plugins".to_string(),
        ];

        lines.extend(
            self.plugins
                .iter()
                .map(|plugin| match plugin.description.as_deref() {
                    Some(description) => format!("- `{}`: {description}", plugin.display_name),
                    None => format!("- `{}`", plugin.display_name),
                }),
        );

        lines.push("### How to use plugins".to_string());
        lines.push(
            r###"- Discovery: The list above is the plugins available in this session.
- Skill naming: If a plugin contributes skills, those skill entries are prefixed with `plugin_name:` in the Skills list.
- Trigger rules: If the user explicitly names a plugin, prefer capabilities associated with that plugin for that turn.
- Relationship to capabilities: Plugins are not invoked directly. Use their underlying skills, MCP tools, and app tools to help solve the task.
- Preference: When a relevant plugin is available, prefer using capabilities associated with that plugin over standalone capabilities that provide similar functionality.
- Missing/blocked: If the user requests a plugin that is not listed above, or the plugin does not have relevant callable capabilities for the task, say so briefly and continue with the best fallback."###
                .to_string(),
        );

        format!("\n{}\n", lines.join("\n"))
}
```

