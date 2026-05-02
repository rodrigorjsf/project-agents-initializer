# Cursor Hooks

**Summary**: Lifecycle automation points in Cursor that execute shell commands or LLM prompts at specific agent events — supporting four configuration levels (enterprise, team, project, user), regex matchers for conditional execution, and exit-code-based control flow.
**Sources**: hooks-guide.md, analysis-cursor-hooks-guide.md
**Last updated**: 2026-04-18

---

## How Hooks Work

Hooks are spawned as JSON stdio processes that observe, block, or modify agent behavior at lifecycle events. They provide **deterministic control** independent of the model's judgment.

## Hook Events

### Agent Events

| Event                                               | Triggers When            |
| --------------------------------------------------- | ------------------------ |
| `sessionStart` / `sessionEnd`                       | Session lifecycle        |
| `preToolUse` / `postToolUse` / `postToolUseFailure` | Tool execution lifecycle |
| `subagentStart` / `subagentStop`                    | Subagent lifecycle       |
| `beforeShellExecution` / `afterShellExecution`      | Shell commands           |
| `beforeMCPExecution` / `afterMCPExecution`          | MCP tool calls           |
| `beforeReadFile` / `afterFileEdit`                  | File operations          |
| `beforeSubmitPrompt`                                | Prompt submission        |
| `preCompact` / `stop`                               | Context management       |
| `afterAgentResponse` / `afterAgentThought`          | Agent output             |

### Tab Events

| Event               | Triggers When    |
| ------------------- | ---------------- |
| `beforeTabFileRead` | Tab reads a file |
| `afterTabFileEdit`  | Tab edits a file |

## Hook Types

| Type        | Mechanism                  | Use Case                            |
| ----------- | -------------------------- | ----------------------------------- |
| **Command** | Shell script               | Formatting, validation, audit       |
| **Prompt**  | Single-turn LLM evaluation | Policy decisions, conditional logic |

## Exit Codes

| Code  | Effect                           |
| ----- | -------------------------------- |
| `0`   | Allow (proceed)                  |
| `2`   | Deny (block with feedback)       |
| Other | Fail-open (proceed with logging) |

## Configuration

```json
// .cursor/hooks.json
{
  "hooks": {
    "afterFileEdit": [
      {
        "command": "prettier --write ${file}",
        "type": "command",
        "matcher": "\\.tsx?$",
        "timeout": 5000
      }
    ]
  }
}
```

### Config Levels

1. Enterprise (managed)
2. Team (dashboard)
3. Project: `.cursor/hooks.json`
4. User: `~/.cursor/hooks.json`

### Config Fields

| Field        | Description                     |
| ------------ | ------------------------------- |
| `command`    | Shell command to execute        |
| `type`       | `command` or `prompt`           |
| `timeout`    | Max execution time (ms)         |
| `failClosed` | Block on hook failure           |
| `matcher`    | Regex for conditional execution |
| `loop_limit` | Max re-executions               |

### Interpolation Variables

- `${env:NAME}` — Environment variable
- `${userHome}` — Home directory
- `${workspaceFolder}` — Project root
- `${pathSeparator}` — OS path separator

## Partner Integrations

Security-focused hook providers: MintMCP, Oasis Security, Semgrep, Endor Labs, Snyk, 1Password

## Related pages

- [[claude-code-hooks]]
- [[cursor-plugins]]
- [[cursor-rules]]
- [[agent-workflows]]
