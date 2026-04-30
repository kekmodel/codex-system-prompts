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

## Captured corpus (auto-generated)

<!-- AUTO-GENERATED-START -->
_Auto-generated by `extractor pass5` (M6) at codex `rust-v0.128.0-alpha.1`._

**149 captured files** across 11 categories — 
**98,675 tokens** (o200k_base, template counts — runtime values are placeholder-redacted, see SPEC §2.5 Layer A).

### `prompts/base-instructions/` — 8 files, 28,913 tokens

Per-model `base_instructions` (fanned out from `models.json`) + fallbacks.

| File | Tokens | Description |
|---|---:|---|
| [`base-instructions-codex-auto-review.md`](./prompts/base-instructions/base-instructions-codex-auto-review.md) | **2,991** | Per-model `base_instructions` for slug `codex-auto-review`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/5/base_instructions. |
| [`base-instructions-default.md`](./prompts/base-instructions/base-instructions-default.md) | **4,371** | Auto-extracted by Pass 3 (M2) from `codex-rs/protocol/src/prompts/base_instructions/default.md`. Category: base-instructions. Description will be refined at M5 review. |
| [`base-instructions-fallback.md`](./prompts/base-instructions/base-instructions-fallback.md) | **4,371** | Auto-extracted by Pass 3 (M2) from `codex-rs/models-manager/prompt.md`. Category: base-instructions. Description will be refined at M5 review. |
| [`base-instructions-gpt-5.2.md`](./prompts/base-instructions/base-instructions-gpt-5.2.md) | **4,570** | Per-model `base_instructions` for slug `gpt-5.2`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/4/base_instructions. |
| [`base-instructions-gpt-5.3-codex.md`](./prompts/base-instructions/base-instructions-gpt-5.3-codex.md) | **2,551** | Per-model `base_instructions` for slug `gpt-5.3-codex`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/3/base_instructions. |
| [`base-instructions-gpt-5.4-mini.md`](./prompts/base-instructions/base-instructions-gpt-5.4-mini.md) | **2,639** | Per-model `base_instructions` for slug `gpt-5.4-mini`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/2/base_instructions. |
| [`base-instructions-gpt-5.4.md`](./prompts/base-instructions/base-instructions-gpt-5.4.md) | **2,991** | Per-model `base_instructions` for slug `gpt-5.4`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/1/base_instructions. |
| [`base-instructions-gpt-5.5.md`](./prompts/base-instructions/base-instructions-gpt-5.5.md) | **4,429** | Per-model `base_instructions` for slug `gpt-5.5`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/0/base_instructions. |

### `prompts/mode/` — 17 files, 8,944 tokens

Mode-specific prompts: review, compact, realtime, goals, guardian, collaboration.

| File | Tokens | Description |
|---|---:|---|
| [`mode-collab-default.md`](./prompts/mode/mode-collab-default.md) | **173** | Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/default.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-collab-execute.md`](./prompts/mode/mode-collab-execute.md) | **763** | Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/execute.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-collab-pair-programming.md`](./prompts/mode/mode-collab-pair-programming.md) | **222** | Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/pair_programming.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-collab-plan.md`](./prompts/mode/mode-collab-plan.md) | **1,804** | Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/plan.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-compact-prompt.md`](./prompts/mode/mode-compact-prompt.md) | **89** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/compact/prompt.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-compact-summary-prefix.md`](./prompts/mode/mode-compact-summary-prefix.md) | **77** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/compact/summary_prefix.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-goal-budget-limit.md`](./prompts/mode/mode-goal-budget-limit.md) | **139** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/goals/budget_limit.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-goal-continuation.md`](./prompts/mode/mode-goal-continuation.md) | **465** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/goals/continuation.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-guardian-output-contract.md`](./prompts/mode/mode-guardian-output-contract.md) | **121** | Guardian output JSON-schema contract appended to the policy prompt at runtime (defines outcome/risk_level/user_authorization fields). |
| [`mode-guardian-policy-template.md`](./prompts/mode/mode-guardian-policy-template.md) | **1,416** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/guardian/policy_template.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-guardian-policy.md`](./prompts/mode/mode-guardian-policy.md) | **1,042** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/guardian/policy.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-realtime-backend.md`](./prompts/mode/mode-realtime-backend.md) | **954** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/realtime/backend_prompt.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-realtime-end.md`](./prompts/mode/mode-realtime-end.md) | **38** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/realtime/realtime_end.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-realtime-start.md`](./prompts/mode/mode-realtime-start.md) | **145** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/realtime/realtime_start.md`. Category: mode. Description will be refined at M5 review. |
| [`mode-review-exit-interrupted.md`](./prompts/mode/mode-review-exit-interrupted.md) | **67** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_interrupted.xml`. Category: mode. Description will be refined at M5 review. |
| [`mode-review-exit-success.md`](./prompts/mode/mode-review-exit-success.md) | **59** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_success.xml`. Category: mode. Description will be refined at M5 review. |
| [`mode-review.md`](./prompts/mode/mode-review.md) | **1,370** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/review_prompt.md`. Category: mode. Description will be refined at M5 review. |

