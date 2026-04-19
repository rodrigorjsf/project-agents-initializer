<!-- TEMPLATE: Hook Configuration
     Placement: .claude/settings.json hooks object, .claude/settings.local.json, or hooks/hooks.json (plugin)
     Rule: Valid hook events: SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest,
           PostToolUse, PostToolUseFailure, Notification, SubagentStart, SubagentStop,
           Stop, StopFailure, TeammateIdle, TaskCompleted, InstructionsLoaded,
           ConfigChange, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact,
           Elicitation, ElicitationResult, SessionEnd
     Rule: matcher field filters by tool name or pattern; UserPromptSubmit, Stop, TeammateIdle,
           TaskCompleted, WorktreeCreate, and WorktreeRemove do NOT support matchers (silently ignored)
     Rule: Exit-code handling is event-specific — do not apply one rule to all 22 events
     Rule: 0 = success; 2 = blocking error for events that support blocking; non-blocking for others
     Rule: Blocks execution on exit 2: PreToolUse, PermissionRequest, UserPromptSubmit, Stop,
           SubagentStop, TeammateIdle, TaskCompleted, ConfigChange, Elicitation, ElicitationResult
     Rule: Any non-zero exit code fails worktree creation (not just exit 2): WorktreeCreate
     Rule: Shows stderr only (non-blocking) on exit 2: PostToolUse, PostToolUseFailure, Notification,
           SubagentStart, SessionStart, SessionEnd, PreCompact, PostCompact
     Rule: Failures logged in debug mode only (not shown to user): WorktreeRemove
     Rule: Exit code ignored entirely: StopFailure, InstructionsLoaded
     Rule: For any event-specific behavior, use the canonical hook reference "Exit code 2 behavior
           per event" table rather than assuming defaults from this template
     Rule: Hook input arrives as JSON on stdin
-->

{
  "hooks": {
    "[HookEvent]": [
      {
        "matcher": "[tool-name-or-pattern]",
        "hooks": [
          {
            "type": "[command|prompt]",
            "[handler-key: command|prompt]": "[handler-value]"
          }
        ]
      }
    ]
  }
}
<!-- CONDITIONAL: If the hook blocks write operations, use a concrete matcher such as `Write|Edit|Create`
     instead of `"*"` or an omitted matcher. -->
