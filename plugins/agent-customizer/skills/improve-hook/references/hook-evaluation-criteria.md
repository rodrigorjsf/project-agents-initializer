# Hook Evaluation Criteria

Scoring rubric for assessing existing Claude Code hook configurations before improvement.
Source: hooks/claude-hook-reference-doc.md, hooks/automate-workflow-with-hooks.md

---

## Contents

- Hard limits table (JSON validity, recognized events, valid matchers)
- Bloat indicators table (overly broad matchers, redundant hooks)
- Staleness indicators table (deprecated events, invalid tools)
- Quality assessment (event selection, error handling, security)
- Quality score rubric (5-dimension scoring 1-10)
- Evaluation output template

---

## Hard Limits Table

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| JSON configuration | Valid JSON, no syntax errors | hooks/claude-hook-reference-doc.md |
| Event name | From recognized 22-event list | hooks/claude-hook-reference-doc.md lines 22-46 |
| Handler type | `command`, `http`, `prompt`, or `agent` | hooks/claude-hook-reference-doc.md lines 249-257 |
| Matcher field | Valid regex string or empty | hooks/claude-hook-reference-doc.md lines 162-179 |
| Command path | Executable file exists or is a valid command | hooks/automate-workflow-with-hooks.md |

A hook configuration violating any hard limit is flagged **INVALID** regardless of intent.

*Source: hooks/claude-hook-reference-doc.md lines 132-200*

---

## Bloat Indicators Table

| Indicator | Why It's Bloat |
|-----------|---------------|
| Overly broad matcher (`"*"` or `""`) for blocking hooks | Fires on every tool use; high performance cost |
| Multiple hooks for the same event doing redundant work | Consolidate into one hook with combined logic |
| `agent` hook when `command` hook suffices | Agent hooks have 60s overhead; use command for deterministic checks |
| `prompt` hook when `command` hook suffices | Prompt hooks add LLM cost; use command for regex/pattern checks |
| Hook commands that always exit 0 (never block) | Observation-only hooks should use PostToolUse, not PreToolUse |
| Sensitive data in `command` string of settings.json | Use environment variables instead |

*Source: hooks/automate-workflow-with-hooks.md lines 569-625*

---

## Staleness Indicators Table

| Indicator | How to Detect |
|-----------|---------------|
| Deprecated event names | Verify against current 22-event reference list |
| Invalid tool names in matcher | Check tool names against current Claude Code tools |
| Hardcoded absolute paths to scripts that don't exist | Verify each `command` script path exists |
| Outdated matcher values (e.g., old session end reasons) | Verify against current matcher value lists |

*Source: hooks/claude-hook-reference-doc.md lines 162-179*

---

## Quality Assessment

| Question | Good | Bad |
|----------|------|-----|
| Event type matches intent? | `PreToolUse` for blocking, `PostToolUse` for formatting | Using `PostToolUse` to try to block actions |
| Matcher is specific, not `"*"`? | `"Edit\|Write"` for file hooks | `"*"` on a blocking hook |
| Error handling defined? | Exit 2 with clear stderr message | Silent failure (exit 0 always) |
| Security posture appropriate? | Hook validates before allowing | Hook only logs, never blocks |
| Hook type appropriate for task? | `command` for deterministic, `prompt` for judgment | `agent` for a simple grep check |

*Source: hooks/automate-workflow-with-hooks.md lines 1-13*

---

## Quality Score Rubric

| Dimension | 8-10 (Good) | 4-7 (Mixed) | 1-3 (Bad) |
|-----------|-------------|-------------|-----------|
| Event Selection | Event matches intent; blocking uses PreToolUse | Some mismatches | Events don't match intent |
| Matcher Specificity | Specific regex; no unnecessary `"*"` | Some broad matchers | All matchers are `"*"` |
| Error Handling | Exit 2 with reason; stderr feedback | Some events handled | Silent failures only |
| Security Posture | Validates before allowing; secrets in env vars | Partial validation | No blocking, secrets exposed |
| Handler Efficiency | Right type for each task | Some oversized handlers | Agent hooks for trivial tasks |
| **Overall** | | | |

*Source: hooks/claude-hook-reference-doc.md lines 249-257*

---

## Evaluation Output Template

```
## Hook Evaluation Results

### Hooks Found
| Event | Matcher | Type | Status |
|-------|---------|------|--------|
| `PreToolUse` | `"*"` | command | ⚠️ Overly broad matcher |
| `PostToolUse` | `"Edit\|Write"` | command | ✅ |

### Issues

**Bloat Issues:**
- PreToolUse matcher `"*"`: fires on every tool use; narrow to specific tool

**Error Handling Issues:**
- hook-validate.sh always exits 0; never blocks — PreToolUse hook has no effect

### Quality Score
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Event Selection | 8 | Events match intent |
| Matcher Specificity | 3 | `"*"` on blocking hook |
| Error Handling | 2 | Always exits 0 |
| Security Posture | 4 | Intent to validate, no enforcement |
| Handler Efficiency | 7 | Appropriate types |
| **Overall** | **5** | Fix matcher and exit codes |
```
