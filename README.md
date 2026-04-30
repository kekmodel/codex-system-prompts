# codex-system-prompts

> Mirror of codex `rust-v0.126.0-alpha.12`. See [SPEC.md](./SPEC.md) for the full specification, [DISCLAIMER.md](./DISCLAIMER.md) for legal context, and [CHANGELOG.md](./CHANGELOG.md) for per-tag prompt diffs.

Unofficial, version-tracked mirror of the prompt strings shipped by OpenAI's [Codex CLI](https://github.com/openai/codex).

Modeled on Piebald AI's [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts), adapted to Codex's hybrid prompt architecture (per-model `base_instructions` monoliths + `ContextualUserFragment` wrappers + programmatic `format!`-built tool descriptions).

## Layout

| Path | Purpose |
|---|---|
| `prompts/` | Extracted prompt files, by category. The auto-generated index below lists every captured file with its token count. |
| `prompts/feature-gated/<flag>/` | Non-default-feature prompts (per SPEC §2.1.1) |
| `extractor/` | Extraction tooling — Python orchestrator (Pass 1/1.5/1.6/2/3/4/5) + (optional) Rust shim |
| `data/upstream-tags.md` | Upstream→mirror tag mapping (lossless, including silently skipped tags) |
| `tests/snapshot-cross-check/` | Snapshot-based verification (SPEC §2.5) |
| `SPEC.md` | Specification (v0.7 current) |
| `SPEC_REVIEW_v0.2.md` | Tier-1 + Tier-2 review notes that drove v0.3 hardening |
| `CHANGELOG.md` | Per-mirror-tag prompt diffs, Piebald-style |

## How updates happen

