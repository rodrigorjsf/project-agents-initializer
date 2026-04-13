---
name: create-skill
description: "Creates new SKILL.md files with references, templates, and frontmatter grounded in the docs corpus. Uses subagent-driven codebase analysis and evidence-based guidance. Use when creating a new Claude Code skill from scratch."
---

# Create Skill

Generates a new SKILL.md file with supporting references and templates, grounded in the docs corpus and project conventions.

## Hard Rules

<RULES>
- **NEVER** create skills that explain what Claude already knows (language syntax, obvious conventions)
- **NEVER** inline reference content in SKILL.md body — use the `references/` subdirectory
- **NEVER** exceed 500 lines in the SKILL.md body
- **EVERY** reference file must be ≤ 200 lines with source attribution
- **EVERY** skill must use `${CLAUDE_SKILL_DIR}` for all bundled file references (not hardcoded paths)
- **EVERY** skill description must be third-person and include a "Use when..." trigger phrase
</RULES>

## Process

### Preflight Check

Check if a skill with the same name already exists at:

- `.claude/skills/{requested-name}/SKILL.md`
- `plugins/*/skills/{requested-name}/SKILL.md`

**If a skill already exists at either location:**

1. Inform the user: "A skill named `{name}` already exists."
2. Inform the user that `improve-skill` is currently a Phase 5 placeholder and not yet executable.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this create skill. Ask the user to choose a different name or wait for the improve workflow implementation.

**If no skill exists with that name:**
Proceed to Phase 1 below.

### Phase 1: Codebase Analysis

Delegate to the `artifact-analyzer` agent with this task:

> Analyze the project to understand existing skills, naming conventions, and integration patterns. Focus on: existing skill directory structure, naming patterns, which skills delegate to agents, plugin conventions in CLAUDE.md files, and any skill that is similar to `{requested-name}` in purpose.

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context. Wait for it to complete and parse its structured output.

### Phase 2: Generate Skill

Before generating, read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/skill-authoring-guide.md` — core principles, structure rules, progressive disclosure, anti-patterns
- `${CLAUDE_SKILL_DIR}/references/skill-format-reference.md` — frontmatter fields, name validation, string substitution variables
- `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — per-artifact prompting strategies for skills

Read `${CLAUDE_SKILL_DIR}/assets/templates/skill-md.md` and fill its placeholders using:

- User requirements for the new skill
- Phase 1 analysis output (naming conventions, existing patterns, plugin context)
- Evidence from the reference files above

Generate the complete skill directory structure:

1. `SKILL.md` — primary skill file with frontmatter and phase definitions
2. `references/` — create only reference files that include initial source attribution sections (no empty stubs without attribution)
3. `assets/templates/` — create stub template files if the skill generates output files

### Phase 3: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/skill-validation-criteria.md` and execute its **Validation Loop Instructions** against the generated skill.

The loop evaluates all hard limits and quality checks, fixes any failures, and re-evaluates — maximum 3 iterations. Do not proceed to Phase 4 until ALL criteria pass.

### Phase 4: Present and Write

1. Show the user the complete generated skill directory (SKILL.md + any stub references/templates)
2. Cite the evidence from reference files that informed key decisions (frontmatter choices, phase structure, reference selections)
3. Ask for confirmation before writing any files
4. On approval, write all files to the target location
