<!-- TEMPLATE: Hook Configuration
     Placement: <project-root>/.cursor/hooks.json (project) or ~/.cursor/hooks.json (user)
     Format: JSON with `version` and `hooks` keys; each event maps to an array of definitions
     Rule: Use only Cursor-native event names (camelCase). Reject any name that is not in
           `references/hook-events-reference.md`.
     Rule: Valid Agent events: sessionStart, sessionEnd, preToolUse, postToolUse,
           postToolUseFailure, subagentStart, subagentStop, beforeShellExecution,
           afterShellExecution, beforeMCPExecution, afterMCPExecution, beforeReadFile,
           afterFileEdit, beforeSubmitPrompt, preCompact, stop, afterAgentResponse,
           afterAgentThought
     Rule: Valid Tab events: beforeTabFileRead, afterTabFileEdit
     Rule: Handler types are `command` (default) or `prompt` only — there is no `http` or
           `agent` handler in Cursor's native model
     Rule: Matchers apply only to events documented as supporting matchers in
           `references/hook-events-reference.md`. Setting a matcher on an event that does
           not support one (e.g., sessionStart, beforeMCPExecution, afterMCPExecution,
           preCompact, beforeTabFileRead, afterTabFileEdit) is a structural error
     Rule: Exit-code semantics — `0` = success, `2` = block; other non-zero exits fail open
           by default. Set `"failClosed": true` on security-critical blocking hooks
           (beforeMCPExecution, beforeShellExecution, beforeReadFile) so a crash, timeout,
           or invalid-JSON response blocks the action
     Rule: Hook input arrives as JSON on stdin; the script's stdout JSON is consumed for
           `permission`, `additional_context`, `updated_input`, etc.
-->

<!-- Emit raw JSON only. Do not include Markdown headings, tables, prose, or code fences in
     the generated `.cursor/hooks.json`. -->
{
  "version": 1,
  "hooks": {
    "[hookEvent]": [
      {
        "command": "[script-path-or-shell-string]",
        "matcher": "[regex-string-or-omit-when-event-has-no-matcher-field]",
        "timeout": 30,
        "failClosed": false
      }
    ]
  }
}

<!-- CONDITIONAL: For blocking events (preToolUse, beforeShellExecution, beforeMCPExecution,
     beforeReadFile, beforeSubmitPrompt, subagentStart) provide a concrete matcher when the
     event supports one. Avoid omitting the matcher just to fire on every occurrence. -->

<!-- CONDITIONAL: For prompt-handler hooks, replace the per-script body with:
     {
       "type": "prompt",
       "prompt": "[natural-language criterion; $ARGUMENTS is auto-replaced with hook input]",
       "timeout": 10
     }
     Use `prompt` only when natural-language judgment is genuinely required. -->