Per [SPEC §8](./SPEC.md#8-automation), two equivalent paths trigger re-extraction on a new upstream `rust-v*` tag, both sharing the same deterministic `extractor extract` entry:

- **Manual (Claude-driven)** — ask Claude in this repo: *"Codex 최신 버전으로 업데이트해."* Claude runs the extractor in dry-run, presents a paginated summary, and on approval commits + (selectively) tags.
- **Automated (GH Action)** — hourly poll of upstream tags, opens auto-PR for human merge.

## Versioning model

- Mirror tags are a **sparse subset** of upstream tags — only tags with material prompt diff get a mirror commit + tag (SPEC §12.3 / T2.4).
- The complete upstream tag history (including silent skips) lives in [`data/upstream-tags.md`](./data/upstream-tags.md).
- Working tree is always at the latest extracted tag; historical inspection via `git checkout <tag>`.

## Token-count caveat

Token counts in this index use `tiktoken`'s `o200k_base` (gpt-4o / o-series / gpt-5.x). For variable-bearing prompts (most of Codex's content), the count is the *template* count with placeholders intact. **Real session tokens can be 2–5× higher** when variables expand at runtime — for instance, the `<personality_spec>` body interpolates `{}` to a multi-hundred-token personality spec, and the `<environment_context>` fragment interpolates cwd / shell / agents_md / subagents content. See [SPEC §7](./SPEC.md#7-token-accounting-v03-reframed--t23) for the full framing.

<!-- AUTO-GENERATED-START -->

## Coverage

Per [SPEC §2.5](./SPEC.md#25-verification--two-layers-t13-refined-v05).

### Layer A — Structural mapping

**32 snapshots**, **11 unique placeholders** (7 captured-static, 3 runtime, 1 out-of-scope, 0 deferred, 0 unmapped)

### Layer B — Completeness

| Source | Captured | Total | Missing |
|---|---:|---:|---:|
| Auto-include (`include_str!`/`include_bytes!`) | 38 | 38 | 0 |
| `models.json` fan-out | 6 | 6 | 0 |
| Allow-list (Pass 1.5) | 11 | 11 | 0 |

### Auxiliary

| Check | Files | Issues |
|---|---:|---:|
| Token-count drift | 91 | 0 |
| Frontmatter schema | 91 | 0 |

**✓ All verification checks passed.**

> Neither layer proves complete capture. Layer A only validates *what tests exercise*; Layer B is bounded by allow-list curation. See SPEC §2.5 for limits.

## Captured prompt corpus

**91 files** at codex `rust-v0.128.0-alpha.1`, totaling **93,866 tokens** (o200k_base, template counts — see *Token-count caveat* above).

### `prompts/base-instructions/` — 8 files, 28,913 tokens

_Per-model `base_instructions` (fanned out from `models.json`) + fallbacks._

- [`base-instructions-codex-auto-review.md`](./prompts/base-instructions/base-instructions-codex-auto-review.md) — **2,991** tokens — Per-model `base_instructions` for slug `codex-auto-review`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/5/base_instructions.
- [`base-instructions-default.md`](./prompts/base-instructions/base-instructions-default.md) — **4,371** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/protocol/src/prompts/base_instructions/default.md`. Category: base-instructions. Description will be refined at M5 review.
- [`base-instructions-fallback.md`](./prompts/base-instructions/base-instructions-fallback.md) — **4,371** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/models-manager/prompt.md`. Category: base-instructions. Description will be refined at M5 review.
- [`base-instructions-gpt-5.2.md`](./prompts/base-instructions/base-instructions-gpt-5.2.md) — **4,570** tokens — Per-model `base_instructions` for slug `gpt-5.2`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/4/base_instructions.
- [`base-instructions-gpt-5.3-codex.md`](./prompts/base-instructions/base-instructions-gpt-5.3-codex.md) — **2,551** tokens — Per-model `base_instructions` for slug `gpt-5.3-codex`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/3/base_instructions.
- [`base-instructions-gpt-5.4-mini.md`](./prompts/base-instructions/base-instructions-gpt-5.4-mini.md) — **2,639** tokens — Per-model `base_instructions` for slug `gpt-5.4-mini`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/2/base_instructions.
- [`base-instructions-gpt-5.4.md`](./prompts/base-instructions/base-instructions-gpt-5.4.md) — **2,991** tokens — Per-model `base_instructions` for slug `gpt-5.4`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/1/base_instructions.
- [`base-instructions-gpt-5.5.md`](./prompts/base-instructions/base-instructions-gpt-5.5.md) — **4,429** tokens — Per-model `base_instructions` for slug `gpt-5.5`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/0/base_instructions.

### `prompts/mode/` — 17 files, 8,944 tokens

_Mode-specific prompts: review, compact, realtime, goals, guardian, collaboration._

- [`mode-collab-default.md`](./prompts/mode/mode-collab-default.md) — **173** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/default.md`. Category: mode. Description will be refined at M5 review.
- [`mode-collab-execute.md`](./prompts/mode/mode-collab-execute.md) — **763** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/execute.md`. Category: mode. Description will be refined at M5 review.
- [`mode-collab-pair-programming.md`](./prompts/mode/mode-collab-pair-programming.md) — **222** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/pair_programming.md`. Category: mode. Description will be refined at M5 review.
- [`mode-collab-plan.md`](./prompts/mode/mode-collab-plan.md) — **1,804** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/plan.md`. Category: mode. Description will be refined at M5 review.
- [`mode-compact-prompt.md`](./prompts/mode/mode-compact-prompt.md) — **89** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/compact/prompt.md`. Category: mode. Description will be refined at M5 review.
- [`mode-compact-summary-prefix.md`](./prompts/mode/mode-compact-summary-prefix.md) — **77** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/compact/summary_prefix.md`. Category: mode. Description will be refined at M5 review.
- [`mode-goal-budget-limit.md`](./prompts/mode/mode-goal-budget-limit.md) — **139** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/goals/budget_limit.md`. Category: mode. Description will be refined at M5 review.
- [`mode-goal-continuation.md`](./prompts/mode/mode-goal-continuation.md) — **465** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/goals/continuation.md`. Category: mode. Description will be refined at M5 review.
- [`mode-guardian-output-contract.md`](./prompts/mode/mode-guardian-output-contract.md) — **121** tokens — Guardian output JSON-schema contract appended to the policy prompt at runtime (defines outcome/risk_level/user_authorization fields).
- [`mode-guardian-policy-template.md`](./prompts/mode/mode-guardian-policy-template.md) — **1,416** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/guardian/policy_template.md`. Category: mode. Description will be refined at M5 review.
- [`mode-guardian-policy.md`](./prompts/mode/mode-guardian-policy.md) — **1,042** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/guardian/policy.md`. Category: mode. Description will be refined at M5 review.
- [`mode-realtime-backend.md`](./prompts/mode/mode-realtime-backend.md) — **954** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/realtime/backend_prompt.md`. Category: mode. Description will be refined at M5 review.
- [`mode-realtime-end.md`](./prompts/mode/mode-realtime-end.md) — **38** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/realtime/realtime_end.md`. Category: mode. Description will be refined at M5 review.
- [`mode-realtime-start.md`](./prompts/mode/mode-realtime-start.md) — **145** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/realtime/realtime_start.md`. Category: mode. Description will be refined at M5 review.
- [`mode-review-exit-interrupted.md`](./prompts/mode/mode-review-exit-interrupted.md) — **67** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_interrupted.xml`. Category: mode. Description will be refined at M5 review.
- [`mode-review-exit-success.md`](./prompts/mode/mode-review-exit-success.md) — **59** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_success.xml`. Category: mode. Description will be refined at M5 review.
- [`mode-review.md`](./prompts/mode/mode-review.md) — **1,370** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/review_prompt.md`. Category: mode. Description will be refined at M5 review.

### `prompts/permission/` — 8 files, 1,357 tokens

_Approval-policy and sandbox-mode prompt fragments._

- [`permission-approval-never.md`](./prompts/permission/permission-approval-never.md) — **23** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/never.md`. Category: permission. Description will be refined at M5 review.
- [`permission-approval-on-failure.md`](./prompts/permission/permission-approval-on-failure.md) — **60** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_failure.md`. Category: permission. Description will be refined at M5 review.
- [`permission-approval-on-request-rule-request-permission.md`](./prompts/permission/permission-approval-on-request-rule-request-permission.md) — **333** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_request_rule_request_permission.md`. Category: permission. Description will be refined at M5 review.
- [`permission-approval-on-request.md`](./prompts/permission/permission-approval-on-request.md) — **758** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_request.md`. Category: permission. Description will be refined at M5 review.
- [`permission-approval-unless-trusted.md`](./prompts/permission/permission-approval-unless-trusted.md) — **50** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/unless_trusted.md`. Category: permission. Description will be refined at M5 review.
- [`permission-sandbox-danger-full-access.md`](./prompts/permission/permission-sandbox-danger-full-access.md) — **40** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/danger_full_access.md`. Category: permission. Description will be refined at M5 review.
- [`permission-sandbox-read-only.md`](./prompts/permission/permission-sandbox-read-only.md) — **36** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/read_only.md`. Category: permission. Description will be refined at M5 review.
- [`permission-sandbox-workspace-write.md`](./prompts/permission/permission-sandbox-workspace-write.md) — **57** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/workspace_write.md`. Category: permission. Description will be refined at M5 review.

### `prompts/context-fragment/` — 22 files, 1,304 tokens

_ContextualUserFragment wrappers — XML-tagged user-message injections._

- [`context-fragment-approved-command-prefix-saved.md`](./prompts/context-fragment/context-fragment-approved-command-prefix-saved.md) — **6** tokens — `ApprovedCommandPrefixSaved` ContextualUserFragment from `codex-rs/core/src/context/approved_command_prefix_saved.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template.
- [`context-fragment-apps-instructions.md`](./prompts/context-fragment/context-fragment-apps-instructions.md) — **143** tokens — `AppsInstructions` ContextualUserFragment from `codex-rs/core/src/context/apps_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template.
- [`context-fragment-available-plugins-instructions.md`](./prompts/context-fragment/context-fragment-available-plugins-instructions.md) — **332** tokens — `AvailablePluginsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_plugins_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-available-skills-instructions.md`](./prompts/context-fragment/context-fragment-available-skills-instructions.md) — **30** tokens — `AvailableSkillsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_skills_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-collaboration-mode-instructions.md`](./prompts/context-fragment/context-fragment-collaboration-mode-instructions.md) — **18** tokens — `CollaborationModeInstructions` ContextualUserFragment from `codex-rs/core/src/context/collaboration_mode_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-environment-context.md`](./prompts/context-fragment/context-fragment-environment-context.md) — **335** tokens — `EnvironmentContext` ContextualUserFragment from `codex-rs/core/src/context/environment_context.rs`. Role: 'user'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-guardian-followup-review-reminder.md`](./prompts/context-fragment/context-fragment-guardian-followup-review-reminder.md) — **89** tokens — `GuardianFollowupReviewReminder` ContextualUserFragment from `codex-rs/core/src/context/guardian_followup_review_reminder.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-hook-additional-context.md`](./prompts/context-fragment/context-fragment-hook-additional-context.md) — **18** tokens — `HookAdditionalContext` ContextualUserFragment from `codex-rs/core/src/context/hook_additional_context.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-image-generation-instructions.md`](./prompts/context-fragment/context-fragment-image-generation-instructions.md) — **41** tokens — `ImageGenerationInstructions` ContextualUserFragment from `codex-rs/core/src/context/image_generation_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template.
- [`context-fragment-model-switch-instructions.md`](./prompts/context-fragment/context-fragment-model-switch-instructions.md) — **28** tokens — `ModelSwitchInstructions` ContextualUserFragment from `codex-rs/core/src/context/model_switch_instructions.rs`. Role: 'developer'. Markers: '<model_switch>' … '</model_switch>'. body() captured as template.
- [`context-fragment-network-rule-saved.md`](./prompts/context-fragment/context-fragment-network-rule-saved.md) — **85** tokens — `NetworkRuleSaved` ContextualUserFragment from `codex-rs/core/src/context/network_rule_saved.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-permissions-instructions.md`](./prompts/context-fragment/context-fragment-permissions-instructions.md) — **26** tokens — `PermissionsInstructions` ContextualUserFragment from `codex-rs/core/src/context/permissions_instructions.rs`. Role: 'developer'. Markers: '<permissions instructions>' … '</permissions instructions>'. body() captured as function-body-source…
- [`context-fragment-personality-spec-instructions.md`](./prompts/context-fragment/context-fragment-personality-spec-instructions.md) — **31** tokens — `PersonalitySpecInstructions` ContextualUserFragment from `codex-rs/core/src/context/personality_spec_instructions.rs`. Role: 'developer'. Markers: '<personality_spec>' … '</personality_spec>'. body() captured as template.
- [`context-fragment-plugin-instructions.md`](./prompts/context-fragment/context-fragment-plugin-instructions.md) — **18** tokens — `PluginInstructions` ContextualUserFragment from `codex-rs/core/src/context/plugin_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source.
- [`context-fragment-realtime-end-instructions.md`](./prompts/context-fragment/context-fragment-realtime-end-instructions.md) — **5** tokens — `RealtimeEndInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_end_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template.
- [`context-fragment-realtime-start-instructions.md`](./prompts/context-fragment/context-fragment-realtime-start-instructions.md) — **2** tokens — `RealtimeStartInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_start_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template.
- [`context-fragment-realtime-start-with-instructions.md`](./prompts/context-fragment/context-fragment-realtime-start-with-instructions.md) — **2** tokens — `RealtimeStartWithInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_start_with_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template.
- [`context-fragment-skill-instructions.md`](./prompts/context-fragment/context-fragment-skill-instructions.md) — **19** tokens — `SkillInstructions` ContextualUserFragment from `codex-rs/core/src/context/skill_instructions.rs`. Role: 'user'. Markers: '<skill>' … '</skill>'. body() captured as template.
- [`context-fragment-subagent-notification.md`](./prompts/context-fragment/context-fragment-subagent-notification.md) — **11** tokens — `SubagentNotification` ContextualUserFragment from `codex-rs/core/src/context/subagent_notification.rs`. Role: 'user'. Markers: '<subagent_notification>' … '</subagent_notification>'. body() captured as template.
- [`context-fragment-turn-aborted.md`](./prompts/context-fragment/context-fragment-turn-aborted.md) — **11** tokens — `TurnAborted` ContextualUserFragment from `codex-rs/core/src/context/turn_aborted.rs`. Role: 'user'. Markers: '<turn_aborted>' … '</turn_aborted>'. body() captured as template.
- [`context-fragment-user-instructions.md`](./prompts/context-fragment/context-fragment-user-instructions.md) — **17** tokens — `UserInstructions` ContextualUserFragment from `codex-rs/core/src/context/user_instructions.rs`. Role: 'user'. Markers: '# AGENTS.md instructions for ' … '</INSTRUCTIONS>'. body() captured as template.
- [`context-fragment-user-shell-command.md`](./prompts/context-fragment/context-fragment-user-shell-command.md) — **37** tokens — `UserShellCommand` ContextualUserFragment from `codex-rs/core/src/context/user_shell_command.rs`. Role: 'user'. Markers: '<user_shell_command>' … '</user_shell_command>'. body() captured as template.

