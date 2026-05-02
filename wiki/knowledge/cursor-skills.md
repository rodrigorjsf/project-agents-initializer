# Cursor Skills

**Summary**: Portable, specialized capability packages following the Agent Skills open standard that extend Cursor's agent with domain-specific knowledge and workflows — discovered automatically at startup and invoked manually or by the agent based on description matching.
**Sources**: agent-skills-guide.md, agent-best-practices.md, analysis-cursor-skills-guide.md
**Last updated**: 2026-04-18

---

## Skill Locations

Cursor discovers skills from multiple directories:

| Location            | Scope         |
| ------------------- | ------------- |
| `.agents/skills/`   | Project       |
| `.cursor/skills/`   | Project       |
| `~/.cursor/skills/` | User          |
| `.claude/skills/`   | Compatibility |
| `.codex/skills/`    | Compatibility |

## Format

Each skill is a directory with `SKILL.md` at root:

```yaml
---
name: deploy-app
description: "Deploy applications to staging or production. Use when deploying or releasing code."
disable-model-invocation: true
---
```

### Frontmatter Fields

| Field                      | Required | Description                        |
| -------------------------- | -------- | ---------------------------------- |
| `name`                     | Yes      | kebab-case identifier (1–64 chars) |
| `description`              | Yes      | What + when (max 1024 chars)       |
| `license`                  | No       | License identifier                 |
| `compatibility`            | No       | Environment requirements           |
| `metadata`                 | No       | Key-value extensions               |
| `disable-model-invocation` | No       | Manual-only when `true`            |

### Optional Directories

- `scripts/` — Executable code (Bash, Python, JavaScript)
- `references/` — Detailed documentation loaded on demand
- `assets/` — Templates, images, data files

## Invocation

- **Automatic**: Agent decides based on task matching description
- **Manual**: Type `/` in Agent chat, search skill name
- **Remote**: Install from GitHub repositories

## Cursor vs Claude Code Skills

| Feature         | Cursor                               | Claude Code                                      |
| --------------- | ------------------------------------ | ------------------------------------------------ |
| Discovery dirs  | `.agents/skills/`, `.cursor/skills/` | `.claude/skills/`                                |
| Frontmatter     | Agent Skills standard only           | Standard + `model`, `effort`, `context`, `agent` |
| File references | Relative paths from skill root       | `${CLAUDE_SKILL_DIR}` or relative paths          |
| Namespacing     | Plugin name prefix                   | Plugin name prefix                               |
| Disabling auto  | `disable-model-invocation`           | `disable-model-invocation`                       |

## Related pages

- [[agent-skills-standard]]
- [[skill-authoring]]
- [[claude-code-skills]]
- [[cursor-rules]]
- [[cursor-plugins]]
