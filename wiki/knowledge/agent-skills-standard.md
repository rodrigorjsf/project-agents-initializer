# Agent Skills Standard

**Summary**: The open specification for extending AI agents with portable, version-controlled skill packages — defining SKILL.md structure, YAML frontmatter requirements, progressive disclosure loading, bundled file conventions, and the directory format adopted by Claude Code, Cursor, Codex, and other compliant agents.
**Sources**: agentskills-specification.md, agentskills-what-are-skills.md, skills-standard/README.md, analysis-agent-skills-standard.md
**Last updated**: 2026-04-18

---

## What Is a Skill?

A lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows. Skills are:

- **Portable** — Just files; easy to edit, version, share
- **Self-documenting** — Human-readable SKILL.md
- **Extensible** — From text instructions to executable code

Canonical reference: [agentskills.io](https://agentskills.io)

## Directory Structure

```
skill-name/
├── SKILL.md           (required — metadata + instructions)
├── scripts/           (optional — executable code)
├── references/        (optional — documentation)
└── assets/            (optional — templates, resources)
```

## YAML Frontmatter

| Field           | Required | Constraints                                                         |
| --------------- | -------- | ------------------------------------------------------------------- |
| `name`          | Yes      | 1–64 chars, lowercase + hyphens, no `--`, must match directory name |
| `description`   | Yes      | 1–1024 chars, what + when                                           |
| `license`       | No       | Short identifier or filename                                        |
| `compatibility` | No       | 1–500 chars, environment requirements                               |
| `metadata`      | No       | Key-value mapping (string → string)                                 |
| `allowed-tools` | No       | Space-delimited pre-approved tools                                  |

### Name Validation Rules

- Unicode lowercase alphanumeric (a–z) + hyphens only
- Must NOT start or end with hyphen
- Must NOT contain consecutive hyphens (`--`)
- Must match parent directory name

### Description Best Practices

- Describe both WHAT the skill does and WHEN to use it
- Include keywords for agent discovery
- Good: "Extracts text and tables from PDF files, fills forms, merges PDFs. Use when working with PDFs."
- Bad: "Helps with PDFs."

## Progressive Disclosure

| Phase          | Loaded When                | Budget                                     |
| -------------- | -------------------------- | ------------------------------------------ |
| **Discovery**  | Session start              | ~100 tokens (name + description only)      |
| **Activation** | Task matches description   | <5,000 tokens (full SKILL.md)              |
| **Execution**  | Explicitly loaded by skill | On-demand (references/, scripts/, assets/) |

This three-phase loading keeps context efficient — only metadata loads at startup.

## Bundled File References

Use relative paths from skill root:

- `references/api-errors.md`
- `scripts/extract.py`
- `assets/templates/output.md`

One level deep from SKILL.md; avoid deeply nested chains.

## Validation

Use `skills-ref validate ./my-skill` to check frontmatter validity and naming conventions.

## Platform Adoption

| Platform      | Skill Discovery Dirs                       |
| ------------- | ------------------------------------------ |
| Claude Code   | `.claude/skills/`, plugin `skills/`        |
| Cursor        | `.agents/skills/`, `.cursor/skills/`       |
| Codex         | `.codex/skills/`                           |
| Compatibility | Cross-discovers from other platforms' dirs |

## Related pages

- [[skill-authoring]]
- [[claude-code-skills]]
- [[cursor-skills]]
- [[progressive-disclosure]]