### `prompts/tool/` — 5 files, 8,435 tokens

_Built-in tool descriptions (apply_patch, spawn_agent guidance, MCP message templates)._

- [`tool-apply-patch-instructions.md`](./prompts/tool/tool-apply-patch-instructions.md) — **752** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/apply-patch/apply_patch_tool_instructions.md`. Category: tool. Description will be refined at M5 review.
- [`tool-apply-patch-json-description.md`](./prompts/tool/tool-apply-patch-json-description.md) — **706** tokens — JSON-API variant of the apply_patch tool description (paired with apply_patch_tool_instructions.md / apply_patch.lark grammar).
- [`tool-consequential-message-templates.md`](./prompts/tool/tool-consequential-message-templates.md) — **6,900** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/consequential_tool_message_templates.json`. Category: tool. Description will be refined at M5 review.
- [`tool-spawn-agent-inherited-model-guidance.md`](./prompts/tool/tool-spawn-agent-inherited-model-guidance.md) — **33** tokens — Guidance attached to spawn_agent's `model` parameter — inheritance default rule.
- [`tool-spawn-agent-model-override-description.md`](./prompts/tool/tool-spawn-agent-model-override-description.md) — **44** tokens — Description for spawn_agent's optional `model` override parameter.

### `prompts/agent/` — 4 files, 852 tokens

