---
name: init-cursor
description: "Initializes optimized Cursor rules hierarchy and AGENTS.md for projects. Uses subagent-driven codebase analysis to generate minimal, scoped .cursor/rules/*.mdc files following progressive disclosure — based on the ETH Zurich 'Evaluating AGENTS.md' study and Cursor's context engineering best practices."
---

# Initialize Cursor Rules

Generate an evidence-based configuration hierarchy for this project, leveraging Cursor's full rule system: AGENTS.md files, `.cursor/rules/*.mdc` with metadata-controlled activation, and progressive disclosure pointers.

## Why This Approach

Research shows that auto-generated comprehensive configuration files **reduce** agent task success by ~3% while **increasing cost by 20%+** (Evaluating AGENTS.md, ETH Zurich, 2026). Developer-written **minimal** files improve success by ~4%. This skill generates files that mimic what an experienced developer would write: only non-obvious tooling and conventions.

Cursor's configuration hierarchy enables powerful progressive disclosure:

- **Root AGENTS.md** — always loaded, project-wide essentials
- **Subdirectory AGENTS.md** — loaded on-demand when working in that area
- **`.cursor/rules/*.mdc`** — metadata-controlled activation (always, auto-attached by globs, agent-requested by description, or manual @-mention)
- **Domain files** — referenced via progressive disclosure pointers

## Hard Rules

<RULES>
- **NEVER** generate a single file with everything — use hierarchical progressive disclosure
- **NEVER** include directory/file structure listings (research proves these don't help agents navigate)
- **NEVER** include obvious language conventions the model already knows
- **NEVER** exceed 200 lines per file
- **EVERY** instruction must pass: "Would removing this cause the agent to make mistakes?" If no, cut it.
- Root AGENTS.md target: **15-40 lines**
- Scope AGENTS.md target: **10-30 lines**
- `.cursor/rules/` files: **focused, metadata-scoped, one topic per file**
- `.mdc` frontmatter: ONLY `description`, `alwaysApply`, `globs` — no other fields
- Domain files: only when non-standard patterns are detected
</RULES>

## Process

### Preflight Check

Check if `.cursor/rules/` directory exists AND contains any `.mdc` or `.md` files.

**If rules already exist:**

1. Inform the user: "Cursor rules already exist in this project. Switching to the improve workflow to optimize your existing configuration."
2. Invoke the `improve-cursor` skill and follow its complete process.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this init skill.

**If no rules exist:**
Proceed to Phase 1 below.

### Phase 1: Codebase Analysis

Delegate to the `codebase-analyzer` agent with this task:

> Analyze the project at the current working directory. Return ONLY non-standard, non-obvious information that would cause the agent to make mistakes if it didn't know them. Be ruthlessly minimal.

The agent runs in an isolated context with read-only access. Wait for it to complete and parse its structured output.

### Phase 2: Scope Detection

Delegate to the `scope-detector` agent with this task:

> Detect scopes in the project at the current working directory. Only flag scopes with genuinely different tooling or conventions. A simple single-package project should have ZERO additional scopes. Also identify areas that would benefit from auto-attached `.cursor/rules/*.mdc` files with globs patterns.

Wait for it to complete and parse its structured output.

### Phase 3: Generate Files

Before generating, read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines
- `${CLAUDE_SKILL_DIR}/references/cursor-rules-system.md` — .cursor/rules/ conventions, .mdc format, and activation modes

Using ONLY the information from Phase 1 and Phase 2, generate the file hierarchy:

#### Root AGENTS.md

Read `${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md`. Fill placeholders. Remove empty sections. Target: 15-40 lines.

#### Subdirectory AGENTS.md (per detected scope)

If scopes detected, read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-agents-md.md`. Only scope-specific content differing from root.

#### .cursor/rules/ Files (Metadata-Controlled Rules)

If file-pattern-specific rules or agent-requested rules detected, read `${CLAUDE_SKILL_DIR}/assets/templates/cursor-rule.mdc`. Consult `${CLAUDE_SKILL_DIR}/references/cursor-rules-system.md` for:

- When to create .mdc rules vs using AGENTS.md
- Activation modes: Always (`alwaysApply: true`), Auto-attached (`globs`), Agent-requested (`description`), Manual
- Valid frontmatter fields: ONLY `description`, `alwaysApply`, `globs`
- File naming: kebab-case `.mdc` files in `.cursor/rules/`

#### Domain Files

If non-standard domain patterns detected, read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md`.

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its **Validation Loop Instructions** against every generated file.

Check both general criteria AND the Cursor-specific structural checks:
- `.mdc` files use ONLY valid frontmatter fields (`description`, `alwaysApply`, `globs`)
- No `paths:` frontmatter (Claude-specific — invalid in Cursor)
- Activation mode is appropriate for each rule's content
- Always-loaded content is minimal (use auto-attached or agent-requested where possible)

Maximum 3 iterations.

### Phase 5: Present and Write

1. Show the user ALL generated files with their content before writing
2. Explain briefly why each file exists and what evidence supports its content
3. Highlight which files are always-loaded (root AGENTS.md, `alwaysApply: true` rules) vs on-demand (subdirectory AGENTS.md, globs-based rules, agent-requested rules)
4. Ask for confirmation before writing files
5. Write all files to the project
6. Create `.cursor/rules/` directory if generating rules files