### `prompts/permission/` — 8 files, 1,357 tokens

Approval-policy and sandbox-mode prompt fragments.

| File | Tokens | Description |
|---|---:|---|
| [`permission-approval-never.md`](./prompts/permission/permission-approval-never.md) | **23** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/never.md`. Category: permission. Description will be refined at M5 review. |
| [`permission-approval-on-failure.md`](./prompts/permission/permission-approval-on-failure.md) | **60** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_failure.md`. Category: permission. Description will be refined at M5 review. |
| [`permission-approval-on-request-rule-request-permission.md`](./prompts/permission/permission-approval-on-request-rule-request-permission.md) | **333** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_request_rule_request_permission.md`. Category: permission. Description will be refined at M5 review. |
| [`permission-approval-on-request.md`](./prompts/permission/permission-approval-on-request.md) | **758** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_request.md`. Category: permission. Description will be refined at M5 review. |
| [`permission-approval-unless-trusted.md`](./prompts/permission/permission-approval-unless-trusted.md) | **50** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/unless_trusted.md`. Category: permission. Description will be refined at M5 review. |
| [`permission-sandbox-danger-full-access.md`](./prompts/permission/permission-sandbox-danger-full-access.md) | **40** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/danger_full_access.md`. Category: permission. Description will be refined at M5 review. |
| [`permission-sandbox-read-only.md`](./prompts/permission/permission-sandbox-read-only.md) | **36** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/read_only.md`. Category: permission. Description will be refined at M5 review. |
| [`permission-sandbox-workspace-write.md`](./prompts/permission/permission-sandbox-workspace-write.md) | **57** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/workspace_write.md`. Category: permission. Description will be refined at M5 review. |

### `prompts/context-fragment/` — 22 files, 1,304 tokens

ContextualUserFragment wrappers — XML-tagged user-message injections.

