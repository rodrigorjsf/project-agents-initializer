<!-- TEMPLATE: Hook Configuration Snippet (generated from automation migration)
     Placement: Merge into `.claude/settings.json` under the `hooks` key — NOT a standalone file
     Rule: Hooks require Claude Code; do NOT generate for standalone distribution
     Rule: Choose the hook event that matches when enforcement should trigger
     Rule: Use `matcher` to scope hooks to specific tools (glob-style tool name matching)
     Available hook events (22 total): PreToolUse, PostToolUse, Stop, SessionStart,
       UserPromptSubmit, plus 17 others across session, subagent, compaction, and control lifecycles
     Source: automation-migration-guide.md — Mechanism Comparison table
-->

<!-- CONDITIONAL: Use `command` type ONLY for deterministic enforcement that needs
     no LLM judgment (formatting, file blocking, validation scripts).
     Zero context cost. Highest enforcement reliability (100%). -->
{
  "hooks": {
    "[PreToolUse|PostToolUse|Stop|SessionStart|UserPromptSubmit]": [
      {
        "matcher": "[tool-name-pattern]",
        "hooks": [
          {
            "type": "command",
            "command": "[path/to/hook-script.sh or inline shell command]"
          }
        ]
      }
    ]
  }
}

<!-- CONDITIONAL: Use `prompt` type ONLY when enforcement requires LLM judgment
     (single-turn decision). Model returns {"ok": true} to proceed or
     {"ok": false, "reason": "..."} to block. Default model: Haiku. -->
{
  "hooks": {
    "[PreToolUse|PostToolUse|Stop]": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "[Describe what to check. Instruct model to respond with {\"ok\": false, \"reason\": \"...\"} if condition is not met.]"
          }
        ]
      }
    ]
  }
}

<!-- CONDITIONAL: Use `agent` type ONLY when verification requires inspecting files
     or running commands (multi-turn with tools). Same ok/reason format as prompt.
     Default timeout: 60s, up to 50 tool-use turns. -->
{
  "hooks": {
    "[PreToolUse|PostToolUse|Stop]": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "[Describe what to verify against the codebase state. Agent can read files and run commands.]",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
