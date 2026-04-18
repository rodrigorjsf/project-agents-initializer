# Claude Code Hooks

**Summary**: Deterministic automation points in the Claude Code lifecycle that execute shell commands, HTTP requests, LLM prompts, or agent-based verification at specific events — enabling formatting, validation, auditing, and control flow without relying on the model's judgment.
**Sources**: automate-workflow-with-hooks.md, claude-hook-reference-doc.md, analysis-automate-workflow-with-hooks.md, analysis-claude-hook-reference-doc.md
**Last updated**: 2026-04-18

---

## Why Hooks

Hooks provide **deterministic control** — they run reliably regardless of the model's behavior. Use hooks to enforce rules that must always apply, not as suggestions the model might follow. For decisions requiring judgment rather than deterministic rules, use [[#Prompt-Based Hooks]] or [[#Agent-Based Hooks]].

## Hook Types

| Type        | Mechanism                                | Use Case                                   | Default Timeout |
| ----------- | ---------------------------------------- | ------------------------------------------ | --------------- |
| **Command** | Shell script execution                   | Formatting, file protection, audit logging | 600s (10 min)   |
| **HTTP**    | POST to external endpoint                | Notifications, CI triggers, webhooks       | 30s             |
| **Prompt**  | Single-turn Claude evaluation            | Conditional logic, policy decisions        | 30s             |
| **Agent**   | Claude with tool access (up to 50 turns) | Complex verification, multi-step checks    | 60s             |

All timeouts are configurable per hook via the `timeout` field (in seconds).

## Complete Lifecycle Events

Every event in the Claude Code lifecycle has a corresponding hook point. Events fire at specific times during a session — some fire once, others fire repeatedly inside the agentic loop.

### Session Lifecycle Events

| Event                | Triggers When                                         | Matcher Target                                                                                       | Can Block? |
| -------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------- |
| `SessionStart`       | Session begins or resumes                             | Source: `startup`, `resume`, `clear`, `compact`                                                      | No         |
| `InstructionsLoaded` | CLAUDE.md or `.claude/rules/*.md` loaded into context | Load reason: `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`            | No         |
| `SessionEnd`         | Session terminates                                    | End reason: `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other` | No         |

### User Interaction Events

| Event              | Triggers When                                    | Matcher Target                                                                 | Can Block?                                           |
| ------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------ | ---------------------------------------------------- |
| `UserPromptSubmit` | User sends a prompt (before Claude processes it) | No matcher support                                                             | Yes — blocks prompt processing and erases the prompt |
| `Notification`     | Claude Code sends a notification                 | Type: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` | No                                                   |

### Tool Execution Events

| Event                | Triggers When             | Matcher Target                                                                | Can Block?                  |
| -------------------- | ------------------------- | ----------------------------------------------------------------------------- | --------------------------- |
| `PreToolUse`         | Before tool execution     | Tool name: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `mcp__*` | Yes — blocks the tool call  |
| `PermissionRequest`  | Permission dialog appears | Tool name                                                                     | Yes — denies the permission |
| `PostToolUse`        | After tool succeeds       | Tool name                                                                     | No (tool already ran)       |
| `PostToolUseFailure` | After tool fails          | Tool name                                                                     | No (tool already failed)    |

### Subagent and Team Events

| Event           | Triggers When                        | Matcher Target                                      | Can Block?                            |
| --------------- | ------------------------------------ | --------------------------------------------------- | ------------------------------------- |
| `SubagentStart` | Subagent spawned                     | Agent type: `Bash`, `Explore`, `Plan`, custom names | No                                    |
| `SubagentStop`  | Subagent finishes                    | Agent type (same as SubagentStart)                  | Yes — prevents subagent from stopping |
| `TeammateIdle`  | Agent team teammate about to go idle | No matcher support                                  | Yes — keeps teammate working          |
| `TaskCompleted` | Task marked as completed             | No matcher support                                  | Yes — prevents completion             |

### Completion Events

| Event         | Triggers When              | Matcher Target                                                                                                                        | Can Block?                                      |
| ------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `Stop`        | Claude finishes responding | No matcher support                                                                                                                    | Yes — prevents stopping, continues conversation |
| `StopFailure` | Turn ends due to API error | Error type: `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` | No (output/exit code ignored)                   |

### Context and Configuration Events

| Event          | Triggers When                             | Matcher Target                                                                             | Can Block?                     |
| -------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------ |
| `PreCompact`   | Before context compaction                 | Trigger: `manual`, `auto`                                                                  | No                             |
| `PostCompact`  | After compaction completes                | Trigger: `manual`, `auto`                                                                  | No                             |
| `ConfigChange` | Configuration file changes during session | Source: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` | Yes (except `policy_settings`) |