| File | Tokens | Description |
|---|---:|---|
| [`context-fragment-approved-command-prefix-saved.md`](./prompts/context-fragment/context-fragment-approved-command-prefix-saved.md) | **6** | `ApprovedCommandPrefixSaved` ContextualUserFragment from `codex-rs/core/src/context/approved_command_prefix_saved.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template. |
| [`context-fragment-apps-instructions.md`](./prompts/context-fragment/context-fragment-apps-instructions.md) | **143** | `AppsInstructions` ContextualUserFragment from `codex-rs/core/src/context/apps_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template. |
| [`context-fragment-available-plugins-instructions.md`](./prompts/context-fragment/context-fragment-available-plugins-instructions.md) | **332** | `AvailablePluginsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_plugins_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-available-skills-instructions.md`](./prompts/context-fragment/context-fragment-available-skills-instructions.md) | **30** | `AvailableSkillsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_skills_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-collaboration-mode-instructions.md`](./prompts/context-fragment/context-fragment-collaboration-mode-instructions.md) | **18** | `CollaborationModeInstructions` ContextualUserFragment from `codex-rs/core/src/context/collaboration_mode_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-environment-context.md`](./prompts/context-fragment/context-fragment-environment-context.md) | **335** | `EnvironmentContext` ContextualUserFragment from `codex-rs/core/src/context/environment_context.rs`. Role: 'user'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-guardian-followup-review-reminder.md`](./prompts/context-fragment/context-fragment-guardian-followup-review-reminder.md) | **89** | `GuardianFollowupReviewReminder` ContextualUserFragment from `codex-rs/core/src/context/guardian_followup_review_reminder.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-hook-additional-context.md`](./prompts/context-fragment/context-fragment-hook-additional-context.md) | **18** | `HookAdditionalContext` ContextualUserFragment from `codex-rs/core/src/context/hook_additional_context.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-image-generation-instructions.md`](./prompts/context-fragment/context-fragment-image-generation-instructions.md) | **41** | `ImageGenerationInstructions` ContextualUserFragment from `codex-rs/core/src/context/image_generation_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template. |
| [`context-fragment-model-switch-instructions.md`](./prompts/context-fragment/context-fragment-model-switch-instructions.md) | **28** | `ModelSwitchInstructions` ContextualUserFragment from `codex-rs/core/src/context/model_switch_instructions.rs`. Role: 'developer'. Markers: '<model_switch>' … '</model_switch>'. body() captured as template. |
| [`context-fragment-network-rule-saved.md`](./prompts/context-fragment/context-fragment-network-rule-saved.md) | **85** | `NetworkRuleSaved` ContextualUserFragment from `codex-rs/core/src/context/network_rule_saved.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-permissions-instructions.md`](./prompts/context-fragment/context-fragment-permissions-instructions.md) | **26** | `PermissionsInstructions` ContextualUserFragment from `codex-rs/core/src/context/permissions_instructions.rs`. Role: 'developer'. Markers: '<permissions instructions>' … '</permissions instructions>'. body() captured as function-body-source… |
| [`context-fragment-personality-spec-instructions.md`](./prompts/context-fragment/context-fragment-personality-spec-instructions.md) | **31** | `PersonalitySpecInstructions` ContextualUserFragment from `codex-rs/core/src/context/personality_spec_instructions.rs`. Role: 'developer'. Markers: '<personality_spec>' … '</personality_spec>'. body() captured as template. |
| [`context-fragment-plugin-instructions.md`](./prompts/context-fragment/context-fragment-plugin-instructions.md) | **18** | `PluginInstructions` ContextualUserFragment from `codex-rs/core/src/context/plugin_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as function-body-source. |
| [`context-fragment-realtime-end-instructions.md`](./prompts/context-fragment/context-fragment-realtime-end-instructions.md) | **5** | `RealtimeEndInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_end_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template. |
| [`context-fragment-realtime-start-instructions.md`](./prompts/context-fragment/context-fragment-realtime-start-instructions.md) | **2** | `RealtimeStartInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_start_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template. |
| [`context-fragment-realtime-start-with-instructions.md`](./prompts/context-fragment/context-fragment-realtime-start-with-instructions.md) | **2** | `RealtimeStartWithInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_start_with_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as template. |
| [`context-fragment-skill-instructions.md`](./prompts/context-fragment/context-fragment-skill-instructions.md) | **19** | `SkillInstructions` ContextualUserFragment from `codex-rs/core/src/context/skill_instructions.rs`. Role: 'user'. Markers: '<skill>' … '</skill>'. body() captured as template. |
| [`context-fragment-subagent-notification.md`](./prompts/context-fragment/context-fragment-subagent-notification.md) | **11** | `SubagentNotification` ContextualUserFragment from `codex-rs/core/src/context/subagent_notification.rs`. Role: 'user'. Markers: '<subagent_notification>' … '</subagent_notification>'. body() captured as template. |
| [`context-fragment-turn-aborted.md`](./prompts/context-fragment/context-fragment-turn-aborted.md) | **11** | `TurnAborted` ContextualUserFragment from `codex-rs/core/src/context/turn_aborted.rs`. Role: 'user'. Markers: '<turn_aborted>' … '</turn_aborted>'. body() captured as template. |
| [`context-fragment-user-instructions.md`](./prompts/context-fragment/context-fragment-user-instructions.md) | **17** | `UserInstructions` ContextualUserFragment from `codex-rs/core/src/context/user_instructions.rs`. Role: 'user'. Markers: '# AGENTS.md instructions for ' … '</INSTRUCTIONS>'. body() captured as template. |
| [`context-fragment-user-shell-command.md`](./prompts/context-fragment/context-fragment-user-shell-command.md) | **37** | `UserShellCommand` ContextualUserFragment from `codex-rs/core/src/context/user_shell_command.rs`. Role: 'user'. Markers: '<user_shell_command>' … '</user_shell_command>'. body() captured as template. |

### `prompts/tool/` — 60 files, 13,188 tokens

Built-in tool descriptions (apply_patch, spawn_agent guidance, MCP message templates).