_Built-in agent roles + agent_names list + hierarchical-agent message._

- [`agent-builtin-awaiter.md`](./prompts/agent/agent-builtin-awaiter.md) — **259** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/agent/builtins/awaiter.toml`. Category: agent. Description will be refined at M5 review.
- [`agent-hierarchical-message.md`](./prompts/agent/agent-hierarchical-message.md) — **209** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/hierarchical_agents_message.md`. Category: agent. Description will be refined at M5 review.
- [`agent-role-explorer.md`](./prompts/agent/agent-role-explorer.md) — **188** tokens — Explorer role description — inline string in role.rs DEFAULT_ROLE_CONFIG table.
- [`agent-role-worker.md`](./prompts/agent/agent-role-worker.md) — **196** tokens — Worker role description — inline string in role.rs DEFAULT_ROLE_CONFIG table.

### `prompts/memory/` — 4 files, 18,057 tokens

_/memories skill prompts._

- [`memory-read-read-path.md`](./prompts/memory/memory-read-read-path.md) — **1,532** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/read/templates/memories/read_path.md`. Category: memory. Description will be refined at M5 review.
- [`memory-write-consolidation.md`](./prompts/memory/memory-write-consolidation.md) — **10,379** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/consolidation.md`. Category: memory. Description will be refined at M5 review.
- [`memory-write-stage-one-input.md`](./prompts/memory/memory-write-stage-one-input.md) — **86** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/stage_one_input.md`. Category: memory. Description will be refined at M5 review.
- [`memory-write-stage-one-system.md`](./prompts/memory/memory-write-stage-one-system.md) — **6,060** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/stage_one_system.md`. Category: memory. Description will be refined at M5 review.

