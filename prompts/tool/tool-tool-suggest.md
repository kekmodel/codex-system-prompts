---
name: 'Tool: tool_suggest'
category: tool
codex_version: rust-v0.129.0-alpha.1
codex_commit: 4d8f88e1458d931b940c27dd93e43e6b4b6cf92f
source:
  path: codex-rs/tools/src/tool_discovery.rs
  kind: rust_toolspec_inline
  reached_from:
  - tools/src/tool_discovery.rs:305
  tool_name: tool_suggest
extraction:
  pass: 1.7
  method: rust_toolspec_inline
variables: []
tokens:
  o200k_base: 662
description: '`tool_suggest` ToolSpec.'
---
```json
{
  "type": "function",
  "name": "tool_suggest",
  "description": "# Tool suggestion discovery\n\nUse this tool only to ask the user to install one known plugin or connector from the list below. The list contains known candidates that are not currently installed.\n\nUse this ONLY when all of the following are true:\n- The user explicitly wants a specific plugin or connector that is not already available in the current context or active `tools` list.\n- `{TOOL_SEARCH_TOOL_NAME}` is not available, or it has already been called and did not find or make the requested tool callable.\n- The tool is one of the known installable plugins or connectors listed below. Only ask to install tools from this list.\n\nDo not use tool suggestion for adjacent capabilities, broad recommendations, or tools that merely seem useful. The user's intent must clearly match one listed tool.\n\nKnown plugins/connectors available to install:\n{discoverable_tools}\n\nWorkflow:\n\n1. Check the current context and active `tools` list first. If `{TOOL_SEARCH_TOOL_NAME}` is available, call `{TOOL_SEARCH_TOOL_NAME}` before calling `{TOOL_SUGGEST_TOOL_NAME}`. Do not use tool suggestion if the needed tool is already available, found through `{TOOL_SEARCH_TOOL_NAME}`, or callable after discovery.\n2. Match the user's explicit request against the known plugin/connector list above. Only proceed when one listed plugin or connector exactly fits.\n3. If we found both connectors and plugins to suggest, use plugins first, only use connectors if the corresponding plugin is installed but the connector is not.\n4. If one tool clearly fits, call `{TOOL_SUGGEST_TOOL_NAME}` with:\n   - `tool_type`: `connector` or `plugin`\n   - `action_type`: `install`\n   - `tool_id`: exact id from the known plugin/connector list above\n   - `suggest_reason`: concise one-line user-facing reason this tool can help with the current request\n5. After the suggestion flow completes:\n   - if the user finished the install flow, continue by searching again or using the newly available tool\n   - if the user did not finish, continue without that tool, and don't suggest that tool again unless the user explicitly asks for it.\n\nIMPORTANT: DO NOT call this tool in parallel with other tools.",
  "parameters": {
    "type": "object",
    "properties": {
      "tool_type": {
        "type": "string",
        "description": "Type of discoverable tool to suggest. Use \"connector\" or \"plugin\"."
      },
      "action_type": {
        "type": "string",
        "description": "Suggested action for the tool. Use \"install\"."
      },
      "tool_id": {
        "type": "string",
        "description": "Connector or plugin id to suggest."
      },
      "suggest_reason": {
        "type": "string",
        "description": "Concise one-line user-facing reason why this tool can help with the current request."
      }
    },
    "additionalProperties": false
  }
}
```
