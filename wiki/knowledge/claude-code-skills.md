# Claude Code Skills

**Summary**: Custom instruction packages that extend Claude Code's capabilities through SKILL.md files with YAML frontmatter — following the Agent Skills open standard with Claude-specific extensions for model selection, tool restriction, and context forking.
**Sources**: extend-claude-with-skills.md, research-claude-code-skills-format.md, analysis-extend-claude-with-skills.md, analysis-research-claude-code-skills-format.md
**Last updated**: 2026-04-18

---

## Skill Format

Every skill is a directory containing at minimum a `SKILL.md` file:

```
my-skill/
├── SKILL.md           (required — YAML frontmatter + instructions)
├── references/        (optional — detailed reference material)
├── assets/            (optional — templates, examples, data)
└── scripts/           (optional — executable helpers)
```

### YAML Frontmatter

| Field                      | Required | Description                                |
| -------------------------- | -------- | ------------------------------------------ |
| `name`                     | Yes      | 1–64 chars, lowercase, hyphens only        |
| `description`              | Yes      | Max 1024 chars, third person, what + when  |
| `disable-model-invocation` | No       | `true` = manual only (for destructive ops) |
| `user-invocable`           | No       | `false` = background knowledge only        |
| `allowed-tools`            | No       | Restrict available tools                   |
| `model`                    | No       | sonnet, opus, haiku, full ID               |
| `effort`                   | No       | low, medium, high, max (Opus 4.6 only)     |
| `context`                  | No       | `fork` = isolated subagent execution       |
| `agent`                    | No       | Explore, Plan, general-purpose             |
| `argument-hint`            | No       | Placeholder text for arguments             |
| `hooks`                    | No       | Lifecycle hook definitions                 |

### String Substitutions

- `$ARGUMENTS` / `$ARGUMENTS[N]` / `$N` — User-provided arguments
- `${CLAUDE_SESSION_ID}` — Current session identifier
- `${CLAUDE_SKILL_DIR}` — Skill directory path
- `` !`<command>` `` — Dynamic context (runs shell command before sending to Claude)

## Skill Locations

1. **Plugin skills** — `<plugin>/skills/` (namespaced: `plugin-name:skill-name`)
2. **Project skills** — `.claude/skills/`
3. **Personal skills** — `~/.claude/skills/`

## Progressive Disclosure

| Tier                             | Loaded When       | Budget        |
| -------------------------------- | ----------------- | ------------- |
| Metadata (name, description)     | Session start     | ~100 tokens   |
| Instructions (SKILL.md body)     | Skill activated   | <5,000 tokens |
| Resources (references/, assets/) | Explicitly loaded | On-demand     |

## Bundled Skills

Claude Code ships with: `/batch`, `/claude-api`, `/debug`, `/loop`, `/simplify`

## Invocation

- **Manual**: Type `/skill-name` in chat
- **Auto**: Claude decides based on description match
- **Plugin**: `/plugin-name:skill-name [arguments]`

## Key Practices

- Keep SKILL.md under **500 lines** (~5,000 tokens)
- Use `disable-model-invocation: true` for side-effect tasks (deploy, commit)
- Move large API docs to `references/` files, referenced from SKILL.md
- Test skills both ways: auto-invocation and manual with `/`
- Don't use skills for settings — use CLAUDE.md instead

## Related pages

- [[agent-skills-standard]]
- [[skill-authoring]]
- [[claude-code-plugins]]
- [[cursor-skills]]
- [[progressive-disclosure]]
