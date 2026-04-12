<!-- TEMPLATE: hook-config.md
  Placement: .cursor/hooks.json
  Format: JSON with version field and event-keyed hook arrays
  Rule: Hooks require Cursor; do NOT generate for standalone distribution
  Rule: Choose the hook event that matches when enforcement should trigger

  Hook events available:
  - sessionStart / sessionEnd
  - preToolUse / postToolUse / postToolUseFailure
  - subagentStart / subagentStop
  - beforeShellExecution / afterShellExecution
  - beforeMCPExecution / afterMCPExecution
  - beforeReadFile / afterFileEdit
  - beforeSubmitPrompt
  - preCompact
  - stop
  - afterAgentResponse / afterAgentThought

  Source: automation-migration-guide.md — Mechanism Comparison table

  MIGRATION: This template applies only in improve (not init) context.
  Only suggest hooks when the automation-migration-guide.md classifies
  an instruction as HOOK_CANDIDATE (deterministic enforcement).
-->

<!-- CONDITIONAL: Use command hooks for deterministic enforcement that needs
     no LLM judgment (formatting, file blocking, validation scripts).
     Zero context cost. Highest enforcement reliability (100%). -->
```json
{
  "version": 1,
  "hooks": {
    "[HOOK_EVENT]": [
      {
        "command": "[path/to/hook-script.sh or inline shell command]"
      }
    ]
  }
}
```

### When to Use Each Hook Event

| Event | Use Case |
|-------|----------|
| `afterFileEdit` | Run formatters, linters after edits |
| `beforeShellExecution` | Gate risky commands (e.g., SQL writes) |
| `stop` | Continue agent loop with `followup_message` |
| `sessionStart` | Inject context at conversation start |
| `preToolUse` | Validate tool arguments before execution |
| `postToolUseFailure` | Retry or log failed tool invocations |

### Hook Script Pattern

Scripts receive JSON on stdin and must output JSON on stdout:

```json
// Input (varies by event)
{
  "tool_name": "edit_file",
  "file_path": "src/index.ts",
  "conversation_id": "abc-123"
}

// Output options
{ }                                        // Allow (no modification)
{ "decision": "block", "reason": "..." }   // Block the action
{ "followup_message": "Continue..." }      // Resume agent (stop hook)
```
