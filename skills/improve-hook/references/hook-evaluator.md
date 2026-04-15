# Hook Evaluation Instructions

Structured process for evaluating hook configurations against evidence-based quality criteria.
Used by IMPROVE-HOOK skill for current state analysis. Source: agents/hook-evaluator.md

---

## Contents

- [Constraints](#constraints)
- [Quality Criteria](#quality-criteria)
  - [Hard Limits](#hard-limits-auto-fail-if-violated)
  - [Valid Hook Event Types](#valid-hook-event-types)
  - [Quality Checks](#quality-checks)
- [Process](#process)
- [Output Format](#output-format)
- [Self-Verification](#self-verification)

---

Follow these evaluation instructions. Analyze the target hook configuration and evaluate it against evidence-based criteria. Identify specific problems with evidence so the improve-hook workflow can act on them.

## Constraints

- Do not modify any files — only analyze and report
- Do not suggest improvements — only identify problems with evidence
- Do not evaluate non-hook artifacts (skills, rules, subagents)
- Be specific: cite exact JSON paths and values for each issue found

## Quality Criteria

### Hard Limits (Auto-fail if violated)

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| JSON structure | Valid JSON; no syntax errors | hooks/claude-hook-reference-doc.md |
| Event name | From recognized event list | hooks/claude-hook-reference-doc.md lines 22-46 |
| Handler type | `command`, `http`, `prompt`, or `agent` only | hooks/claude-hook-reference-doc.md lines 249-257 |
| `command` path | Script file exists and is executable | hooks/automate-workflow-with-hooks.md |
| Exit code behavior | Exit 2 effect is event-dependent | Blocks: PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop. Shows stderr only (non-blocking): PostToolUse, PostToolUseFailure, SessionStart, SessionEnd, PreCompact, PostCompact, Notification. StopFailure ignores exit code entirely. |

### Valid Hook Event Types

SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse,
PostToolUseFailure, Notification, SubagentStart, SubagentStop, Stop, StopFailure,
TeammateIdle, TaskCompleted, InstructionsLoaded, ConfigChange, WorktreeCreate,
WorktreeRemove, PreCompact, PostCompact, Elicitation, ElicitationResult, SessionEnd

### Quality Checks

| Criterion | Pass Condition |
|-----------|---------------|
| Event matches intent | PreToolUse for blocking, PostToolUse for observation |
| Matcher specificity | Not `"*"` for blocking hooks |
| Error handling | Exit 2 with meaningful stderr for blockable events; non-blockable events should still provide informative stderr |
| Silent success | Exit 0 without spurious stderr output |
| No hardcoded secrets | `command` uses environment variables, not literal secrets |
| Correct hook type | `command` for deterministic; `prompt`/`agent` only when judgment needed |

## Process

### 1. Locate Hook Configuration

Search for hook definitions in:

- `.claude/settings.json` — hooks key
- `.claude/settings.local.json` — hooks key (if exists)
- Plugin `hooks/hooks.json` — if plugin-scoped hooks

### 2. Check Against Criteria

Evaluate every hook definition against the Quality Criteria above:

1. Validate JSON structure first — parse errors are AUTO-FAIL
2. Check each event name against the valid event types list
3. Check handler type for each hook entry
4. For `command` type: verify the script path exists and is executable
5. Check matcher applicability: matchers are supported by PreToolUse, PostToolUse*, PermissionRequest, SessionStart/End, Notification, ConfigChange; matchers are silently ignored for UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCompleted, WorktreeCreate, WorktreeRemove — flag any matcher set on ignored-matcher events
6. Check for hardcoded secrets in command strings

### 3. Compile Findings

Organize all issues by severity:

- AUTO-FAIL: Hard limit violations
- HIGH: Security issues or blocking hooks that may not work correctly
- MEDIUM: Specificity or handler type mismatches
- LOW: Style or documentation gaps

## Output Format

Return your analysis in exactly this format:

```
## Hook Evaluation Results

### Hooks Found
| Event | Matcher | Type | Location |
|-------|---------|------|----------|
| [event] | [matcher] | [type] | [file] |

### Hard Limit Check
| Criterion | Status | Evidence |
|-----------|--------|---------|
| Valid JSON | ✅/❌ | [parse result] |
| Valid event names | ✅/❌ | [event list or "invalid: X"] |
| Valid handler types | ✅/❌ | [types found or "invalid: X"] |
| Command paths exist | ✅/❌ | [path check result] |

### Quality Issues
- [Hook: event/matcher]: [Description of issue] — [criterion violated]

### Security Issues
- [Hook: event/matcher]: [Description of security concern]

### Summary
| Severity | Count |
|----------|-------|
| AUTO-FAIL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |

Overall Status: [PASS | FAIL]
```

## Self-Verification

Before returning results:

1. Every reported issue cites the specific hook (event + matcher) it applies to
2. Hard limit violations are correctly classified as AUTO-FAIL
3. No improvement suggestions included — report only identifies problems
4. Valid event names verified against the list in Quality Criteria — no false positives
5. All criteria in the Quality Criteria section were evaluated — none skipped
