# Hook Validation Criteria

Quality checklist for generated and improved Claude Code hook configurations.
Source: hooks/claude-hook-reference-doc.md, hooks/automate-workflow-with-hooks.md

---

## Hard Limits (Auto-fail if violated)

Any hook violating these criteria must be fixed before proceeding:

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| JSON structure | Valid JSON; no syntax errors | hooks/claude-hook-reference-doc.md |
| Event name | From recognized 22-event list | hooks/claude-hook-reference-doc.md lines 22-46 |
| Handler type | `command`, `http`, `prompt`, or `agent` only | hooks/claude-hook-reference-doc.md lines 249-257 |
| `command` path | Script file exists and is executable | hooks/automate-workflow-with-hooks.md |
| Exit code behavior | Exit 2 effect is event-dependent — see full table in hook reference | Blocks execution on exit 2: PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCompleted, ConfigChange, Elicitation, ElicitationResult, WorktreeCreate. Shows stderr only (non-blocking): PostToolUse, PostToolUseFailure, Notification, SubagentStart, SessionStart, SessionEnd, PreCompact, PostCompact, WorktreeRemove. Exit code ignored: StopFailure, InstructionsLoaded. |

*Source: hooks/claude-hook-reference-doc.md "Exit code 2 behavior per event" table*

---

## Quality Checks (All must pass)

- [ ] Event type matches intent (PreToolUse for blocking, PostToolUse for observation)
- [ ] Matcher is specific (not `"*"` for blocking hooks)
- [ ] Error handling defined: exit 2 with meaningful stderr for blockable events; non-blockable events should provide informative stderr
- [ ] Silent success uses exit 0 (not leaving stderr output that confuses verbose mode)
- [ ] Secrets not hardcoded in `command` string (use environment variables)
- [ ] `command` hook used for deterministic checks (not `agent` for simple regex checks)
- [ ] `prompt` or `agent` hook used only when judgment is genuinely required

---

## If This Is an IMPROVE Operation — Also Check

**Information Preservation:**

- [ ] Existing blocking behavior not weakened (exit 2 not changed to exit 0)
- [ ] Matcher not broadened unintentionally (specific regex not replaced with `"*"`)
- [ ] Valid hooks not removed while fixing structure

**Structural:**

- [ ] Hook location remains appropriate (settings.json scope matches intended sharing)
- [ ] Multiple hooks for same event not consolidated if they serve different purposes

---

## Validation Loop Instructions

Execute this loop for each generated or improved hook:

1. Evaluate the hook against ALL criteria above
2. If ANY criterion fails: identify the specific failure, fix the hook, restart evaluation
3. Maximum 3 iterations — if still failing after 3 attempts, surface the remaining issues to the user
4. Only proceed to writing hooks when ALL criteria pass

**Do not skip criteria for "minor" violations.** Hard limits are hard limits.