### Worktree Events

| Event            | Triggers When                                                | Matcher Target     | Can Block?                         |
| ---------------- | ------------------------------------------------------------ | ------------------ | ---------------------------------- |
| `WorktreeCreate` | Worktree created via `--worktree` or `isolation: "worktree"` | No matcher support | Yes — non-zero exit fails creation |
| `WorktreeRemove` | Worktree removed at session exit or subagent finish          | No matcher support | No                                 |

### MCP Elicitation Events

| Event               | Triggers When                                   | Matcher Target  | Can Block?                                     |
| ------------------- | ----------------------------------------------- | --------------- | ---------------------------------------------- |
| `Elicitation`       | MCP server requests user input during tool call | MCP server name | Yes — denies the elicitation                   |
| `ElicitationResult` | User responds to MCP elicitation                | MCP server name | Yes — blocks response (action becomes decline) |

## Configuration

Hooks are defined in JSON at multiple levels:

| Location                      | Scope                     | Shareable                 |
| ----------------------------- | ------------------------- | ------------------------- |
| `~/.claude/settings.json`     | All your projects         | No, local to machine      |
| `.claude/settings.json`       | Single project            | Yes, committable          |
| `.claude/settings.local.json` | Single project            | No, gitignored            |
| Managed policy settings       | Organization-wide         | Yes, admin-controlled     |
| Plugin `hooks/hooks.json`     | When plugin is enabled    | Yes, bundled with plugin  |
| Skill or agent frontmatter    | While component is active | Yes, defined in component |

Enterprise administrators can use `allowManagedHooksOnly` to block user, project, and plugin hooks.

### Structure

```
hooks → event name → matcher group array → hooks array → handler
```

### Handler Fields (Common)

| Field           | Required | Description                                                                |
| --------------- | -------- | -------------------------------------------------------------------------- |
| `type`          | Yes      | `"command"`, `"http"`, `"prompt"`, or `"agent"`                            |
| `timeout`       | No       | Seconds before canceling (defaults: 600 command, 30 prompt/http, 60 agent) |
| `statusMessage` | No       | Custom spinner message while hook runs                                     |
| `once`          | No       | If `true`, runs only once per session (skills only)                        |

## Exit Code Control

| Code  | Behavior                                                                                                          |
| ----- | ----------------------------------------------------------------------------------------------------------------- |
| `0`   | Proceed (allow). Stdout parsed for JSON output. For `UserPromptSubmit`/`SessionStart`, stdout is added as context |
| `2`   | Block with stderr feedback to Claude. JSON on stdout is ignored                                                   |
| Other | Proceed with stderr logging (visible in verbose mode via `Ctrl+O`)                                                |

For structured control, return JSON on exit 0: `{hookSpecificOutput: {hookEventName: "...", decision: {...}}}`

### Universal JSON Output Fields

| Field            | Default | Description                                                                       |
| ---------------- | ------- | --------------------------------------------------------------------------------- |
| `continue`       | `true`  | If `false`, Claude stops processing entirely (overrides event-specific decisions) |
| `stopReason`     | none    | Message shown to user when `continue` is `false`                                  |
| `suppressOutput` | `false` | If `true`, hides stdout from verbose mode                                         |
| `systemMessage`  | none    | Warning message shown to the user                                                 |

## Advanced Control Patterns

### `updatedInput` — Pre-Execution Validation

`PreToolUse` and `PermissionRequest` hooks can modify tool parameters before execution via the `updatedInput` field. Combine with `"allow"` to auto-approve with modifications, or `"ask"` to show modified input to the user:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": { "command": "npm run lint" },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

### `updatedPermissions` — Programmatic Permission Control

`PermissionRequest` hooks can modify session permissions when allowing an action. Use `setMode` to change the permission mode, or `addAllowRule`/`addDenyRule` to add persistent rules:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

### `additionalContext` — Context Injection

Multiple events support injecting text into Claude's context via the `additionalContext` field in JSON output: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Notification`, and `SubagentStart`. Multiple hooks' values are concatenated. For `SessionStart`, `CLAUDE_ENV_FILE` enables persisting environment variables for all subsequent Bash commands in the session.

## Async Hooks

Set `"async": true` on command hooks to run them in the background without blocking Claude. Async hooks:

- Receive the same JSON input on stdin as synchronous hooks
- **Cannot block or control behavior** — `decision`, `permissionDecision`, and `continue` fields have no effect since the action already completed
- If the hook produces `systemMessage` or `additionalContext`, the content is delivered on the next conversation turn
- Only `type: "command"` hooks support `async` — prompt/agent/http hooks cannot run asynchronously
- Each execution creates a separate background process with no deduplication
- Use the same default 10-minute timeout as sync hooks (configurable via `timeout`)

## Matchers

Matchers narrow hook scope using regex patterns against event-specific fields:

- `"Bash"` — Only Bash tool invocations
- `"Edit|Write"` — Edit OR Write tools
- `"mcp__.*"` — All MCP tools
- `"mcp__github__.*"` — All tools from the GitHub MCP server
- `"mcp__.*__write.*"` — Any write tool from any MCP server

Events without matcher support (`UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`) always fire on every occurrence. A `matcher` field on these events is silently ignored.

**Keep matchers narrow** to avoid unintended matches. Matching on `".*"` or leaving matcher empty for `PermissionRequest` would auto-approve every permission prompt.

## Security Patterns

### File Protection with Path Traversal Validation

Use `PreToolUse` hooks on `Edit|Write` to check target file paths against protected patterns. Exit 2 to block. Validate against path traversal by checking for `..` sequences and canonicalizing paths before comparison.

### Auto-Format After Writes

`PostToolUse` hooks on `Edit|Write` extract the edited file path from stdin JSON (via `jq -r '.tool_input.file_path'`) and pipe to Prettier, Black, or your formatter of choice.

### `stop_hook_active` — Infinite Loop Prevention

`Stop` and `SubagentStop` hooks receive a `stop_hook_active` boolean in their JSON input. When `true`, it means Claude Code is already continuing as a result of a prior stop hook. **Always check this field** and exit 0 early to prevent Claude from running indefinitely:

```bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0
fi
```

## Prompt-Based Hooks

`type: "prompt"` hooks send the hook input data plus your prompt to a Claude model (Haiku by default, configurable via `model`). The model returns a yes/no decision as JSON:

- `"ok": true` — the action proceeds
- `"ok": false` — the action is blocked; `reason` is fed back to Claude

Use for decisions requiring judgment rather than deterministic rules.

## Agent-Based Hooks

`type: "agent"` hooks spawn a subagent with tool access (Read, Grep, Glob, etc.) to verify conditions against the actual state of the codebase. Same `"ok"`/`"reason"` response format as prompt hooks, but supports up to 50 tool-use turns with a longer default timeout of 60 seconds. Use `$ARGUMENTS` as a placeholder for hook input JSON in the prompt.

## Common Patterns

- **Auto-format**: PostToolUse on `Edit|Write` → `jq -r '.tool_input.file_path' | xargs npx prettier --write`
- **File protection**: PreToolUse on `Edit|Write` → check against protected paths, exit 2 to block
- **Audit logging**: PostToolUse → `jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> audit.log`
- **Notification**: Notification event → `osascript` (macOS) or `notify-send` (Linux)
- **Permission auto-approval**: PermissionRequest with narrow matcher + JSON `behavior: "allow"` decision
- **Context re-injection**: SessionStart with `compact` matcher → echo critical context back after compaction
- **Config audit**: ConfigChange → log `{timestamp, source, file_path}` to compliance log
- **Completeness check**: Stop → prompt hook asking if all tasks are complete, blocks with `reason` if not
- **Test verification**: Stop → agent hook that runs test suite before allowing completion
- **MCP tool logging**: PreToolUse on `mcp__github__.*` → log GitHub API operations
- **Environment setup**: SessionStart → write `export` statements to `$CLAUDE_ENV_FILE` for persistent env vars

## HTTP Hooks

`type: "http"` hooks POST event JSON to an endpoint. Response handling differs from command hooks:

- **2xx with empty body** → success (equivalent to exit 0 with no output)
- **2xx with JSON body** → parsed using same JSON output schema as command hooks
- **Non-2xx / connection failure / timeout** → non-blocking error, execution continues

To block a tool call via HTTP, return a 2xx response with appropriate `hookSpecificOutput` fields. Status codes alone cannot block actions. Header values support env var interpolation via `$VAR_NAME` syntax, but only variables listed in `allowedEnvVars` are resolved.

## Hooks in Skills and Agents

Hooks can be defined directly in [[claude-code-skills]] and [[claude-code-subagents]] YAML frontmatter. These hooks are scoped to the component's lifecycle and cleaned up when it finishes. All hook events are supported. For subagents, `Stop` hooks are automatically converted to `SubagentStop`.

## Related pages

- [[claude-code-plugins]]
- [[claude-code-memory]]
- [[claude-code-subagents]]
- [[cursor-hooks]]
- [[agent-workflows]]
