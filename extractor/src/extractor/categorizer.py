"""Path-rule-based categorization (SPEC §3.2, §4).

Each rule maps a substring match in the target_rel path → (category, filename
without .md extension). First-match wins. Unmatched candidates fall through
to category='orphan'.

Rules are intentionally explicit and curated rather than glob-pattern-based:
the prompt set is small (~50 files), and explicit rules make the
categorization auditable and easy to extend.
"""

from __future__ import annotations

from pathlib import Path

# (path_substring, category, filename_template)
# {stem} = target file stem (basename without extension), with underscores → hyphens.
RULES: list[tuple[str, str, str]] = [
    # ============ Tool descriptions (static) ============
    ("apply-patch/apply_patch_tool_instructions.md", "tool", "tool-apply-patch-instructions"),
    ("tools/src/tool_apply_patch.lark", "data", "data-apply-patch-grammar"),
    ("apply_patch.lark", "data", "data-apply-patch-grammar"),
    # ============ Mode prompts ============
    ("core/review_prompt.md", "mode", "mode-review"),
    ("core/templates/review/exit_success.xml", "mode", "mode-review-exit-success"),
    ("core/templates/review/exit_interrupted.xml", "mode", "mode-review-exit-interrupted"),
    ("core/templates/compact/prompt.md", "mode", "mode-compact-prompt"),
    ("core/templates/compact/summary_prefix.md", "mode", "mode-compact-summary-prefix"),
    ("core/src/context/prompts/realtime/realtime_start.md", "mode", "mode-realtime-start"),
    ("core/src/context/prompts/realtime/realtime_end.md", "mode", "mode-realtime-end"),
    ("core/templates/realtime/backend_prompt.md", "mode", "mode-realtime-backend"),
    ("core/templates/goals/continuation.md", "mode", "mode-goal-continuation"),
    ("core/templates/goals/budget_limit.md", "mode", "mode-goal-budget-limit"),
    ("core/src/guardian/policy_template.md", "mode", "mode-guardian-policy-template"),
    ("core/src/guardian/policy.md", "mode", "mode-guardian-policy"),
    ("collaboration-mode-templates/templates/default.md", "mode", "mode-collab-default"),
    ("collaboration-mode-templates/templates/execute.md", "mode", "mode-collab-execute"),
    ("collaboration-mode-templates/templates/plan.md", "mode", "mode-collab-plan"),
    ("collaboration-mode-templates/templates/pair_programming.md", "mode", "mode-collab-pair-programming"),
    # ============ Permissions ============
    ("core/src/context/prompts/permissions/approval_policy/", "permission", "permission-approval-{stem}"),
    ("core/src/context/prompts/permissions/sandbox_mode/", "permission", "permission-sandbox-{stem}"),
    # ============ Memory / skills ============
    ("memories/read/templates/", "memory", "memory-read-{stem}"),
    ("memories/write/templates/", "memory", "memory-write-{stem}"),
    # ============ TUI ============
    ("tui/prompt_for_init_command.md", "tui", "tui-init-command"),
    # ============ Agents ============
    ("core/hierarchical_agents_message.md", "agent", "agent-hierarchical-message"),
    ("core/src/agent/builtins/explorer.toml", "agent", "agent-builtin-explorer"),
    ("core/src/agent/builtins/awaiter.toml", "agent", "agent-builtin-awaiter"),
    ("core/src/agent/agent_names.txt", "data", "data-agent-names"),
    ("agent_names.txt", "data", "data-agent-names"),
    # ============ Base instructions (fallback files; per-model fan-out is separate) ============
    ("models-manager/prompt.md", "base-instructions", "base-instructions-fallback"),
    ("protocol/src/prompts/base_instructions/default.md", "base-instructions", "base-instructions-default"),
    # ============ Tool: MCP-related ============
    ("core/src/consequential_tool_message_templates.json", "tool", "tool-consequential-message-templates"),
    # ============ Code mode (where applicable as files) ============
    # (most code-mode content is inline in description.rs; M5 will capture)
    # ============ Announcement tip ============
    ("announcement_tip.toml", "data", "data-announcement-tip"),
]


def categorize(target_rel: Path) -> tuple[str, str] | None:
    """Return (category, filename_no_ext) or None if no rule matches."""
    rel = str(target_rel).replace("\\", "/")
    for pattern, category, filename_template in RULES:
        if pattern in rel:
            stem = target_rel.stem.replace("_", "-")
            filename = filename_template.format(stem=stem)
            return (category, filename)
    return None
