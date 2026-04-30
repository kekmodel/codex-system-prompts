# codex-system-prompts CHANGELOG

> Per-mirror-tag prompt diffs, newest first. Format mirrors Piebald's [`claude-code-system-prompts/CHANGELOG.md`](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/CHANGELOG.md). See [SPEC §3.5](./SPEC.md#35-changelog-strategy).

# [rust-v0.128.0-alpha.1](https://github.com/openai/codex/releases/tag/rust-v0.128.0-alpha.1)

_+7,627 tokens_

Diff vs. previous mirror tag `rust-v0.126.0-alpha.12` at codex commit `8148b7b1f8660e464661743587f754471ae60868`. NEW: 37, MODIFIED: 18, MOVED: 0, REMOVED: 0.

## `prompts/mode/`

- `mode-collab-default.md` — token Δ +72 (101 → 173).

## `prompts/context-fragment/`

- `context-fragment-approved-command-prefix-saved.md` — token Δ +0 (6 → 6).
- `context-fragment-apps-instructions.md` — token Δ +0 (143 → 143).
- `context-fragment-available-plugins-instructions.md` — token Δ −332 (332 → 0).
- `context-fragment-available-skills-instructions.md` — token Δ −30 (30 → 0).
- `context-fragment-collaboration-mode-instructions.md` — token Δ −18 (18 → 0).
- `context-fragment-environment-context.md` — token Δ −335 (335 → 0).
- `context-fragment-guardian-followup-review-reminder.md` — token Δ −89 (89 → 0).
- `context-fragment-hook-additional-context.md` — token Δ −18 (18 → 0).
- `context-fragment-image-generation-instructions.md` — token Δ +0 (41 → 41).
- `context-fragment-network-rule-saved.md` — token Δ −85 (85 → 0).
- `context-fragment-permissions-instructions.md` — token Δ −18 (26 → 8).
- `context-fragment-plugin-instructions.md` — token Δ −18 (18 → 0).
- `context-fragment-realtime-end-instructions.md` — token Δ +0 (5 → 5).
- `context-fragment-realtime-start-instructions.md` — token Δ +0 (2 → 2).
- `context-fragment-realtime-start-with-instructions.md` — token Δ +0 (2 → 2).

## `prompts/tool/`

- **NEW:** `tool-apply-patch.md` (**861** tk) — `apply_patch` ToolSpec.
- **NEW:** `tool-close-agent-v2.md` (**129** tk) — `close_agent` ToolSpec.
- **NEW:** `tool-close-agent.md` (**125** tk) — `close_agent` ToolSpec.
- **NEW:** `tool-create-goal.md` (**193** tk) — `create_goal` ToolSpec.
- **NEW:** `tool-exec-command-unix.md` (**316** tk) — `exec_command` ToolSpec.
- **NEW:** `tool-exec-command-windows.md` (**320** tk) — `exec_command` ToolSpec.
- **NEW:** `tool-followup-task.md` (**165** tk) — `followup_task` ToolSpec.
- **NEW:** `tool-get-goal.md` (**77** tk) — `get_goal` ToolSpec.
- **NEW:** `tool-list-agents.md` (**115** tk) — `list_agents` ToolSpec.
- **NEW:** `tool-list-dir.md` (**195** tk) — `list_dir` ToolSpec.
- **NEW:** `tool-list-mcp-resource-templates.md` (**177** tk) — `list_mcp_resource_templates` ToolSpec.
- **NEW:** `tool-list-mcp-resources.md` (**166** tk) — `list_mcp_resources` ToolSpec.
- **NEW:** `tool-read-mcp-resource.md` (**152** tk) — `read_mcp_resource` ToolSpec.
- **NEW:** `tool-report-agent-job-result.md` (**164** tk) — `report_agent_job_result` ToolSpec.
- **NEW:** `tool-request-permissions.md` (**138** tk) — `request_permissions` ToolSpec.
- **NEW:** `tool-request-user-input.md` (**231** tk) — `request_user_input` ToolSpec.
- **NEW:** `tool-resume-agent.md` (**97** tk) — `resume_agent` ToolSpec.
- **NEW:** `tool-send-input.md` (**202** tk) — `send_input` ToolSpec.
- **NEW:** `tool-send-message.md` (**137** tk) — `send_message` ToolSpec.
- **NEW:** `tool-shell-command-unix.md` (**211** tk) — `shell_command` ToolSpec.
- **NEW:** `tool-shell-command-windows.md` (**350** tk) — `shell_command` ToolSpec.
- **NEW:** `tool-shell-unix.md` (**179** tk) — `shell` ToolSpec.
- **NEW:** `tool-shell-windows.md` (**384** tk) — `shell` ToolSpec.
- **NEW:** `tool-spawn-agent-v2.md` (**318** tk) — `spawn_agent` ToolSpec.
- **NEW:** `tool-spawn-agent.md` (**883** tk) — `spawn_agent` ToolSpec.
- **NEW:** `tool-spawn-agents-on-csv.md` (**379** tk) — `spawn_agents_on_csv` ToolSpec.
- **NEW:** `tool-test-sync-tool.md` (**216** tk) — `test_sync_tool` ToolSpec.
- **NEW:** `tool-tool-suggest.md` (**662** tk) — `tool_suggest` ToolSpec.
- **NEW:** `tool-update-goal.md` (**165** tk) — `update_goal` ToolSpec.
- **NEW:** `tool-update-plan.md` (**123** tk) — `update_plan` ToolSpec.
- **NEW:** `tool-view-image.md` (**196** tk) — `view_image` ToolSpec.
- **NEW:** `tool-wait-agent-v2.md` (**103** tk) — `wait_agent` ToolSpec.
- **NEW:** `tool-wait-agent.md` (**99** tk) — `wait_agent` ToolSpec.
- **NEW:** `tool-write-stdin.md` (**197** tk) — `write_stdin` ToolSpec.

