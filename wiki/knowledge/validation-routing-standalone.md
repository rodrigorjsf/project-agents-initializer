# Validation Routing — Standalone Skills

**Summary**: Routing guide for validators checking standalone skills (`skills/` — the `npx skills add` portable distribution). Lists primary sources, forbidden sources, convention entry points, and direct read paths.
**Sources**: docs/compliance/normative-source-matrix.md
**Last updated**: 2026-05-02

---

> **Derived view** — Derived from `standalone-bundle` in the normative source matrix (`docs/compliance/normative-source-matrix.md:283-290`). See [[compliance-routing]] for the full routing table.

---

## Scope Identifier

**Named bundle**: `standalone-bundle`
**Distribution**: `skills/`

---

## Source Authority

### Primary Sources (Tier 2 — Shared Standards)

| Source ID | Canonical Path | What it governs |
|-----------|----------------|-----------------|
| `SHARED-SKILLS-STD` | `docs/shared/skills-standard/` | Agent Skills open standard: SKILL.md format, frontmatter, loading |
| `SHARED-AUTHORING` | `docs/shared/skill-authoring-best-practices.md` | Universal skill writing, eval-driven iteration, description optimization |

### Secondary Sources (Tier 3 — Project)

| Source ID | Canonical Path |
|-----------|----------------|
| `PROJECT-DESIGN-GUIDELINES` | `DESIGN-GUIDELINES.md` |
| `GENERAL-AGENTS-GUIDE` | `docs/general-llm/a-guide-to-agents.md` |

### Project Rules & Instructions

- `.claude/rules/standalone-skills.md` — inline bash analysis requirement; no agent delegation
- `.claude/rules/reference-files.md` — reference file line limits and structure
- `.github/instructions/skill-files.instructions.md` — SKILL.md review criteria (standalone section)

---

## Forbidden Sources

The following must NEVER be used as normative authority for standalone skill artifacts:

- `docs/claude-code/**` — all Claude Code-specific documentation
- `docs/claude-code/skills/` — Claude `${CLAUDE_SKILL_DIR}` substitution (not available in standalone)
- `docs/claude-code/hooks/` — Claude hook exit codes and JSON stdio
- `docs/claude-code/subagents/` — Claude agent delegation patterns
- `docs/cursor/**` — all Cursor IDE-specific documentation
- `docs/cursor/rules/` — Cursor `.mdc` format and `globs:` frontmatter
- Any `CLAUDE-*` source ID
- Any `CURSOR-*` source ID
- Hook-specific or subagent-specific guidance of any platform

**Key contamination signals to watch for:**
- `${CLAUDE_SKILL_DIR}` in skill content (Claude-only substitution — not available in standalone runtime)
- References to named agents or the Task tool for analysis phases (standalone must use inline bash)
- `paths:` in any generated rule file (Claude-specific; standalone generates portable artifacts)
- `globs:` in standalone-generated content (Cursor-specific)
- `model: sonnet` or `model: inherit` references in skill body (platform-specific)
- Phase instructions that say "delegate to" an agent instead of providing explicit bash commands

---

## Critical Standalone Constraint

> **ALL analysis must be inline** — explicit bash commands for each step.
> Standalone skills MUST NEVER reference agent names, use Task tool delegation, or spawn subagents.
> This is the most common contamination pattern from Claude Code plugin skill patterns.

```
WRONG (Claude plugin pattern):
  - Delegate to `codebase-analyzer` agent

CORRECT (standalone pattern):
  - Run: find . -name "SKILL.md" | head -20
  - Run: grep -r "name:" skills/*/SKILL.md
```

---

## Convention Entry Points

Start validation from these files:

| Artifact Type | Entry Point | Key Rules |
|---------------|-------------|-----------|
| `SKILL.md` | `skills/*/SKILL.md` | ALL analysis inline; no agent delegation; explicit bash per step |
| Reference files | `skills/*/references/*.md` | ≤200 lines; same content structure as plugin references |
| Templates | `skills/*/assets/templates/**/*.md` | Same metadata conventions as plugin templates; no hook/subagent content |
| Standalone `README.md` | `skills/README.md` | Must NOT reference `init-cursor` or `improve-cursor` (plugin-only skills) |

---

## Direct Read Paths

Read these in order when validating a standalone skill artifact:

1. Wiki concept pages (compact, curated): `[[agent-skills-standard]]`, `[[skill-authoring]]`, `[[progressive-disclosure]]`.
2. Source documents (raw): `docs/shared/skills-standard/`, `docs/shared/skill-authoring-best-practices.md`, `docs/general-llm/a-guide-to-agents.md`.
3. Concrete examples in this repo: `skills/*/SKILL.md`.

---

## Common Validation Mistakes

- Loading `docs/claude-code/skills/` to check SKILL.md format — standalone uses the Agent Skills open standard, not Claude-specific format
- Accepting "delegate to codebase-analyzer" as valid for standalone (it is valid ONLY in Claude plugin skills)
- Using Claude hook or subagent docs as supporting authority for standalone artifacts
- Checking that `.claude/rules/` are referenced by standalone skills — they should NOT be; standalone generates portable artifacts
