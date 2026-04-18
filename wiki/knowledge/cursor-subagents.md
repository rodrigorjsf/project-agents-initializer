# Cursor Subagents

**Summary**: Specialized task-delegation assistants in Cursor that run in isolated context windows — supporting foreground/background execution, model selection via `inherit`/`fast`/specific ID, read-only mode, and automatic or explicit invocation without parent conversation history.
**Sources**: subagents-guide.md, analysis-cursor-subagents-guide.md
**Last updated**: 2026-04-18

---

## Execution Modes

| Mode           | Behavior                                 | Use Case                      |
| -------------- | ---------------------------------------- | ----------------------------- |
| **Foreground** | Blocks until completion                  | Standard task delegation      |
| **Background** | Returns immediately, works independently | Long research, parallel tasks |

## Built-in Subagents

| Name        | Purpose                        | Model                   |
| ----------- | ------------------------------ | ----------------------- |
| **Explore** | Codebase search/analysis       | Faster model            |
| **Bash**    | Shell command execution        | Isolates verbose output |
| **Browser** | Web automation, visual testing | Filters DOM snapshots   |

## Custom Subagent Definition

```yaml
---
name: security-auditor
description: "Audit code for security vulnerabilities in auth, payments, and sensitive data"
model: inherit
readonly: true
---
You are a security auditor. Focus on:
- Authentication and authorization flaws
- Input validation gaps
- Data exposure risks
Report only high-confidence findings.
```

### Frontmatter Fields

| Field           | Required | Default   | Description                             |
| --------------- | -------- | --------- | --------------------------------------- |
| `name`          | Yes      | —         | Identifier                              |
| `description`   | Yes      | —         | When to invoke                          |
| `model`         | No       | `inherit` | `inherit`, `fast`, or specific model ID |
| `readonly`      | No       | `false`   | Restricts write permissions             |
| `is_background` | No       | `false`   | Background execution                    |

> **Cursor agents must not have** `tools` or `maxTurns` fields (those are Claude Code specific).

## File Locations

| Location                            | Scope         |
| ----------------------------------- | ------------- |
| `.cursor/agents/`                   | Project       |
| `~/.cursor/agents/`                 | User          |
| `.claude/agents/`, `.codex/agents/` | Compatibility |

## Invocation

- **Automatic**: Based on task complexity and description matching
- **Explicit**: `/name` syntax or natural language mention
- **Parallel**: Multiple Task tool calls in one message
- **Resumption**: Pass agent ID to continue previous conversations

## Nested Launch Support

Cursor subagents **support nested launches** (spawning other subagents), unlike Claude Code. However, this project's agents are restricted from nesting to maintain simplicity.

## Common Patterns

- **Verifier**: Validates completed work, runs tests (model: fast)
- **Debugger**: Root cause analysis, stack trace capture
- **Search agent**: Semantic search with fast model for parallel execution
- **Orchestrator**: Planner → Implementer → Verifier with structured handoffs

## Related pages

- [[subagents]]
- [[claude-code-subagents]]
- [[cursor-skills]]
- [[agent-workflows]]
