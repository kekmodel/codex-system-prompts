---
name: 'Tool: spawn_agent'
category: tool
codex_version: rust-v0.128.0-alpha.1
codex_commit: 8148b7b1f8660e464661743587f754471ae60868
source:
  path: codex-rs/tools/src/agent_tool.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/agent_tool.rs:69
  tool_name: spawn_agent
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 313
description: '`spawn_agent` ToolSpec.'
---
{
  "type": "function",
  "name": "spawn_agent",
  "description": "\n        {agent_role_guidance}\n        Spawns an agent to work on the specified task. If your current task is `/root/task1` and you spawn_agent with task_name \"task_3\" the agent will have canonical task name `/root/task1/task_3`.\nYou are then able to refer to this agent as `task_3` or `/root/task1/task_3` interchangeably. However an agent `/root/task2/task_3` would only be able to communicate with this agent via its canonical name `/root/task1/task_3`.\nThe spawned agent will have the same tools as you and the ability to spawn its own subagents.\nSpawned agents inherit your current model by default. Omit `model` to use that preferred default; set `model` only when an explicit override is needed.\nIt will be able to send you and other running agents messages, and its final answer will be provided to you when it finishes.\nThe new agent's canonical task name will be provided to it along with the message.\n{concurrency_guidance}",
  "parameters": {
    "type": "object",
    "properties": {
      "task_name": {
        "type": "string",
        "description": "Task name for the new agent. Use lowercase letters, digits, and underscores."
      }
    },
    "additionalProperties": false
  }
}