### `prompts/code-mode/` — 5 files, 1,427 tokens

_Code-mode (JS-orchestration tool) description constants._

- [`code-mode-deferred-nested-tools-guidance.md`](./prompts/code-mode/code-mode-deferred-nested-tools-guidance.md) — **76** tokens — Guidance noting that some nested MCP/app tools may be omitted from the description but are still callable via `tools` / `ALL_TOOLS`.
- [`code-mode-exec-description-template.md`](./prompts/code-mode/code-mode-exec-description-template.md) — **700** tokens — Code-mode `exec` tool description template — programmatic preface for the JS-orchestration `exec` tool.
- [`code-mode-mcp-typescript-preamble.md`](./prompts/code-mode/code-mode-mcp-typescript-preamble.md) — **413** tokens — TypeScript schema preamble injected into code-mode tool description for the MCP nested-tool API.
- [`code-mode-only-preface.md`](./prompts/code-mode/code-mode-only-preface.md) — **76** tokens — Preface added when code-mode is the only tool exposure (no other MCP tools listed).
- [`code-mode-wait-description-template.md`](./prompts/code-mode/code-mode-wait-description-template.md) — **162** tokens — Code-mode `wait` tool description template (paired with `exec`).

### `prompts/tui/` — 1 files, 322 tokens

_TUI-injected prompts (e.g. /init)._

- [`tui-init-command.md`](./prompts/tui/tui-init-command.md) — **322** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/tui/prompt_for_init_command.md`. Category: tui. Description will be refined at M5 review.

### `prompts/data/` — 2 files, 513 tokens

_Static reference data embedded in the binary (apply_patch grammar, agent_names list, etc.)._

- [`data-agent-names.md`](./prompts/data/data-agent-names.md) — **340** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/agent/agent_names.txt`. Category: data. Description will be refined at M5 review.
- [`data-apply-patch-grammar.md`](./prompts/data/data-apply-patch-grammar.md) — **173** tokens — Auto-extracted by Pass 3 (M2) from `codex-rs/tools/src/tool_apply_patch.lark`. Category: data. Description will be refined at M5 review.

