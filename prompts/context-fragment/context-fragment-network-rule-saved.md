---
name: 'Context fragment: NetworkRuleSaved'
category: context-fragment
codex_version: rust-v0.126.0-alpha.12
codex_commit: ebdf3a878c8c7253504599bd384cd421a4e548c1
source:
  path: codex-rs/core/src/context/network_rule_saved.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/network_rule_saved.rs:20
  struct: NetworkRuleSaved
  role: developer
  start_marker: ''
  end_marker: ''
  body_extraction: function-body-source
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 85
description: '`NetworkRuleSaved` ContextualUserFragment from `codex-rs/core/src/context/network_rule_saved.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
let (action, list_name) = match self.action {
            NetworkPolicyRuleAction::Allow => ("Allowed", "allowlist"),
            NetworkPolicyRuleAction::Deny => ("Denied", "denylist"),
        };
        format!(
            "{action} network rule saved in execpolicy ({list_name}): {}",
            self.host
        )
}
```