| File | Tokens | Description |
|---|---:|---|
| [`tool-apply-patch-instructions.md`](./prompts/tool/tool-apply-patch-instructions.md) | **752** | Auto-extracted by Pass 3 (M2) from `codex-rs/apply-patch/apply_patch_tool_instructions.md`. Category: tool. Description will be refined at M5 review. |
| [`tool-apply-patch-json-description.md`](./prompts/tool/tool-apply-patch-json-description.md) | **706** | JSON-API variant of the apply_patch tool description (paired with apply_patch_tool_instructions.md / apply_patch.lark grammar). |
| [`tool-close-agent-description-v2.md`](./prompts/tool/tool-close-agent-description-v2.md) | **41** | Inline ToolSpec description for `close_agent` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-close-agent-description.md`](./prompts/tool/tool-close-agent-description.md) | **41** | Inline ToolSpec description for `close_agent` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-close-agent-parameters-v2.md`](./prompts/tool/tool-close-agent-parameters-v2.md) | **73** | Per-parameter `JsonSchema` descriptions for `close_agent` (1 parameter). Pass 1.7 (M9). |
| [`tool-close-agent-parameters.md`](./prompts/tool/tool-close-agent-parameters.md) | **69** | Per-parameter `JsonSchema` descriptions for `close_agent` (1 parameter). Pass 1.7 (M9). |
| [`tool-consequential-message-templates.md`](./prompts/tool/tool-consequential-message-templates.md) | **6,900** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/consequential_tool_message_templates.json`. Category: tool. Description will be refined at M5 review. |
| [`tool-create-goal-description.md`](./prompts/tool/tool-create-goal-description.md) | **55** | Inline ToolSpec description for `create_goal` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-create-goal-parameters.md`](./prompts/tool/tool-create-goal-parameters.md) | **111** | Per-parameter `JsonSchema` descriptions for `create_goal` (2 parameters). Pass 1.7 (M9). |
| [`tool-exec-command-description.md`](./prompts/tool/tool-exec-command-description.md) | **69** | Inline ToolSpec description for `exec_command` — `cfg!(windows)` conditional. Both branches captured side-by-side. Pass 1.7 (M9). |
| [`tool-exec-command-parameters.md`](./prompts/tool/tool-exec-command-parameters.md) | **211** | Per-parameter `JsonSchema` descriptions for `exec_command` (7 parameters). Pass 1.7 (M9). |
| [`tool-followup-task-description.md`](./prompts/tool/tool-followup-task-description.md) | **48** | Inline ToolSpec description for `followup_task` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-followup-task-parameters.md`](./prompts/tool/tool-followup-task-parameters.md) | **90** | Per-parameter `JsonSchema` descriptions for `followup_task` (2 parameters). Pass 1.7 (M9). |
| [`tool-get-goal-description.md`](./prompts/tool/tool-get-goal-description.md) | **24** | Inline ToolSpec description for `get_goal` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-list-agents-description.md`](./prompts/tool/tool-list-agents-description.md) | **18** | Inline ToolSpec description for `list_agents` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-list-agents-parameters.md`](./prompts/tool/tool-list-agents-parameters.md) | **83** | Per-parameter `JsonSchema` descriptions for `list_agents` (1 parameter). Pass 1.7 (M9). |
| [`tool-list-dir-description.md`](./prompts/tool/tool-list-dir-description.md) | **18** | Inline ToolSpec description for `list_dir` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-list-dir-parameters.md`](./prompts/tool/tool-list-dir-parameters.md) | **127** | Per-parameter `JsonSchema` descriptions for `list_dir` (4 parameters). Pass 1.7 (M9). |
| [`tool-list-mcp-resource-templates-description.md`](./prompts/tool/tool-list-mcp-resource-templates-description.md) | **48** | Inline ToolSpec description for `list_mcp_resource_templates` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-list-mcp-resource-templates-parameters.md`](./prompts/tool/tool-list-mcp-resource-templates-parameters.md) | **104** | Per-parameter `JsonSchema` descriptions for `list_mcp_resource_templates` (2 parameters). Pass 1.7 (M9). |
| [`tool-list-mcp-resources-description.md`](./prompts/tool/tool-list-mcp-resources-description.md) | **40** | Inline ToolSpec description for `list_mcp_resources` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-list-mcp-resources-parameters.md`](./prompts/tool/tool-list-mcp-resources-parameters.md) | **101** | Per-parameter `JsonSchema` descriptions for `list_mcp_resources` (2 parameters). Pass 1.7 (M9). |
| [`tool-read-mcp-resource-description.md`](./prompts/tool/tool-read-mcp-resource-description.md) | **16** | Inline ToolSpec description for `read_mcp_resource` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-read-mcp-resource-parameters.md`](./prompts/tool/tool-read-mcp-resource-parameters.md) | **111** | Per-parameter `JsonSchema` descriptions for `read_mcp_resource` (2 parameters). Pass 1.7 (M9). |
| [`tool-report-agent-job-result-description.md`](./prompts/tool/tool-report-agent-job-result-description.md) | **20** | Inline ToolSpec description for `report_agent_job_result` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-report-agent-job-result-parameters.md`](./prompts/tool/tool-report-agent-job-result-parameters.md) | **107** | Per-parameter `JsonSchema` descriptions for `report_agent_job_result` (3 parameters). Pass 1.7 (M9). |
| [`tool-request-permissions-description.md`](./prompts/tool/tool-request-permissions-description.md) | **12** | Inline ToolSpec description for `request_permissions` resolved from a `let description = …` binding (sub-kind `let_unresolved`). Pass 1.7 (M9). |
| [`tool-request-permissions-parameters.md`](./prompts/tool/tool-request-permissions-parameters.md) | **69** | Per-parameter `JsonSchema` descriptions for `request_permissions` (1 parameter). Pass 1.7 (M9). |
| [`tool-request-user-input-description.md`](./prompts/tool/tool-request-user-input-description.md) | **12** | Inline ToolSpec description for `request_user_input` resolved from a `let description = …` binding (sub-kind `let_unresolved`). Pass 1.7 (M9). |
| [`tool-request-user-input-parameters.md`](./prompts/tool/tool-request-user-input-parameters.md) | **141** | Per-parameter `JsonSchema` descriptions for `request_user_input` (5 parameters). Pass 1.7 (M9). |
| [`tool-resume-agent-description.md`](./prompts/tool/tool-resume-agent-description.md) | **18** | Inline ToolSpec description for `resume_agent` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-resume-agent-parameters.md`](./prompts/tool/tool-resume-agent-parameters.md) | **65** | Per-parameter `JsonSchema` descriptions for `resume_agent` (1 parameter). Pass 1.7 (M9). |
| [`tool-send-input-description.md`](./prompts/tool/tool-send-input-description.md) | **41** | Inline ToolSpec description for `send_input` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-send-input-parameters.md`](./prompts/tool/tool-send-input-parameters.md) | **122** | Per-parameter `JsonSchema` descriptions for `send_input` (3 parameters). Pass 1.7 (M9). |
| [`tool-send-message-description.md`](./prompts/tool/tool-send-message-description.md) | **22** | Inline ToolSpec description for `send_message` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-send-message-parameters.md`](./prompts/tool/tool-send-message-parameters.md) | **88** | Per-parameter `JsonSchema` descriptions for `send_message` (2 parameters). Pass 1.7 (M9). |
| [`tool-shell-command-description.md`](./prompts/tool/tool-shell-command-description.md) | **227** | Inline ToolSpec description for `shell_command` resolved from a `let description = …` binding (sub-kind `cfg_conditional`). Pass 1.7 (M9). |
| [`tool-shell-command-parameters.md`](./prompts/tool/tool-shell-command-parameters.md) | **124** | Per-parameter `JsonSchema` descriptions for `shell_command` (4 parameters). Pass 1.7 (M9). |
| [`tool-shell-description.md`](./prompts/tool/tool-shell-description.md) | **333** | Inline ToolSpec description for `shell` resolved from a `let description = …` binding (sub-kind `cfg_conditional`). Pass 1.7 (M9). |
| [`tool-shell-parameters.md`](./prompts/tool/tool-shell-parameters.md) | **84** | Per-parameter `JsonSchema` descriptions for `shell` (2 parameters). Pass 1.7 (M9). |
| [`tool-spawn-agent-description-v2.md`](./prompts/tool/tool-spawn-agent-description-v2.md) | **20** | Inline ToolSpec description for `spawn_agent` — built dynamically by `spawn_agent_tool_description_v2(...)`. Body is a placeholder; resolving the helper is a follow-up. Pass 1.7 (M9). |
| [`tool-spawn-agent-description.md`](./prompts/tool/tool-spawn-agent-description.md) | **18** | Inline ToolSpec description for `spawn_agent` — built dynamically by `spawn_agent_tool_description(...)`. Body is a placeholder; resolving the helper is a follow-up. Pass 1.7 (M9). |
| [`tool-spawn-agent-inherited-model-guidance.md`](./prompts/tool/tool-spawn-agent-inherited-model-guidance.md) | **33** | Guidance attached to spawn_agent's `model` parameter — inheritance default rule. |
| [`tool-spawn-agent-model-override-description.md`](./prompts/tool/tool-spawn-agent-model-override-description.md) | **44** | Description for spawn_agent's optional `model` override parameter. |
| [`tool-spawn-agent-parameters-v2.md`](./prompts/tool/tool-spawn-agent-parameters-v2.md) | **77** | Per-parameter `JsonSchema` descriptions for `spawn_agent` (1 parameter). Pass 1.7 (M9). |
| [`tool-spawn-agents-on-csv-description.md`](./prompts/tool/tool-spawn-agents-on-csv-description.md) | **82** | Inline ToolSpec description for `spawn_agents_on_csv` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-spawn-agents-on-csv-parameters.md`](./prompts/tool/tool-spawn-agents-on-csv-parameters.md) | **211** | Per-parameter `JsonSchema` descriptions for `spawn_agents_on_csv` (7 parameters). Pass 1.7 (M9). |
| [`tool-test-sync-tool-description.md`](./prompts/tool/tool-test-sync-tool-description.md) | **10** | Inline ToolSpec description for `test_sync_tool` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-test-sync-tool-parameters.md`](./prompts/tool/tool-test-sync-tool-parameters.md) | **144** | Per-parameter `JsonSchema` descriptions for `test_sync_tool` (5 parameters). Pass 1.7 (M9). |
| [`tool-tool-suggest-description.md`](./prompts/tool/tool-tool-suggest-description.md) | **451** | Inline ToolSpec description for `tool_suggest` resolved from a `let description = …` binding (sub-kind `let_literal`). Pass 1.7 (M9). |
| [`tool-tool-suggest-parameters.md`](./prompts/tool/tool-tool-suggest-parameters.md) | **136** | Per-parameter `JsonSchema` descriptions for `tool_suggest` (4 parameters). Pass 1.7 (M9). |
| [`tool-update-goal-description.md`](./prompts/tool/tool-update-goal-description.md) | **107** | Inline ToolSpec description for `update_goal` (literal `static_raw`). Captured by Pass 1.7 (M9). |
| [`tool-update-plan-description.md`](./prompts/tool/tool-update-plan-description.md) | **35** | Inline ToolSpec description for `update_plan` (literal `static_raw`). Captured by Pass 1.7 (M9). |
| [`tool-update-plan-parameters.md`](./prompts/tool/tool-update-plan-parameters.md) | **70** | Per-parameter `JsonSchema` descriptions for `update_plan` (1 parameter). Pass 1.7 (M9). |
| [`tool-view-image-description.md`](./prompts/tool/tool-view-image-description.md) | **36** | Inline ToolSpec description for `view_image` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-view-image-parameters.md`](./prompts/tool/tool-view-image-parameters.md) | **132** | Per-parameter `JsonSchema` descriptions for `view_image` (2 parameters). Pass 1.7 (M9). |
| [`tool-wait-agent-description-v2.md`](./prompts/tool/tool-wait-agent-description-v2.md) | **50** | Inline ToolSpec description for `wait_agent` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-wait-agent-description.md`](./prompts/tool/tool-wait-agent-description.md) | **46** | Inline ToolSpec description for `wait_agent` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-write-stdin-description.md`](./prompts/tool/tool-write-stdin-description.md) | **13** | Inline ToolSpec description for `write_stdin` (literal `static_plain`). Captured by Pass 1.7 (M9). |
| [`tool-write-stdin-parameters.md`](./prompts/tool/tool-write-stdin-parameters.md) | **132** | Per-parameter `JsonSchema` descriptions for `write_stdin` (4 parameters). Pass 1.7 (M9). |

