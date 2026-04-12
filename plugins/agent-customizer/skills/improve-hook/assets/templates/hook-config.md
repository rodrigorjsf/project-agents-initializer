<!-- TEMPLATE: Hook Configuration
     Placement: .claude/settings.json hooks object, .claude/settings.local.json, or hooks/hooks.json (plugin)
     Rule: Valid hook events: SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest,
           PostToolUse, PostToolUseFailure, Notification, SubagentStart, SubagentStop,
           Stop, StopFailure, TeammateIdle, TaskCompleted, InstructionsLoaded,
           ConfigChange, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact,
           Elicitation, ElicitationResult, SessionEnd
     Rule: matcher field filters by tool name or pattern
     Rule: Exit codes: 0 = success; 2 = blocking error (effect is event-dependent: blocks PreToolUse/UserPromptSubmit/Stop; shows stderr for PostToolUse/SessionEnd/etc.)
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
