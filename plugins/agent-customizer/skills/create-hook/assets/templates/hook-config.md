<!-- TEMPLATE: Hook Configuration
     Placement: .claude/settings.json hooks object, .claude/settings.local.json, or hooks/hooks.json (plugin)
     Rule: Valid hook events: PreToolUse, PostToolUse, Notification, Stop, SubagentStop,
           PreCompact, PostCompact, PrePromptSubmit, PromptSubmitAfterModel,
           PostPromptSubmit, PreToolUseRejected, PreHaiku, PreApiRequest
     Rule: matcher field filters by tool name or pattern
     Rule: Exit codes: 0 = proceed, 1 = error (shown to user), 2 = block operation
     Rule: Hook input arrives as JSON on stdin
-->

{
  "hooks": {
    "[HookEvent]": [
      {
        "matcher": "[tool-name-or-pattern]",
        "hooks": [
          {
            "type": "command",
            "command": "[shell-command-to-execute]"
          }
        ]
      }
    ]
  }
}

<!-- CONDITIONAL: For prompt-type hooks (no external command needed) -->
{
  "hooks": {
    "[HookEvent]": [
      {
        "matcher": "[tool-name-or-pattern]",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "[instruction-for-Claude]"
          }
        ]
      }
    ]
  }
}