## `prompts/memory/`

- `memory-write-consolidation.md` — token Δ +0 (10,379 → 10,379).

## `prompts/orphan/`

- **NEW:** `orphan-models-manager-default-personality-header.md` (**30** tk) — `codex-rs/models-manager/src/model_info.rs::DEFAULT_PERSONALITY_HEADER`
- **NEW:** `orphan-models-manager-local-friendly-template.md` (**16** tk) — `codex-rs/models-manager/src/model_info.rs::LOCAL_FRIENDLY_TEMPLATE`
- **NEW:** `orphan-models-manager-local-pragmatic-template.md` (**10** tk) — `codex-rs/models-manager/src/model_info.rs::LOCAL_PRAGMATIC_TEMPLATE`
- `orphan-core-templates-search-tool-tool-suggest-description.md` — token Δ +17 (413 → 430).

---

# [rust-v0.126.0-alpha.12](https://github.com/openai/codex/releases/tag/rust-v0.126.0-alpha.12)

_+93,777 tokens_ (first extraction)

Initial extraction baseline at codex commit `ebdf3a878c8c7253504599bd384cd421a4e548c1`. All 91 captured files are NEW (no prior mirror snapshot).

## `prompts/base-instructions/` (8 files, 28,913 tokens)

- **NEW:** `base-instructions-codex-auto-review.md` (**2,991** tk) — Per-model `base_instructions` for slug `codex-auto-review`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/5/base_in…
- **NEW:** `base-instructions-default.md` (**4,371** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/protocol/src/prompts/base_instructions/default.md`. Category: base-instructions. Description will be refined at M5…
- **NEW:** `base-instructions-fallback.md` (**4,371** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/models-manager/prompt.md`. Category: base-instructions. Description will be refined at M5 review.
- **NEW:** `base-instructions-gpt-5.2.md` (**4,570** tk) — Per-model `base_instructions` for slug `gpt-5.2`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/4/base_instructions…
- **NEW:** `base-instructions-gpt-5.3-codex.md` (**2,551** tk) — Per-model `base_instructions` for slug `gpt-5.3-codex`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/3/base_instru…
- **NEW:** `base-instructions-gpt-5.4-mini.md` (**2,639** tk) — Per-model `base_instructions` for slug `gpt-5.4-mini`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/2/base_instruc…
- **NEW:** `base-instructions-gpt-5.4.md` (**2,991** tk) — Per-model `base_instructions` for slug `gpt-5.4`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/1/base_instructions…
- **NEW:** `base-instructions-gpt-5.5.md` (**4,429** tk) — Per-model `base_instructions` for slug `gpt-5.5`, fanned out from `codex-rs/models-manager/models.json` per SPEC §2.4. JSON pointer: /models/0/base_instructions…

## `prompts/mode/` (17 files, 8,872 tokens)

- **NEW:** `mode-collab-default.md` (**101** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/default.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-collab-execute.md` (**763** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/execute.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-collab-pair-programming.md` (**222** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/pair_programming.md`. Category: mode. Description will be refined at M5 revi…
- **NEW:** `mode-collab-plan.md` (**1,804** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/collaboration-mode-templates/templates/plan.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-compact-prompt.md` (**89** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/compact/prompt.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-compact-summary-prefix.md` (**77** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/compact/summary_prefix.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-goal-budget-limit.md` (**139** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/goals/budget_limit.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-goal-continuation.md` (**465** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/goals/continuation.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-guardian-output-contract.md` (**121** tk) — Guardian output JSON-schema contract appended to the policy prompt at runtime (defines outcome/risk_level/user_authorization fields).
- **NEW:** `mode-guardian-policy-template.md` (**1,416** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/guardian/policy_template.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-guardian-policy.md` (**1,042** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/guardian/policy.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-realtime-backend.md` (**954** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/realtime/backend_prompt.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-realtime-end.md` (**38** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/realtime/realtime_end.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-realtime-start.md` (**145** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/realtime/realtime_start.md`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-review-exit-interrupted.md` (**67** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_interrupted.xml`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-review-exit-success.md` (**59** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/templates/review/exit_success.xml`. Category: mode. Description will be refined at M5 review.
- **NEW:** `mode-review.md` (**1,370** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/review_prompt.md`. Category: mode. Description will be refined at M5 review.

## `prompts/permission/` (8 files, 1,357 tokens)

- **NEW:** `permission-approval-never.md` (**23** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/never.md`. Category: permission. Description will be refined a…
- **NEW:** `permission-approval-on-failure.md` (**60** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_failure.md`. Category: permission. Description will be refi…
- **NEW:** `permission-approval-on-request-rule-request-permission.md` (**333** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_request_rule_request_permission.md`. Category: permission.…
- **NEW:** `permission-approval-on-request.md` (**758** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/on_request.md`. Category: permission. Description will be refi…
- **NEW:** `permission-approval-unless-trusted.md` (**50** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/approval_policy/unless_trusted.md`. Category: permission. Description will be…
- **NEW:** `permission-sandbox-danger-full-access.md` (**40** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/danger_full_access.md`. Category: permission. Description will be…
- **NEW:** `permission-sandbox-read-only.md` (**36** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/read_only.md`. Category: permission. Description will be refined…
- **NEW:** `permission-sandbox-workspace-write.md` (**57** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/context/prompts/permissions/sandbox_mode/workspace_write.md`. Category: permission. Description will be re…

## `prompts/context-fragment/` (22 files, 1,304 tokens)

- **NEW:** `context-fragment-approved-command-prefix-saved.md` (**6** tk) — `ApprovedCommandPrefixSaved` ContextualUserFragment from `codex-rs/core/src/context/approved_command_prefix_saved.rs`. Role: 'developer'. Markers: '' … ''. body…
- **NEW:** `context-fragment-apps-instructions.md` (**143** tk) — `AppsInstructions` ContextualUserFragment from `codex-rs/core/src/context/apps_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as templat…
- **NEW:** `context-fragment-available-plugins-instructions.md` (**332** tk) — `AvailablePluginsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_plugins_instructions.rs`. Role: 'developer'. Markers: '' … ''. b…
- **NEW:** `context-fragment-available-skills-instructions.md` (**30** tk) — `AvailableSkillsInstructions` ContextualUserFragment from `codex-rs/core/src/context/available_skills_instructions.rs`. Role: 'developer'. Markers: '' … ''. bod…
- **NEW:** `context-fragment-collaboration-mode-instructions.md` (**18** tk) — `CollaborationModeInstructions` ContextualUserFragment from `codex-rs/core/src/context/collaboration_mode_instructions.rs`. Role: 'developer'. Markers: '' … ''.…
- **NEW:** `context-fragment-environment-context.md` (**335** tk) — `EnvironmentContext` ContextualUserFragment from `codex-rs/core/src/context/environment_context.rs`. Role: 'user'. Markers: '' … ''. body() captured as function…
- **NEW:** `context-fragment-guardian-followup-review-reminder.md` (**89** tk) — `GuardianFollowupReviewReminder` ContextualUserFragment from `codex-rs/core/src/context/guardian_followup_review_reminder.rs`. Role: 'developer'. Markers: '' ……
- **NEW:** `context-fragment-hook-additional-context.md` (**18** tk) — `HookAdditionalContext` ContextualUserFragment from `codex-rs/core/src/context/hook_additional_context.rs`. Role: 'developer'. Markers: '' … ''. body() captured…
- **NEW:** `context-fragment-image-generation-instructions.md` (**41** tk) — `ImageGenerationInstructions` ContextualUserFragment from `codex-rs/core/src/context/image_generation_instructions.rs`. Role: 'developer'. Markers: '' … ''. bod…
- **NEW:** `context-fragment-model-switch-instructions.md` (**28** tk) — `ModelSwitchInstructions` ContextualUserFragment from `codex-rs/core/src/context/model_switch_instructions.rs`. Role: 'developer'. Markers: '<model_switch>' … '…
- **NEW:** `context-fragment-network-rule-saved.md` (**85** tk) — `NetworkRuleSaved` ContextualUserFragment from `codex-rs/core/src/context/network_rule_saved.rs`. Role: 'developer'. Markers: '' … ''. body() captured as functi…
- **NEW:** `context-fragment-permissions-instructions.md` (**26** tk) — `PermissionsInstructions` ContextualUserFragment from `codex-rs/core/src/context/permissions_instructions.rs`. Role: 'developer'. Markers: '<permissions instruc…
- **NEW:** `context-fragment-personality-spec-instructions.md` (**31** tk) — `PersonalitySpecInstructions` ContextualUserFragment from `codex-rs/core/src/context/personality_spec_instructions.rs`. Role: 'developer'. Markers: '<personalit…
- **NEW:** `context-fragment-plugin-instructions.md` (**18** tk) — `PluginInstructions` ContextualUserFragment from `codex-rs/core/src/context/plugin_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() captured as fun…
- **NEW:** `context-fragment-realtime-end-instructions.md` (**5** tk) — `RealtimeEndInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_end_instructions.rs`. Role: 'developer'. Markers: '' … ''. body() capt…
- **NEW:** `context-fragment-realtime-start-instructions.md` (**2** tk) — `RealtimeStartInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_start_instructions.rs`. Role: 'developer'. Markers: '' … ''. body()…
- **NEW:** `context-fragment-realtime-start-with-instructions.md` (**2** tk) — `RealtimeStartWithInstructions` ContextualUserFragment from `codex-rs/core/src/context/realtime_start_with_instructions.rs`. Role: 'developer'. Markers: '' … ''…
- **NEW:** `context-fragment-skill-instructions.md` (**19** tk) — `SkillInstructions` ContextualUserFragment from `codex-rs/core/src/context/skill_instructions.rs`. Role: 'user'. Markers: '<skill>' … '</skill>'. body() capture…
- **NEW:** `context-fragment-subagent-notification.md` (**11** tk) — `SubagentNotification` ContextualUserFragment from `codex-rs/core/src/context/subagent_notification.rs`. Role: 'user'. Markers: '<subagent_notification>' … '</s…
- **NEW:** `context-fragment-turn-aborted.md` (**11** tk) — `TurnAborted` ContextualUserFragment from `codex-rs/core/src/context/turn_aborted.rs`. Role: 'user'. Markers: '<turn_aborted>' … '</turn_aborted>'. body() captu…
- **NEW:** `context-fragment-user-instructions.md` (**17** tk) — `UserInstructions` ContextualUserFragment from `codex-rs/core/src/context/user_instructions.rs`. Role: 'user'. Markers: '# AGENTS.md instructions for ' … '</INS…
- **NEW:** `context-fragment-user-shell-command.md` (**37** tk) — `UserShellCommand` ContextualUserFragment from `codex-rs/core/src/context/user_shell_command.rs`. Role: 'user'. Markers: '<user_shell_command>' … '</user_shell_…

## `prompts/tool/` (5 files, 8,435 tokens)

- **NEW:** `tool-apply-patch-instructions.md` (**752** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/apply-patch/apply_patch_tool_instructions.md`. Category: tool. Description will be refined at M5 review.
- **NEW:** `tool-apply-patch-json-description.md` (**706** tk) — JSON-API variant of the apply_patch tool description (paired with apply_patch_tool_instructions.md / apply_patch.lark grammar).
- **NEW:** `tool-consequential-message-templates.md` (**6,900** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/consequential_tool_message_templates.json`. Category: tool. Description will be refined at M5 review.
- **NEW:** `tool-spawn-agent-inherited-model-guidance.md` (**33** tk) — Guidance attached to spawn_agent's `model` parameter — inheritance default rule.
- **NEW:** `tool-spawn-agent-model-override-description.md` (**44** tk) — Description for spawn_agent's optional `model` override parameter.

## `prompts/agent/` (4 files, 852 tokens)

- **NEW:** `agent-builtin-awaiter.md` (**259** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/agent/builtins/awaiter.toml`. Category: agent. Description will be refined at M5 review.
- **NEW:** `agent-hierarchical-message.md` (**209** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/hierarchical_agents_message.md`. Category: agent. Description will be refined at M5 review.
- **NEW:** `agent-role-explorer.md` (**188** tk) — Explorer role description — inline string in role.rs DEFAULT_ROLE_CONFIG table.
- **NEW:** `agent-role-worker.md` (**196** tk) — Worker role description — inline string in role.rs DEFAULT_ROLE_CONFIG table.

## `prompts/memory/` (4 files, 18,057 tokens)

- **NEW:** `memory-read-read-path.md` (**1,532** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/read/templates/memories/read_path.md`. Category: memory. Description will be refined at M5 review.
- **NEW:** `memory-write-consolidation.md` (**10,379** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/consolidation.md`. Category: memory. Description will be refined at M5 review.
- **NEW:** `memory-write-stage-one-input.md` (**86** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/stage_one_input.md`. Category: memory. Description will be refined at M5 review.
- **NEW:** `memory-write-stage-one-system.md` (**6,060** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/memories/write/templates/memories/stage_one_system.md`. Category: memory. Description will be refined at M5 review.

## `prompts/code-mode/` (5 files, 1,427 tokens)

- **NEW:** `code-mode-deferred-nested-tools-guidance.md` (**76** tk) — Guidance noting that some nested MCP/app tools may be omitted from the description but are still callable via `tools` / `ALL_TOOLS`.
- **NEW:** `code-mode-exec-description-template.md` (**700** tk) — Code-mode `exec` tool description template — programmatic preface for the JS-orchestration `exec` tool.
- **NEW:** `code-mode-mcp-typescript-preamble.md` (**413** tk) — TypeScript schema preamble injected into code-mode tool description for the MCP nested-tool API.
- **NEW:** `code-mode-only-preface.md` (**76** tk) — Preface added when code-mode is the only tool exposure (no other MCP tools listed).
- **NEW:** `code-mode-wait-description-template.md` (**162** tk) — Code-mode `wait` tool description template (paired with `exec`).

## `prompts/tui/` (1 files, 322 tokens)

- **NEW:** `tui-init-command.md` (**322** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/tui/prompt_for_init_command.md`. Category: tui. Description will be refined at M5 review.

## `prompts/data/` (2 files, 513 tokens)

- **NEW:** `data-agent-names.md` (**340** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/core/src/agent/agent_names.txt`. Category: data. Description will be refined at M5 review.
- **NEW:** `data-apply-patch-grammar.md` (**173** tk) — Auto-extracted by Pass 3 (M2) from `codex-rs/tools/src/tool_apply_patch.lark`. Category: data. Description will be refined at M5 review.

## `prompts/orphan/` (15 files, 23,725 tokens)

- **NEW:** `orphan-core-gpt-5-1-codex-max-prompt.md` (**1,624** tk) — Orphan file at `codex-rs/core/gpt-5.1-codex-max_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.126.0-alp…
- **NEW:** `orphan-core-gpt-5-1-prompt.md` (**5,076** tk) — Orphan file at `codex-rs/core/gpt_5_1_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.126.0-alpha.12`. Pe…
- **NEW:** `orphan-core-gpt-5-2-codex-prompt.md` (**1,624** tk) — Orphan file at `codex-rs/core/gpt-5.2-codex_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.126.0-alpha.1…
- **NEW:** `orphan-core-gpt-5-2-prompt.md` (**4,570** tk) — Orphan file at `codex-rs/core/gpt_5_2_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.126.0-alpha.12`. Pe…
- **NEW:** `orphan-core-gpt-5-codex-prompt.md` (**1,436** tk) — Orphan file at `codex-rs/core/gpt_5_codex_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.126.0-alpha.12`…
- **NEW:** `orphan-core-prompt-with-apply-patch-instructions.md` (**5,123** tk) — Orphan file at `codex-rs/core/prompt_with_apply_patch_instructions.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-…
- **NEW:** `orphan-core-templates-agents-orchestrator.md` (**1,037** tk) — Orphan file at `codex-rs/core/templates/agents/orchestrator.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-v0.126.…
- **NEW:** `orphan-core-templates-collab-experimental-prompt.md` (**291** tk) — Orphan file at `codex-rs/core/templates/collab/experimental_prompt.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rust-…
- **NEW:** `orphan-core-templates-model-instructions-gpt-5-2-codex-instructions-template.md` (**1,573** tk) — Orphan file at `codex-rs/core/templates/model_instructions/gpt-5.2-codex_instructions_template.md`. Present in the upstream tree but NOT `include_str!`'d by any…
- **NEW:** `orphan-core-templates-personalities-gpt-5-2-codex-friendly.md` (**378** tk) — Orphan file at `codex-rs/core/templates/personalities/gpt-5.2-codex_friendly.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as…
- **NEW:** `orphan-core-templates-personalities-gpt-5-2-codex-pragmatic.md` (**335** tk) — Orphan file at `codex-rs/core/templates/personalities/gpt-5.2-codex_pragmatic.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate a…
- **NEW:** `orphan-core-templates-review-history-message-completed.md` (**59** tk) — Orphan file at `codex-rs/core/templates/review/history_message_completed.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of…
- **NEW:** `orphan-core-templates-review-history-message-interrupted.md` (**67** tk) — Orphan file at `codex-rs/core/templates/review/history_message_interrupted.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as o…
- **NEW:** `orphan-core-templates-search-tool-tool-description.md` (**119** tk) — Orphan file at `codex-rs/core/templates/search_tool/tool_description.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as of `rus…
- **NEW:** `orphan-core-templates-search-tool-tool-suggest-description.md` (**413** tk) — Orphan file at `codex-rs/core/templates/search_tool/tool_suggest_description.md`. Present in the upstream tree but NOT `include_str!`'d by any shipping crate as…


---

## Format

```markdown
# [rust-vX.Y.Z[-alpha.N]](https://github.com/openai/codex/releases/tag/rust-vX.Y.Z[-alpha.N])

_+/-N tokens_

- **NEW:** Category: name — `prompts/<category>/<file>.md`. (entirely new prompt files)
- Category: name — Token Δ +N. (modification — always include token Δ inline)
- **MOVED:** `old/path.md` → `new/path.md` (relocations; preserve token Δ if body unchanged)
- **REMOVED:** `prompts/<category>/<file>.md` — reason. (deletions)
```

When upstream tags are silently skipped (no prompt diff), the next material entry's header opens with `Spans upstream rust-vA..B; no prompt change in intermediate.` See SPEC §3.5 (T2.4).

The complete upstream tag log (including silent skips) is at [`data/upstream-tags.md`](./data/upstream-tags.md).