### `prompts/agent/` — 4 files, 852 tokens

Built-in agent roles + agent_names list + hierarchical-agent message.

| File | Tokens | Description |
|---|---:|---|
| [`agent-builtin-awaiter.md`](./prompts/agent/agent-builtin-awaiter.md) | **259** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/agent/builtins/awaiter.toml`. Category: agent. Description will be refined at M5 review. |
| [`agent-hierarchical-message.md`](./prompts/agent/agent-hierarchical-message.md) | **209** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/hierarchical_agents_message.md`. Category: agent. Description will be refined at M5 review. |
| [`agent-role-explorer.md`](./prompts/agent/agent-role-explorer.md) | **188** | Explorer role description — inline string in role.rs DEFAULT_ROLE_CONFIG table. |
| [`agent-role-worker.md`](./prompts/agent/agent-role-worker.md) | **196** | Worker role description — inline string in role.rs DEFAULT_ROLE_CONFIG table. |

### `prompts/memory/` — 4 files, 18,057 tokens

/memories skill prompts.

| File | Tokens | Description |
|---|---:|---|
| [`memory-read-read-path.md`](./prompts/memory/memory-read-read-path.md) | **1,532** | Auto-extracted by Pass 3 (M2) from `codex-rs/memories/read/templates/memories/read_path.md`. Category: memory. Description will be refined at M5 review. |
| [`memory-write-consolidation.md`](./prompts/memory/memory-write-consolidation.md) | **10,379** | Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/consolidation.md`. Category: memory. Description will be refined at M5 review. |
| [`memory-write-stage-one-input.md`](./prompts/memory/memory-write-stage-one-input.md) | **86** | Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/stage_one_input.md`. Category: memory. Description will be refined at M5 review. |
| [`memory-write-stage-one-system.md`](./prompts/memory/memory-write-stage-one-system.md) | **6,060** | Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/stage_one_system.md`. Category: memory. Description will be refined at M5 review. |

### `prompts/code-mode/` — 5 files, 1,427 tokens

Code-mode (JS-orchestration tool) description constants.

| File | Tokens | Description |
|---|---:|---|
| [`code-mode-deferred-nested-tools-guidance.md`](./prompts/code-mode/code-mode-deferred-nested-tools-guidance.md) | **76** | Guidance noting that some nested MCP/app tools may be omitted from the description but are still callable via `tools` / `ALL_TOOLS`. |
| [`code-mode-exec-description-template.md`](./prompts/code-mode/code-mode-exec-description-template.md) | **700** | Code-mode `exec` tool description template — programmatic preface for the JS-orchestration `exec` tool. |
| [`code-mode-mcp-typescript-preamble.md`](./prompts/code-mode/code-mode-mcp-typescript-preamble.md) | **413** | TypeScript schema preamble injected into code-mode tool description for the MCP nested-tool API. |
| [`code-mode-only-preface.md`](./prompts/code-mode/code-mode-only-preface.md) | **76** | Preface added when code-mode is the only tool exposure (no other MCP tools listed). |
| [`code-mode-wait-description-template.md`](./prompts/code-mode/code-mode-wait-description-template.md) | **162** | Code-mode `wait` tool description template (paired with `exec`). |

### `prompts/tui/` — 1 files, 322 tokens

TUI-injected prompts (e.g. /init).

| File | Tokens | Description |
|---|---:|---|
| [`tui-init-command.md`](./prompts/tui/tui-init-command.md) | **322** | Auto-extracted by Pass 3 (M2) from `codex-rs/tui/prompt_for_init_command.md`. Category: tui. Description will be refined at M5 review. |

### `prompts/data/` — 2 files, 513 tokens

Static reference data embedded in the binary (apply_patch grammar, agent_names list, etc.).

| File | Tokens | Description |
|---|---:|---|
| [`data-agent-names.md`](./prompts/data/data-agent-names.md) | **340** | Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/agent/agent_names.txt`. Category: data. Description will be refined at M5 review. |
| [`data-apply-patch-grammar.md`](./prompts/data/data-apply-patch-grammar.md) | **173** | Auto-extracted by Pass 3 (M2) from `codex-rs/tools/src/tool_apply_patch.lark`. Category: data. Description will be refined at M5 review. |

