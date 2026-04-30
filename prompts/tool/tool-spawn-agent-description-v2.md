---
name: 'Tool: spawn_agent description'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:69
  tool_name: spawn_agent
  description_kind: fn_call_resolved
  resolves_via: spawn_agent_tool_description_v2
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 241
description: Inline ToolSpec description for `spawn_agent` (Pass 1.7, M9).
---
## Branch 1

This session is configured with `max_concurrent_threads_per_session = {limit}` for concurrently open agent threads.

## Branch 2

{agent_role_guidance}
        Spawns an agent to work on the specified task. If your current task is `/root/task1` and you spawn_agent with task_name "task_3" the agent will have canonical task name `/root/task1/task_3`.
You are then able to refer to this agent as `task_3` or `/root/task1/task_3` interchangeably. However an agent `/root/task2/task_3` would only be able to communicate with this agent via its canonical name `/root/task1/task_3`.
The spawned agent will have the same tools as you and the ability to spawn its own subagents.
{SPAWN_AGENT_INHERITED_MODEL_GUIDANCE}
It will be able to send you and other running agents messages, and its final answer will be provided to you when it finishes.
The new agent's canonical task name will be provided to it along with the message.
{concurrency_guidance}

## Branch 3

{tool_description}
{usage_hint_text}
