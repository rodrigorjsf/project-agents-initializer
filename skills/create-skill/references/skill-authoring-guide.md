# Skill Authoring Guide

Evidence-based guidance for creating effective Claude Code skills (SKILL.md files).
Source: skills/skill-authoring-best-practices.md, skills/extend-claude-with-skills.md

---

## Contents

- Core principles (conciseness, degrees of freedom, multi-model testing)
- Skill structure (frontmatter fields, naming, descriptions)
- Progressive disclosure patterns (references, assets, on-demand loading)
- Anti-patterns (what to avoid in skill authoring)
- Invocation control (disable-model-invocation, user-invocable)

---

## Core Principles

**Conciseness is the primary principle.** The context window is a shared resource. At startup, only `name` + `description` are loaded for all skills. SKILL.md loads when triggered; supporting files load only on demand.

Challenge each piece of content:

- "Does Claude really need this explanation?"
- "Can I assume Claude knows this already?"
- "Does this paragraph justify its token cost?"

> "Claude is already very smart — only add context it doesn't have."
> — skill-authoring-best-practices.md

**Degrees of freedom** — match specificity to task fragility:

| Degree | Use When | Format |
|--------|----------|--------|
| High | Multiple valid approaches; decisions depend on context | Text instructions |
| Medium | A preferred pattern exists; variation acceptable | Pseudocode or parameterized scripts |
| Low | Operations are fragile; consistency critical | Exact scripts, no parameters |

Analogy: Claude as a robot on a path — narrow bridge (low freedom) vs. open field (high freedom).

**Test with all models you plan to use:**

| Model | Testing Consideration |
|-------|----------------------|
| Haiku | Provide enough guidance? (may need more detail) |
| Sonnet | Clear and efficient? (balanced) |
| Opus | Avoid over-explaining? (may need less) |

*Source: skills/skill-authoring-best-practices.md lines 11-145*

---

## Skill Structure and Frontmatter

Every skill is a directory with `SKILL.md` as the entry point:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── references/        # Reference docs loaded on demand
├── assets/templates/  # Output templates
└── scripts/           # Scripts Claude can execute
```

**Frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Recommended | Lowercase, numbers, hyphens; max 64 chars; no "anthropic" or "claude" |
| `description` | Recommended | What it does + when to use it; max 1024 chars; third person |
| `disable-model-invocation` | No | `true` = user-only invocation; description not in context |
| `user-invocable` | No | `false` = Claude-only; hidden from `/` menu |
| `allowed-tools` | No | Tools Claude can use without prompting during skill |
| `model` | No | Override model for this skill |
| `effort` | No | `low`/`medium`/`high`/`max`; overrides session effort |
| `context` | No | `fork` = run in isolated subagent context |
| `agent` | No | Subagent type when `context: fork` is set |
| `hooks` | No | Hooks scoped to this skill's lifecycle |
| `argument-hint` | No | Autocomplete hint, e.g. `[issue-number]` |

*Source: skills/extend-claude-with-skills.md lines 169-199*

---

## Naming and Descriptions

**Naming** — prefer gerund form (`processing-pdfs`, `analyzing-data`). Avoid: `helper`, `utils`, `tools`, `data`, `files`.

**Descriptions** — always write in third person (injected into system prompt):

- Good: "Processes Excel files and generates reports"
- Bad: "I can help you process Excel files"
- Bad: "You can use this to process Excel files"

Include: (1) what it does, (2) when to use it, (3) specific trigger terms for matching.

*Source: skills/skill-authoring-best-practices.md lines 168-250*

---

## Progressive Disclosure Patterns

SKILL.md is the index; detailed content lives in supporting files loaded on demand.

**Pattern 1 — High-level guide with references:**

```markdown
## Phase 1: Analyze
Read ${CLAUDE_SKILL_DIR}/references/reference.md for detailed context.
```

**Pattern 2 — Phased loading:**
Load only the references needed for each phase, not all at once.

Keep SKILL.md under 500 lines. Move detailed reference material to separate files. Reference supporting files explicitly so Claude knows what they contain.

*Source: skills/skill-authoring-best-practices.md lines 251-300; skills/extend-claude-with-skills.md lines 223-246*

---

## Invocation Control

| Frontmatter | User can invoke | Claude can invoke | Description in context |
|-------------|----------------|-------------------|----------------------|
| (default) | Yes | Yes | Always loaded |
| `disable-model-invocation: true` | Yes | No | Not loaded (manual only) |
| `user-invocable: false` | No | Yes | Always loaded |

Use `disable-model-invocation: true` for workflows with side effects (commit, deploy, send-message). Use `user-invocable: false` for background knowledge Claude should apply but users shouldn't invoke directly.

*Source: skills/extend-claude-with-skills.md lines 248-283*

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Explaining what Claude already knows | Wastes tokens; dilutes attention | Delete it |
| Generic descriptions ("helps with data") | Poor skill discovery | Be specific about what + when |
| Inlining all reference content in SKILL.md | Context bloat on every invocation | Move to `references/` subdirectory |
| Hardcoded file paths | Goes stale | Use `${CLAUDE_SKILL_DIR}` for bundled files |
| Over-explaining for Opus | Patronizing + token waste | Trust the model; provide minimal scaffolding |
| Contradictions between phases | Claude picks one arbitrarily | Review all phases for consistency |

*Source: skills/skill-authoring-best-practices.md lines 800-1100*