### `prompts/orphan/` — 18 files, 23,798 tokens

Prompt-shaped files in upstream that are NOT `include_str!`'d. Historical/unshipped per SPEC §1.3.

| File | Tokens | Description |
|---|---:|---|
| [`orphan-core-gpt-5-1-codex-max-prompt.md`](./prompts/orphan/orphan-core-gpt-5-1-codex-max-prompt.md) | **1,624** | Orphan file at `codex-rs/core/gpt-5.1-codex-max_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NO… |
| [`orphan-core-gpt-5-1-prompt.md`](./prompts/orphan/orphan-core-gpt-5-1-prompt.md) | **5,076** | Orphan file at `codex-rs/core/gpt_5_1_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT part of… |
| [`orphan-core-gpt-5-2-codex-prompt.md`](./prompts/orphan/orphan-core-gpt-5-2-codex-prompt.md) | **1,624** | Orphan file at `codex-rs/core/gpt-5.2-codex_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT pa… |
| [`orphan-core-gpt-5-2-prompt.md`](./prompts/orphan/orphan-core-gpt-5-2-prompt.md) | **4,570** | Orphan file at `codex-rs/core/gpt_5_2_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT part of… |
| [`orphan-core-gpt-5-codex-prompt.md`](./prompts/orphan/orphan-core-gpt-5-codex-prompt.md) | **1,436** | Orphan file at `codex-rs/core/gpt_5_codex_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical reference. NOT part… |
| [`orphan-core-prompt-with-apply-patch-instructions.md`](./prompts/orphan/orphan-core-prompt-with-apply-patch-instructions.md) | **5,123** | Orphan file at `codex-rs/core/prompt_with_apply_patch_instructions.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical r… |
| [`orphan-core-templates-agents-orchestrator.md`](./prompts/orphan/orphan-core-templates-agents-orchestrator.md) | **1,037** | Orphan file at `codex-rs/core/templates/agents/orchestrator.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical referenc… |
| [`orphan-core-templates-collab-experimental-prompt.md`](./prompts/orphan/orphan-core-templates-collab-experimental-prompt.md) | **291** | Orphan file at `codex-rs/core/templates/collab/experimental_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical r… |
| [`orphan-core-templates-model-instructions-gpt-5-2-codex-instructions-template.md`](./prompts/orphan/orphan-core-templates-model-instructions-gpt-5-2-codex-instructions-template.md) | **1,573** | Orphan file at `codex-rs/core/templates/model_instructions/gpt-5.2-codex_instructions_template.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, pre… |
| [`orphan-core-templates-personalities-gpt-5-2-codex-friendly.md`](./prompts/orphan/orphan-core-templates-personalities-gpt-5-2-codex-friendly.md) | **378** | Orphan file at `codex-rs/core/templates/personalities/gpt-5.2-codex_friendly.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for hi… |
| [`orphan-core-templates-personalities-gpt-5-2-codex-pragmatic.md`](./prompts/orphan/orphan-core-templates-personalities-gpt-5-2-codex-pragmatic.md) | **335** | Orphan file at `codex-rs/core/templates/personalities/gpt-5.2-codex_pragmatic.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for h… |
| [`orphan-core-templates-review-history-message-completed.md`](./prompts/orphan/orphan-core-templates-review-history-message-completed.md) | **59** | Orphan file at `codex-rs/core/templates/review/history_message_completed.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for histor… |
| [`orphan-core-templates-review-history-message-interrupted.md`](./prompts/orphan/orphan-core-templates-review-history-message-interrupted.md) | **67** | Orphan file at `codex-rs/core/templates/review/history_message_interrupted.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for hist… |
| [`orphan-core-templates-search-tool-tool-description.md`](./prompts/orphan/orphan-core-templates-search-tool-tool-description.md) | **119** | Orphan file at `codex-rs/core/templates/search_tool/tool_description.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for historical… |
| [`orphan-core-templates-search-tool-tool-suggest-description.md`](./prompts/orphan/orphan-core-templates-search-tool-tool-suggest-description.md) | **430** | Orphan file at `codex-rs/core/templates/search_tool/tool_suggest_description.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.128.0-alpha.1`. Per SPEC §1.3 boundary cases, preserved here for hi… |
| [`orphan-models-manager-default-personality-header.md`](./prompts/orphan/orphan-models-manager-default-personality-header.md) | **30** | GPT-5 default personality header consumed by gpt-5.2-codex / exp-codex-personality slug branch in `local_personality_messages_for_slug` (model_info.rs:103-117). Inactive: the slug is not in models.json today. |
| [`orphan-models-manager-local-friendly-template.md`](./prompts/orphan/orphan-models-manager-local-friendly-template.md) | **16** | `personality_friendly` variable body for the gpt-5.2-codex slug. Substituted into `{{ personality }}` placeholder when user picks the friendly personality. Inactive today (slug not registered). |
| [`orphan-models-manager-local-pragmatic-template.md`](./prompts/orphan/orphan-models-manager-local-pragmatic-template.md) | **10** | `personality_pragmatic` variable body for the gpt-5.2-codex slug. Substituted into `{{ personality }}` placeholder when user picks the pragmatic personality. Inactive today (slug not registered). |

<!-- AUTO-GENERATED-END -->

## Coverage (auto-generated)

<!-- AUTO-GENERATED-START -->
_Layer A (placeholder mapping) + Layer B (completeness) coverage report._

✅ **Pass 4 verification: PASSED**

- Layer A unmapped placeholders: **0**
- Layer B autoinclude misses:    **0**
- Layer B model-fanout misses:   **0**
- Layer B allow-list misses:     **0**
- Frontmatter schema fails:      **0**
- Token-count drifts:            **0**
<!-- AUTO-GENERATED-END -->