### `prompts/orphan/` — 15 files, 23,742 tokens

_Prompt-shaped files in upstream that are NOT `include_str!`'d. Historical/unshipped per SPEC §1.3._

- [`orphan-core-gpt-5-1-codex-max-prompt.md`](./prompts/orphan/orphan-core-gpt-5-1-codex-max-prompt.md) — **1,624** tokens — Orphan file at `codex-rs/core/gpt-5.1-codex-max_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NO…
- [`orphan-core-gpt-5-1-prompt.md`](./prompts/orphan/orphan-core-gpt-5-1-prompt.md) — **5,076** tokens — Orphan file at `codex-rs/core/gpt_5_1_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT part of…
- [`orphan-core-gpt-5-2-codex-prompt.md`](./prompts/orphan/orphan-core-gpt-5-2-codex-prompt.md) — **1,624** tokens — Orphan file at `codex-rs/core/gpt-5.2-codex_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT pa…
- [`orphan-core-gpt-5-2-prompt.md`](./prompts/orphan/orphan-core-gpt-5-2-prompt.md) — **4,570** tokens — Orphan file at `codex-rs/core/gpt_5_2_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT part of…
- [`orphan-core-gpt-5-codex-prompt.md`](./prompts/orphan/orphan-core-gpt-5-codex-prompt.md) — **1,436** tokens — Orphan file at `codex-rs/core/gpt_5_codex_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT part…
- [`orphan-core-prompt-with-apply-patch-instructions.md`](./prompts/orphan/orphan-core-prompt-with-apply-patch-instructions.md) — **5,123** tokens — Orphan file at `codex-rs/core/prompt_with_apply_patch_instructions.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical r…
- [`orphan-core-templates-agents-orchestrator.md`](./prompts/orphan/orphan-core-templates-agents-orchestrator.md) — **1,037** tokens — Orphan file at `codex-rs/core/templates/agents/orchestrator.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical referenc…
- [`orphan-core-templates-collab-experimental-prompt.md`](./prompts/orphan/orphan-core-templates-collab-experimental-prompt.md) — **291** tokens — Orphan file at `codex-rs/core/templates/collab/experimental_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical r…
- [`orphan-core-templates-model-instructions-gpt-5-2-codex-instructions-template.md`](./prompts/orphan/orphan-core-templates-model-instructions-gpt-5-2-codex-instructions-template.md) — **1,573** tokens — Orphan file at `codex-rs/core/templates/model_instructions/gpt-5.2-codex_instructions_template.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, pre…
- [`orphan-core-templates-personalities-gpt-5-2-codex-friendly.md`](./prompts/orphan/orphan-core-templates-personalities-gpt-5-2-codex-friendly.md) — **378** tokens — Orphan file at `codex-rs/core/templates/personalities/gpt-5.2-codex_friendly.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for hi…
- [`orphan-core-templates-personalities-gpt-5-2-codex-pragmatic.md`](./prompts/orphan/orphan-core-templates-personalities-gpt-5-2-codex-pragmatic.md) — **335** tokens — Orphan file at `codex-rs/core/templates/personalities/gpt-5.2-codex_pragmatic.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for h…
- [`orphan-core-templates-review-history-message-completed.md`](./prompts/orphan/orphan-core-templates-review-history-message-completed.md) — **59** tokens — Orphan file at `codex-rs/core/templates/review/history_message_completed.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for histor…
- [`orphan-core-templates-review-history-message-interrupted.md`](./prompts/orphan/orphan-core-templates-review-history-message-interrupted.md) — **67** tokens — Orphan file at `codex-rs/core/templates/review/history_message_interrupted.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for hist…
- [`orphan-core-templates-search-tool-tool-description.md`](./prompts/orphan/orphan-core-templates-search-tool-tool-description.md) — **119** tokens — Orphan file at `codex-rs/core/templates/search_tool/tool_description.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical…
- [`orphan-core-templates-search-tool-tool-suggest-description.md`](./prompts/orphan/orphan-core-templates-search-tool-tool-suggest-description.md) — **430** tokens — Orphan file at `codex-rs/core/templates/search_tool/tool_suggest_description.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for hi…

<!-- AUTO-GENERATED-END -->
## Contributing

The mirror is auto-generated. Manual edits inside the AUTO-GENERATED markers above will be overwritten on the next extraction. To change the *spec* (categorization, frontmatter, extractor logic), edit `SPEC.md` and the `extractor/` tooling.
