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
<!-- Emit raw JSON only. Do not include Markdown headings, tables, prose, or code fences in the generated `.cursor/hooks.json`. -->
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
