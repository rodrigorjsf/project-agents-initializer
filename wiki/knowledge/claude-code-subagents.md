# Claude Code Subagents

**Summary**: Task-specific assistants defined as Markdown files with YAML frontmatter that run in isolated context windows within Claude Code sessions — supporting tool restriction, model selection, permission modes, persistent memory, and worktree isolation.
**Sources**: creating-custom-subagents.md, claude-orchestrate-of-claude-code-sessions.md, analysis-creating-custom-subagents.md, research-subagent-best-practices.md
**Last updated**: 2026-04-18

---

## Definition Format

```yaml
---
name: code-reviewer
description: Reviews code for bugs, security issues, and style
tools: Read, Grep, Glob
model: haiku
maxTurns: 15
---
You are a senior code reviewer. Focus on correctness, security, and maintainability.
Report only issues with >80% confidence.
```

## Frontmatter Fields

| Field             | Required | Default | Description                                   |
| ----------------- | -------- | ------- | --------------------------------------------- |
| `name`            | Yes      | —       | Identifier                                    |
| `description`     | Yes      | —       | When to invoke                                |
| `tools`           | No       | All     | Comma-separated allowlist                     |
| `disallowedTools` | No       | None    | Denylist                                      |
| `model`           | No       | inherit | sonnet, opus, haiku, full ID                  |
| `maxTurns`        | No       | —       | Cost control (15 exploration, 20 evaluation)  |
| `permissionMode`  | No       | default | acceptEdits, dontAsk, bypassPermissions, plan |
| `memory`          | No       | —       | user, project, local (cross-session learning) |
| `isolation`       | No       | —       | `worktree` for git worktree isolation         |
| `background`      | No       | false   | Run asynchronously                            |
| `effort`          | No       | —       | low, medium, high, max                        |
| `skills`          | No       | —       | Available skills for the subagent             |
| `mcpServers`      | No       | —       | Scoped MCP server access                      |
| `hooks`           | No       | —       | Subagent-specific hooks                       |

## Locations (Priority Order)

1. **CLI flag**: `--agents` with JSON definition
2. **Project**: `.claude/agents/`
3. **User**: `~/.claude/agents/`
4. **Plugin**: `agents/` directory

## Built-in Subagents

| Name            | Model | Tools            | Purpose                     |
| --------------- | ----- | ---------------- | --------------------------- |
| Explore         | Haiku | Read, Grep, Glob | Fast, cheap codebase search |
| Plan            | —     | Read-only        | Research and planning       |
| general-purpose | —     | All              | Full capability             |
| Bash            | —     | Terminal         | Shell execution             |

## Effort Levels

The `effort` frontmatter field controls how hard the model works:

| Level    | Behavior                | Availability  |
| -------- | ----------------------- | ------------- |
| `low`    | Quick, shallow analysis | All models    |
| `medium` | Standard depth          | All models    |
| `high`   | Thorough analysis       | All models    |
| `max`    | Deepest reasoning       | Opus 4.6 only |

## Session-Scoped Hooks for Subagents

[[claude-code-hooks]] can be defined directly in subagent YAML frontmatter, scoped to the subagent's lifecycle:

```yaml
---
name: secure-writer
tools: Edit, Write
hooks:
  PreToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "validate-paths.sh"
  Stop:
    - hooks:
        - type: command
          command: "run-tests.sh"
---
```

All hook events are supported. Key behaviors:

- `Stop` hooks defined in subagent frontmatter are **automatically converted** to `SubagentStop` events
- Hooks are cleaned up when the subagent finishes
- Project-level hooks for `SubagentStart`/`SubagentStop` also fire for custom subagents

## Agent Teams (Experimental)

Multiple Claude Code instances coordinating as a team. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Requires Claude Code v2.1.32+.

### Architecture

| Component     | Role                                                                            |
| ------------- | ------------------------------------------------------------------------------- |
| **Team lead** | Creates team, breaks work into tasks, coordinates progress, synthesizes results |
| **Teammates** | Independent Claude Code instances, each with own context window                 |
| **Task list** | Shared state — teammates claim tasks, mark complete                             |
| **Mailbox**   | Direct messaging between lead and teammates, or between teammates               |

### Task Workflow

Tasks flow through states: **pending** → **in progress** → **completed**. Task dependencies are supported — a task won't become available until its dependencies are complete. File locking prevents race conditions when teammates access shared resources.

### Communication

- **Lead ↔ Teammate**: Direct messages via task list updates and mailbox
- **Teammate ↔ Teammate**: Broadcast messages for coordination
- Display modes: **in-process** (cycle with `Shift+Down`) or **split-panes** (tmux/iTerm2)

### Team-Specific Hooks

Two hook events exist specifically for agent teams:

- `TeammateIdle` — fires when a teammate is about to go idle; block to keep it working
- `TaskCompleted` — fires when a task is marked complete; block to prevent completion

### Sizing Guidelines

| Guideline          | Recommendation                                                                  |
| ------------------ | ------------------------------------------------------------------------------- |
| Team size          | **3–5 teammates** for most workflows                                            |
| Tasks per teammate | **5–6 tasks** each keeps everyone productive                                    |
| Scaling rule       | Add teammates only when work genuinely benefits from parallelism                |
| Task granularity   | Self-contained units producing clear deliverables (function, test file, review) |

Three focused teammates often outperform five scattered ones. Token costs scale linearly with teammate count, and coordination overhead increases with team size.

### Team Use Cases

- Parallel research from different angles
- Cross-layer coordination (frontend, backend, tests simultaneously)
- Model comparison on same task
- Large PR reviews split by concern area

### Team Anti-Patterns

- Sequential, tightly-coupled tasks (use single session)
- Same-file edits across teammates (causes overwrites)
- Simple tasks that don't justify coordination overhead (higher token cost)
- Running unattended too long (increases risk of wasted effort)

### Current Limitations

- No session resumption with in-process teammates (`/resume` and `/rewind` don't restore them)
- Task status can lag — teammates sometimes fail to mark tasks complete
- One team per session; no nested teams
- Lead is fixed for the session lifetime
- All teammates start with the lead's permission mode
- Split panes require tmux or iTerm2 (not supported in VS Code terminal, Windows Terminal, or Ghostty)

## Key Constraint

**Subagents cannot spawn other subagents** — this prevents infinite nesting. Use the `Agent(worker, researcher)` tool syntax to restrict which named subagents can be spawned from the parent context.

**Plugin security**: Agents bundled in [[claude-code-plugins]] cannot use `hooks`, `mcpServers`, or `permissionMode` frontmatter fields — these are silently ignored when loading from a plugin context. To use these fields, copy the agent file to `.claude/agents/` or `~/.claude/agents/`.

## Related pages

- [[subagents]]
- [[claude-code-skills]]
- [[claude-code-plugins]]
- [[claude-code-hooks]]
- [[agent-workflows]]
- [[cursor-subagents]]
