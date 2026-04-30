---
name: 'Context fragment: GuardianFollowupReviewReminder'
category: context-fragment
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/context/guardian_followup_review_reminder.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/guardian_followup_review_reminder.rs:6
  struct: GuardianFollowupReviewReminder
  role: developer
  start_marker: ''
  end_marker: ''
  body_extraction: function-body-source
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 89
description: '`GuardianFollowupReviewReminder` ContextualUserFragment from `codex-rs/core/src/context/guardian_followup_review_reminder.rs`.
  Role: ''developer''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
concat!(
            "Use prior reviews as context, not binding precedent. ",
            "Follow the Workspace Policy. ",
            "If the user explicitly approves a previously rejected action after being informed of the ",
            "concrete risks, set outcome to \"allow\" unless the policy explicitly disallows user ",
            "overwrites in such cases."
        )
        .to_string()
}
```

