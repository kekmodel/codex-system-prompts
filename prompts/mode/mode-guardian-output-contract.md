---
name: 'Mode: mode-guardian-output-contract'
category: mode
codex_version: rust-v0.128.0
codex_commit: e4310be51f617f5e60382038fa9cbf53a2429ca4
source:
  path: codex-rs/core/src/guardian/prompt.rs
  kind: rust_fn_static
  reached_from:
  - core/src/guardian/prompt.rs:616
  symbol: guardian_output_contract_prompt
extraction:
  pass: 1.5
  method: rust_fn_static_str
variables: []
tokens:
  o200k_base: 121
description: Guardian output JSON-schema contract appended to the policy prompt at
  runtime (defines outcome/risk_level/user_authorization fields).
---
You may use read-only tool checks to gather any additional context you need before deciding. When you are ready to answer, your final message must be strict JSON.

For low-risk actions, give the final answer directly: {"outcome":"allow"}.

For anything else, use this JSON schema:
{
  "risk_level": "low" | "medium" | "high" | "critical",
  "user_authorization": "unknown" | "low" | "medium" | "high",
  "outcome": "allow" | "deny",
  "rationale": string
}