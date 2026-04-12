# Hook Events Reference

Complete reference for all 22 Claude Code hook events: triggers, matcher fields, and input/output schemas.
Source: hooks/claude-hook-reference-doc.md

---

## Contents

- Event summary table (all 22 events)
- Matcher field by event type
- JSON configuration schema
- Handler type support matrix
- Common patterns (pre-validation, post-formatting, session injection)

---

## Event Summary Table

| Event | When it fires | Can block? |
|-------|--------------|-----------|
| `SessionStart` | Session begins or resumes | No |
| `SessionEnd` | Session terminates | No |
| `UserPromptSubmit` | Before Claude processes your prompt | Yes |
| `PreToolUse` | Before any tool call executes | Yes |
| `PermissionRequest` | When a permission dialog would appear | Yes (auto-approve) |
| `PostToolUse` | After a tool call succeeds | Yes (feedback) |
| `PostToolUseFailure` | After a tool call fails | No (context only) |
| `Notification` | When Claude sends a notification | No |
| `SubagentStart` | When a subagent spawns | No (inject context) |
| `SubagentStop` | When a subagent finishes | Yes |
| `Stop` | When Claude finishes responding | Yes (force continue) |
| `StopFailure` | When turn ends due to API error | No |
| `TeammateIdle` | When team agent goes idle | No |
| `TaskCompleted` | When a task is marked complete | Yes |
| `InstructionsLoaded` | When CLAUDE.md or rules load | No |
| `ConfigChange` | When a config file changes | Yes (except policy) |
| `WorktreeCreate` | When a worktree is being created | Replaces behavior |
| `WorktreeRemove` | When a worktree is being removed | No |
| `PreCompact` | Before context compaction | No |
| `PostCompact` | After context compaction | No |
| `Elicitation` | When MCP server requests input | Yes |
| `ElicitationResult` | After user responds to MCP elicitation | Yes |

*Source: hooks/claude-hook-reference-doc.md lines 22-46*

---

## Matcher Field by Event Type

| Event | Matcher filters on | Example values |
|-------|-------------------|----------------|
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` | `tool_name` | `Bash`, `Edit\|Write`, `mcp__.*` |
| `SessionStart` | start reason | `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | end reason | `clear`, `resume`, `logout`, `prompt_input_exit` |
| `SubagentStart`, `SubagentStop` | agent type | `Explore`, `Plan`, `general-purpose` |
| `Notification` | notification type | `permission_prompt`, `idle_prompt`, `auth_success` |
| `PreCompact`, `PostCompact` | trigger | `manual`, `auto` |
| `ConfigChange` | config source | `user_settings`, `project_settings`, `local_settings`, `skills` |
| `StopFailure` | error type | `rate_limit`, `billing_error`, `server_error`, `unknown` |
| `InstructionsLoaded` | load reason | `session_start`, `nested_traversal`, `path_glob_match` |
| `Elicitation`, `ElicitationResult` | MCP server name | your configured server names |
| No matcher | always fires | `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` |

*Source: hooks/claude-hook-reference-doc.md lines 162-179*

---

## JSON Configuration Schema

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<regex-string>",
        "hooks": [
          {
            "type": "command",
            "command": "<shell-command-or-path>",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Handler type fields:

- `command`: `type`, `command` (required), `timeout` (optional, seconds)
- `http`: `type`, `url` (required), `timeout` (optional)
- `prompt`: `type`, `prompt` (required), `model` (optional, default Haiku), `timeout`
- `agent`: `type`, `prompt` (required), `timeout` (optional, default 60s)

*Source: hooks/claude-hook-reference-doc.md lines 258-310*

---

## Handler Type Support Matrix

| Handler type | Session events | Agentic loop events | Notes |
|-------------|---------------|--------------------|----|
| `command` | All 22 events | All 22 events | Universal; default choice |
| `http` | No | 8 agentic loop events only | Requires external endpoint |
| `prompt` | No | 8 agentic loop events only | Uses Claude Haiku by default |
| `agent` | No | 8 agentic loop events only | Up to 50 tool-use turns |

The 8 agentic loop events that support all handler types:
`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `TaskCompleted`

*Source: hooks/claude-hook-reference-doc.md lines 249-257*

---

## Common Patterns

### Pre-validation (PreToolUse + Bash)

Intercept Bash tool calls to block dangerous commands:

```json
{ "hooks": { "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": ".claude/hooks/validate.sh" }] }] } }
```

Exit 2 with stderr message to block; exit 0 to allow.

### Post-formatting (PostToolUse + Edit|Write)

Auto-format after file writes:

```json
{ "hooks": { "PostToolUse": [{ "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": ".claude/hooks/format.sh" }] }] } }
```

### Session injection (SessionStart + startup)

Inject dynamic context at session start:

```json
{ "hooks": { "SessionStart": [{ "matcher": "startup", "hooks": [{ "type": "command", "command": ".claude/hooks/inject-context.sh" }] }] } }
```

Stdout from the hook is injected as additional context.

*Source: hooks/automate-workflow-with-hooks.md lines 70-200*
