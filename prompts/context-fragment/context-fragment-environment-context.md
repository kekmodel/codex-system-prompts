---
name: 'Context fragment: EnvironmentContext'
category: context-fragment
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/core/src/context/environment_context.rs
  kind: rust_contextual_user_fragment
  reached_from:
  - core/src/context/environment_context.rs:164
  struct: EnvironmentContext
  role: user
  start_marker: ''
  end_marker: ''
  body_extraction: function-body-source
extraction:
  pass: 1.6
  method: rust_contextual_user_fragment
variables: []
tokens:
  o200k_base: 335
description: '`EnvironmentContext` ContextualUserFragment from `codex-rs/core/src/context/environment_context.rs`.
  Role: ''user''. Markers: '''' … ''''. body() captured as function-body-source.'
---
```rust
fn body(&self) -> String {
let mut lines = Vec::new();
        if let Some(cwd) = &self.cwd {
            lines.push(format!("  <cwd>{}</cwd>", cwd.to_string_lossy()));
        }

        lines.push(format!("  <shell>{}</shell>", self.shell));
        if let Some(current_date) = &self.current_date {
            lines.push(format!("  <current_date>{current_date}</current_date>"));
        }
        if let Some(timezone) = &self.timezone {
            lines.push(format!("  <timezone>{timezone}</timezone>"));
        }
        match &self.network {
            Some(network) => {
                lines.push("  <network enabled=\"true\">".to_string());
                for allowed in &network.allowed_domains {
                    lines.push(format!("    <allowed>{allowed}</allowed>"));
                }
                for denied in &network.denied_domains {
                    lines.push(format!("    <denied>{denied}</denied>"));
                }
                lines.push("  </network>".to_string());
            }
            None => {
                // TODO(mbolin): Include this line if it helps the model.
                // lines.push("  <network enabled=\"false\" />".to_string());
            }
        }
        if let Some(subagents) = &self.subagents {
            lines.push("  <subagents>".to_string());
            lines.extend(subagents.lines().map(|line| format!("    {line}")));
            lines.push("  </subagents>".to_string());
        }
        format!("\n{}\n", lines.join("\n"))
}
```

