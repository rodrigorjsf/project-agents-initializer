# Feature: Plugin Skills Evolution

## Summary

Rewrite all 4 plugin SKILL.md files (`init-agents`, `init-claude`, `improve-agents`, `improve-claude`) to replace inline templates and checklists with explicit loading instructions pointing to the `references/` and `assets/templates/` directories created in Phases 1-3. Add a self-validation loop phase to every skill that reads `references/validation-criteria.md` and iterates up to 3 times before presenting output. Agent delegation patterns remain unchanged.

## User Story

As a developer using the agents-initializer plugin
I want skills that load evidence-based guidance from reference documents and validate their own output
So that generated CLAUDE.md/AGENTS.md files consistently follow best practices without manual quality review

## Problem Statement

The 4 plugin SKILL.md files embed templates as inline code blocks and checklists as inline bullet lists. This means: (1) templates can't be updated independently of skill logic, (2) the same template content is duplicated between init and improve skills, (3) no self-validation loop exists to verify output quality, and (4) reference knowledge (progressive disclosure, exclusion criteria, context optimization) is paraphrased rather than loaded from authoritative source documents.

## Solution Statement

Replace inline content with `Read` instructions referencing externalized files using `${CLAUDE_SKILL_DIR}` variable substitution. Add a new self-validation phase between generation and presentation. Keep agent delegation exactly as-is (hard requirement from `.claude/rules/plugin-skills.md`).

## Metadata

| Field            | Value                                                        |
| ---------------- | ------------------------------------------------------------ |
| Type             | ENHANCEMENT                                                  |
| Complexity       | HIGH                                                         |
| Systems Affected | `plugins/agents-initializer/skills/init-agents/`, `init-claude/`, `improve-agents/`, `improve-claude/` |
| Dependencies     | None (pure markdown, no external libs)                       |
| Estimated Tasks  | 4                                                            |

---

## UX Design

### Before State

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐             ║
║   │  Developer   │ ───► │  /init-*     │ ───► │  SKILL.md    │             ║
║   │  invokes     │      │  /improve-*  │      │  body loaded │             ║
║   └──────────────┘      └──────────────┘      └──────┬───────┘             ║
║                                                       │                     ║
║                                                       ▼                     ║
║   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐             ║
║   │ Phase 1:     │ ───► │ Phase 2:     │ ───► │ Phase 3:     │             ║
║   │ Agent 1      │      │ Agent 2      │      │ INLINE       │             ║
║   │ (delegation) │      │ (delegation) │      │ templates +  │             ║
║   └──────────────┘      └──────────────┘      │ inline rules │             ║
║                                                └──────┬───────┘             ║
║                                                       │                     ║
║                                                       ▼                     ║
║                                                ┌──────────────┐             ║
║                                                │ Phase 4:     │             ║
║                                                │ Present →    │             ║
║                                                │ Write        │             ║
║                                                │ (NO VALID.)  │             ║
║                                                └──────────────┘             ║
║                                                                             ║
║   PAIN_POINTS:                                                              ║
║   - Templates duplicated inline in SKILL.md body (~28-61 lines each)       ║
║   - Checklists duplicated inline (~11-18 lines each)                        ║
║   - No quality validation before presenting output                          ║
║   - Reference knowledge paraphrased, not loaded from source docs            ║
║   - Template updates require editing SKILL.md (coupled)                     ║
║                                                                             ║
║   references/ ── exists on disk but UNUSED                                  ║
║   assets/     ── exists on disk but UNUSED                                  ║
║                                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              AFTER STATE                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐             ║
║   │  Developer   │ ───► │  /init-*     │ ───► │  SKILL.md    │             ║
║   │  invokes     │      │  /improve-*  │      │  body loaded │             ║
║   └──────────────┘      └──────────────┘      └──────┬───────┘             ║
║                                                       │                     ║
║                                                       ▼                     ║
║   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐             ║
║   │ Phase 1:     │ ───► │ Phase 2:     │ ───► │ Phase 3:     │             ║
║   │ Agent 1      │      │ Agent 2      │      │ Read refs +  │             ║
║   │ (unchanged)  │      │ (unchanged)  │      │ Read tmpls   │             ║
║   └──────────────┘      └──────────────┘      └──────┬───────┘             ║
║                                                       │                     ║
║                        ┌──────────────────────────────┘                     ║
║                        ▼                                                    ║
║                 ┌──────────────┐                                            ║
║                 │ Phase 4: NEW │ ◄── Self-validation loop (max 3 iters)     ║
║                 │ Read valid.  │     Reads references/validation-criteria.md ║
║                 │ criteria →   │     Evaluates ALL criteria                  ║
║                 │ loop until   │     Fixes failures automatically            ║
║                 │ ALL pass     │     Surfaces remaining issues to user       ║
║                 └──────┬───────┘                                            ║
║                        │                                                    ║
║                        ▼                                                    ║
║                 ┌──────────────┐                                            ║
║                 │ Phase 5:     │                                             ║
║                 │ Present →    │                                             ║
║                 │ Confirm →    │                                             ║
║                 │ Write        │                                             ║
║                 └──────────────┘                                            ║
║                                                                             ║
║   VALUE_ADD:                                                                ║
║   - Templates loaded from assets/ (independently updatable)                 ║
║   - References loaded from references/ (authoritative source)               ║
║   - Self-validation catches quality issues before user sees output          ║
║   - SKILL.md is leaner orchestrator (~80-150 lines vs 116-176)             ║
║                                                                             ║
║   references/ ── ACTIVELY LOADED during Phase 3 + Phase 4                   ║
║   assets/     ── ACTIVELY LOADED during Phase 3                             ║
║                                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Skill | Before | After | User Impact |
|-------|--------|-------|-------------|
| All 4 skills | Inline templates in SKILL.md body | Templates loaded from `assets/templates/` via `${CLAUDE_SKILL_DIR}` | Templates updatable without touching SKILL.md |
| All 4 skills | No validation before output | Self-validation loop (max 3 iterations) | Output quality guaranteed before presentation |
| init-agents | Inline "What NOT to Include" table | References `what-not-to-include.md` + `context-optimization.md` | More comprehensive exclusion evidence |
| init-claude | Inline "File Loading Behavior" table | References `progressive-disclosure-guide.md` | More detailed hierarchy guidance |
| improve-agents | Inline "Improvement Checklist" | References `validation-criteria.md` loop | Iterative validation vs single-pass check |
| improve-claude | Inline checklist + loading table | References `validation-criteria.md` + `evaluation-criteria.md` | Full scoring rubric + iterative validation |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | all (116) | Current init-agents — baseline to rewrite |
| P0 | `plugins/agents-initializer/skills/init-claude/SKILL.md` | all (176) | Current init-claude — baseline to rewrite |
| P0 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | all (122) | Current improve-agents — baseline to rewrite |
| P0 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | all (160) | Current improve-claude — baseline to rewrite |
| P0 | `.claude/rules/plugin-skills.md` | all | HARD CONSTRAINT: agent delegation required |
| P0 | `plugins/agents-initializer/CLAUDE.md` | all | Plugin conventions — delegation mandatory |
| P1 | `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md` | all (77) | Self-validation loop spec to wire in |
| P1 | `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` | all (135) | Scoring rubric to reference in improve skills |
| P1 | `plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md` | all (34) | Template format to reference (not inline) |
| P1 | `plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md` | all (35) | Template format to reference (not inline) |
| P2 | `plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md` | 1-30 | File hierarchy decision table |
| P2 | `plugins/agents-initializer/skills/init-agents/references/what-not-to-include.md` | all (60) | Exclusion evidence table |
| P2 | `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md` | 1-30 | Rules system conventions |
| P2 | `docs/research-claude-code-skills-format.md` | 126-185 | `${CLAUDE_SKILL_DIR}` variable and reference loading pattern |

---

## Patterns to Mirror

**YAML_FRONTMATTER** (keep identical):

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:1-4
// PRESERVE THIS PATTERN EXACTLY:
---
name: init-agents
description: "Initialize optimized AGENTS.md hierarchy..."
---
```

**AGENT_DELEGATION** (keep identical — hard rule from `.claude/rules/plugin-skills.md`):

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:31-35
// PRESERVE THIS PATTERN EXACTLY:
Delegate to the `codebase-analyzer` agent with this task:

> Analyze the project at the current working directory. Return ONLY non-standard,
> non-obvious information that would cause an agent to make mistakes if it didn't
> know them. Be ruthlessly minimal.

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an
isolated context. Wait for it to complete and parse its structured output.
```

**HARD_RULES_BLOCK** (keep `<RULES>` XML tags):

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:16-25
// PRESERVE THIS PATTERN:
<RULES>
- **NEVER** generate a single file with everything — use hierarchical progressive disclosure
...
</RULES>
```

**REFERENCE_LOADING** (NEW pattern to introduce):

```markdown
// PATTERN: Load reference files using ${CLAUDE_SKILL_DIR} variable substitution
// Agent Skills spec: ${CLAUDE_SKILL_DIR} resolves to the skill's directory at runtime
// SOURCE: docs/research-claude-code-skills-format.md:133

Read `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` for file hierarchy decisions.
Read `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` for content exclusion criteria.
```

**TEMPLATE_LOADING** (NEW pattern to introduce):

```markdown
// PATTERN: Load template files for file generation
// Templates use HTML comments for machine-readable instructions and [bracketed] placeholders

For the root file, read `${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md`. Fill its placeholders using ONLY the analysis output from Phase 1 and Phase 2. Follow the HTML comment instructions in the template to determine which sections to include or remove.
```

**SELF_VALIDATION_LOOP** (NEW pattern to introduce):

```markdown
// PATTERN: Self-validation loop referencing externalized criteria
// SOURCE: plugins/agents-initializer/skills/init-agents/references/validation-criteria.md:67-77

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its **Validation Loop Instructions** against every generated file. The loop allows a maximum of 3 iterations. Do not present files to the user until all criteria pass.
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/init-agents/SKILL.md` | REWRITE | Replace inline templates with asset loading, add self-validation phase |
| `plugins/agents-initializer/skills/init-claude/SKILL.md` | REWRITE | Replace inline templates + loading table with reference/asset loading, add self-validation |
| `plugins/agents-initializer/skills/improve-agents/SKILL.md` | REWRITE | Add evaluation-criteria loading, replace inline checklist with validation loop |
| `plugins/agents-initializer/skills/improve-claude/SKILL.md` | REWRITE | Add evaluation-criteria + claude-rules-system loading, replace checklist + loading table |

---

## NOT Building (Scope Limits)

- **Standalone skills** — those are Phase 5 (separate plan). Plugin and standalone SKILL.md files are in different directories with different conventions.
- **Reference or template file changes** — Phases 1-3 are complete. Reference and template content is final.
- **Agent file changes** — agents (`codebase-analyzer`, `scope-detector`, `file-evaluator`) remain unchanged.
- **Rules file updates** — that's Phase 6, which depends on this phase completing first.
- **plugin.json changes** — that's Phase 6.
- **New frontmatter fields** — the YAML frontmatter for each skill stays identical.
- **Changing agent delegation prompts** — the exact blockquoted prompts sent to agents must remain unchanged.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: REWRITE `plugins/agents-initializer/skills/init-agents/SKILL.md`

**ACTION**: Complete rewrite of init-agents skill to use references and assets

**Current state**: 116 lines with inline root template (lines 49-76), inline scoped template (lines 78-94), inline domain file instructions (lines 95-97), and inline "What NOT to Include" table (lines 106-116). No self-validation.

**Target state**: ~80 lines. Templates externalized, references loaded, self-validation added.

**Structure of rewritten file**:

```
---
name: init-agents
description: [KEEP EXISTING — copy exactly from current line 3]
---

# Initialize AGENTS.md

[KEEP: current lines 8-13 — intro paragraph and "Why This Approach" section,
 shortened to remove the inline evidence citations that are now in references]

## Hard Rules

[KEEP EXACTLY: current lines 16-25 — <RULES> block unchanged]

## Process

### Phase 1: Codebase Analysis

[KEEP EXACTLY: current lines 31-35 — agent delegation unchanged]

### Phase 2: Scope Detection

[KEEP EXACTLY: current lines 39-43 — agent delegation unchanged]

### Phase 3: Generate Files

[NEW: Reference and template loading instructions]

Before generating, read these reference documents:
- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — file hierarchy decisions
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines

Using ONLY the information from Phase 1 and Phase 2, generate the file hierarchy:

#### Root AGENTS.md

Read `${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md`. Fill its placeholders
using analysis output. Follow the HTML comment instructions to include/remove sections.
Remove any section that would be empty. Target: 15-40 lines.

#### Scope AGENTS.md (per detected scope)

If scopes were detected, read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-agents-md.md`
for each scope. Only include scope-specific content that differs from root.

#### Domain Files (only if non-standard patterns detected)

If the codebase-analyzer identified non-standard domain patterns, read
`${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md` and generate a file per domain.

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its
**Validation Loop Instructions** against every generated file.

The loop evaluates all hard limits and quality checks, fixes any failures,
and re-evaluates — maximum 3 iterations. Do not proceed to Phase 5 until
ALL criteria pass for ALL files.

### Phase 5: Present and Write

[KEEP: current lines 101-104 — show files, explain, confirm, write]
```

**PRESERVE UNCHANGED**:

- YAML frontmatter (lines 1-4)
- Agent delegation in Phase 1 (lines 31-35) — exact blockquote text
- Agent delegation in Phase 2 (lines 39-43) — exact blockquote text
- Hard Rules `<RULES>` block (lines 16-25)

**REMOVE**:

- Inline root template code block (lines 49-76)
- Inline scoped template code block (lines 78-94)
- Inline domain file paragraph (lines 95-97) — replaced by template loading
- "What NOT to Include" evidence table (lines 106-116) — now in `references/what-not-to-include.md`

**ADD**:

- Reference loading instructions in Phase 3 (~6 lines)
- Template loading instructions in Phase 3 (~12 lines)
- New Phase 4: Self-Validation (~8 lines)
- Phase renumbering: current Phase 4 becomes Phase 5

**GOTCHA**: The `${CLAUDE_SKILL_DIR}` variable is substituted by Claude Code at runtime (see `docs/research-claude-code-skills-format.md:133`). Use it for ALL file references — relative paths resolve to CWD (user's project), not the skill directory.

**GOTCHA**: The "Why This Approach" section should remain but can be shortened. It provides motivational context that affects how the model approaches the task. Do NOT remove it entirely.

**VALIDATE**:

```bash
# File exists and has content
wc -l plugins/agents-initializer/skills/init-agents/SKILL.md
# Under 500 lines (Agent Skills spec limit)
test $(wc -l < plugins/agents-initializer/skills/init-agents/SKILL.md) -lt 500

# YAML frontmatter intact
head -4 plugins/agents-initializer/skills/init-agents/SKILL.md | grep -q "^name: init-agents"

# No inline templates remain (no ```markdown code blocks with placeholder patterns)
! grep -c '^\`\`\`markdown' plugins/agents-initializer/skills/init-agents/SKILL.md | grep -qv '^0$'

# Agent delegation preserved
grep -q 'Delegate to the `codebase-analyzer` agent' plugins/agents-initializer/skills/init-agents/SKILL.md
grep -q 'Delegate to the `scope-detector` agent' plugins/agents-initializer/skills/init-agents/SKILL.md

# References loaded
grep -q '${CLAUDE_SKILL_DIR}/references/validation-criteria.md' plugins/agents-initializer/skills/init-agents/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md' plugins/agents-initializer/skills/init-agents/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/what-not-to-include.md' plugins/agents-initializer/skills/init-agents/SKILL.md

# Templates loaded
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md' plugins/agents-initializer/skills/init-agents/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/scoped-agents-md.md' plugins/agents-initializer/skills/init-agents/SKILL.md

# Self-validation phase present
grep -q 'Self-Validation' plugins/agents-initializer/skills/init-agents/SKILL.md
grep -q 'Validation Loop' plugins/agents-initializer/skills/init-agents/SKILL.md

# Referenced files exist
test -f plugins/agents-initializer/skills/init-agents/references/validation-criteria.md
test -f plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md
test -f plugins/agents-initializer/skills/init-agents/references/what-not-to-include.md
test -f plugins/agents-initializer/skills/init-agents/references/context-optimization.md
test -f plugins/agents-initializer/skills/init-agents/assets/templates/root-agents-md.md
test -f plugins/agents-initializer/skills/init-agents/assets/templates/scoped-agents-md.md
test -f plugins/agents-initializer/skills/init-agents/assets/templates/domain-doc.md
```

---

### Task 2: REWRITE `plugins/agents-initializer/skills/init-claude/SKILL.md`

**ACTION**: Complete rewrite of init-claude skill to use references and assets

**Current state**: 176 lines with inline root template (lines 56-83), inline scoped template (lines 85-102), inline rules template (lines 104-136), inline domain paragraph (lines 138-140), "File Loading Behavior" table (lines 151-164), and inline "What NOT to Include" table (lines 166-176). No self-validation.

**Target state**: ~105 lines. All inline content externalized, references loaded, self-validation added.

**Structure of rewritten file**:

```
---
name: init-claude
description: [KEEP EXISTING — copy exactly from current line 3]
---

# Initialize CLAUDE.md

[KEEP: current lines 8-9 — intro paragraph]

## Why This Approach

[KEEP but SHORTEN: current lines 12-19 — condense to essential motivation.
 The detailed loading behavior table is now in references/progressive-disclosure-guide.md.
 Keep the 4-tier bullet list (Root, Subdirectory, .claude/rules/, Domain files) as brief
 context — this is unique to Claude and helps the model understand the skill's purpose.]

## Hard Rules

[KEEP EXACTLY: current lines 22-32 — <RULES> block unchanged]

## Process

### Phase 1: Codebase Analysis

[KEEP EXACTLY: current lines 38-42 — agent delegation unchanged]

### Phase 2: Scope Detection

[KEEP EXACTLY: current lines 46-50 — agent delegation unchanged.
 IMPORTANT: The scope-detector blockquote for init-claude includes additional text
 about path-scoped .claude/rules/ and shared packages — preserve this exactly]

### Phase 3: Generate Files

[NEW: Reference and template loading instructions]

Before generating, read these reference documents:
- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines
- `${CLAUDE_SKILL_DIR}/references/claude-rules-system.md` — .claude/rules/ conventions and path-scoping

Using ONLY the information from Phase 1 and Phase 2, generate the file hierarchy:

#### Root CLAUDE.md

Read `${CLAUDE_SKILL_DIR}/assets/templates/root-claude-md.md`. Fill placeholders.
Remove empty sections. Target: 15-40 lines.

#### Subdirectory CLAUDE.md (per detected scope)

If scopes detected, read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-claude-md.md`.
Only scope-specific content differing from root.

#### .claude/rules/ Files (Path-Scoped Rules)

If file-pattern-specific rules detected, read `${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md`.
Consult `${CLAUDE_SKILL_DIR}/references/claude-rules-system.md` for:
- When to create rules files vs using CLAUDE.md
- Path-scoping conventions and glob patterns
- Convention rules vs domain-critical rules categories

#### Domain Files

If non-standard domain patterns detected, read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md`.

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its
**Validation Loop Instructions** against every generated file.

Check both general criteria AND the CLAUDE.md-specific structural checks
(path-scoping, minimal always-loaded content). Maximum 3 iterations.

### Phase 5: Present and Write

[KEEP: current lines 144-149 — show files, explain, highlight always-loaded vs on-demand, confirm, write, create .claude/rules/ directory]
```

**PRESERVE UNCHANGED**:

- YAML frontmatter (lines 1-4)
- Agent delegation in Phase 1 (lines 38-42)
- Agent delegation in Phase 2 (lines 46-50) — NOTE: init-claude's scope-detector prompt includes extra text about .claude/rules/ and shared packages that differs from init-agents
- Hard Rules `<RULES>` block (lines 22-32)
- Phase 5 step about creating `.claude/rules/` directory (line 149)

**REMOVE**:

- Inline root CLAUDE.md template (lines 56-83)
- Inline scoped CLAUDE.md template (lines 85-102)
- Inline .claude/rules/ template + prose (lines 104-136)
- Inline domain file paragraph (lines 138-140)
- "File Loading Behavior" table (lines 151-164) — now in `progressive-disclosure-guide.md`
- "What NOT to Include" table (lines 166-176) — now in `what-not-to-include.md`

**ADD**:

- Reference loading with 4 references (adds `claude-rules-system.md`)
- Template loading with 4 templates (adds `claude-rule.md`)
- Phase 4: Self-Validation with CLAUDE.md-specific note
- Phase renumbering: current Phase 4 becomes Phase 5

**GOTCHA**: init-claude's Phase 2 delegation prompt is DIFFERENT from init-agents. The scope-detector blockquote includes additional text about "path-scoped .claude/rules/ files" and "shared/library packages in monorepos". Copy this exactly — do not simplify to match init-agents.

**GOTCHA**: Keep the "Why This Approach" section's 4-tier bullet list (Root CLAUDE.md, Subdirectory CLAUDE.md, .claude/rules/, Domain files). This is Claude Code-specific context that helps the model understand the unique hierarchy. But REMOVE the detailed "File Loading Behavior" table — that's now in the reference file.

**VALIDATE**:

```bash
wc -l plugins/agents-initializer/skills/init-claude/SKILL.md
test $(wc -l < plugins/agents-initializer/skills/init-claude/SKILL.md) -lt 500

head -4 plugins/agents-initializer/skills/init-claude/SKILL.md | grep -q "^name: init-claude"

! grep -c '^\`\`\`markdown' plugins/agents-initializer/skills/init-claude/SKILL.md | grep -qv '^0$'
! grep -c '^\`\`\`yaml' plugins/agents-initializer/skills/init-claude/SKILL.md | grep -qv '^0$'

grep -q 'Delegate to the `codebase-analyzer` agent' plugins/agents-initializer/skills/init-claude/SKILL.md
grep -q 'Delegate to the `scope-detector` agent' plugins/agents-initializer/skills/init-claude/SKILL.md

grep -q '${CLAUDE_SKILL_DIR}/references/claude-rules-system.md' plugins/agents-initializer/skills/init-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md' plugins/agents-initializer/skills/init-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/validation-criteria.md' plugins/agents-initializer/skills/init-claude/SKILL.md

grep -q 'Self-Validation' plugins/agents-initializer/skills/init-claude/SKILL.md
grep -q 'Validation Loop' plugins/agents-initializer/skills/init-claude/SKILL.md

# All referenced files exist
test -f plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md
test -f plugins/agents-initializer/skills/init-claude/assets/templates/claude-rule.md
test -f plugins/agents-initializer/skills/init-claude/assets/templates/root-claude-md.md
test -f plugins/agents-initializer/skills/init-claude/assets/templates/scoped-claude-md.md
test -f plugins/agents-initializer/skills/init-claude/assets/templates/domain-doc.md
```

---

### Task 3: REWRITE `plugins/agents-initializer/skills/improve-agents/SKILL.md`

**ACTION**: Complete rewrite of improve-agents skill to use references and assets

**Current state**: 122 lines with inline improvement plan structure (lines 60-79), inline Phase 4 present+apply (lines 81-106), and inline "Improvement Checklist" (lines 108-122). No evaluation-criteria loading. No self-validation loop.

**Target state**: ~110 lines. Evaluation criteria loaded from reference, templates loaded for output structure, checklist replaced by self-validation loop.

**Structure of rewritten file**:

```
---
name: improve-agents
description: [KEEP EXISTING — copy exactly from current line 3]
---

# Improve AGENTS.md

[KEEP: current lines 8-9 — intro paragraph]

## Why This Matters

[KEEP: current lines 12-16 — condense slightly but keep the core research citations]

## Hard Rules

[KEEP EXACTLY: current lines 19-27 — <RULES> block unchanged]

## Process

### Phase 1: Current State Analysis

[NEW: Add evaluation criteria loading BEFORE agent delegation]

Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the complete scoring
rubric, bloat indicators table, and staleness detection patterns. Use this to inform
the file-evaluator delegation and to understand the expected output format.

[KEEP EXACTLY: current lines 33-45 — file-evaluator agent delegation unchanged]

### Phase 2: Codebase Comparison

[KEEP EXACTLY: current lines 49-58 — codebase-analyzer agent delegation unchanged]

### Phase 3: Generate Improvement Plan

[NEW: Add reference and template loading]

Read these reference documents for improvement guidance:
- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — hierarchy decisions
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines

Based on both subagent reports, create an improvement plan.

[KEEP: current lines 64-79 — Removal → Refactoring → Addition categorization unchanged]

When generating new or restructured files, use these templates for consistent structure:
- Root AGENTS.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md`
- Scoped AGENTS.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-agents-md.md`
- Domain docs: Read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md`

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its
**Validation Loop Instructions** against every improved or newly created file.

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"**
section in validation-criteria.md — checking information preservation, custom
command retention, and progressive disclosure structure preservation.

Maximum 3 iterations. Do not proceed to Phase 5 until ALL criteria pass.

### Phase 5: Present and Apply

[KEEP: current lines 83-106 — issue summary, specific changes, confirm, apply, verify, metrics.
 But REMOVE the verify sub-items at lines 98-101 since self-validation already covers these]
```

**PRESERVE UNCHANGED**:

- YAML frontmatter (lines 1-4)
- Agent delegation in Phase 1 (lines 33-45) — file-evaluator with full blockquote
- Agent delegation in Phase 2 (lines 49-58) — codebase-analyzer with full blockquote
- Hard Rules `<RULES>` block (lines 19-27)
- Improvement Plan categorization (lines 64-79) — Removal → Refactoring → Addition

**REMOVE**:

- "Improvement Checklist" section (lines 108-122) — replaced by self-validation loop
- Phase 4 verify sub-items (lines 98-101) — redundant with self-validation

**ADD**:

- `evaluation-criteria.md` loading instruction in Phase 1 (~4 lines)
- Reference loading instructions in Phase 3 (~5 lines)
- Template loading instructions in Phase 3 (~5 lines)
- Phase 4: Self-Validation with improve-specific note (~8 lines)
- Phase renumbering: current Phase 4 becomes Phase 5

**GOTCHA**: The improve skills use DIFFERENT agents than init skills. Phase 1 uses `file-evaluator` (not `codebase-analyzer`). Phase 2 uses `codebase-analyzer` (not `scope-detector`). Do NOT copy agent delegation from init skills.

**GOTCHA**: The improve-agents `codebase-analyzer` delegation blockquote (lines 51-56) is DIFFERENT from init-agents. It focuses on "verifying that tooling commands documented in AGENTS.md files still work" and "identifying scopes that have distinct tooling but lack their own AGENTS.md". Copy exactly.

**GOTCHA**: The Improvement Plan categorization (Removal → Refactoring → Addition) is critical business logic. It defines the priority order: remove waste first, then restructure, then add only what's genuinely missing. Preserve this exactly.

**VALIDATE**:

```bash
wc -l plugins/agents-initializer/skills/improve-agents/SKILL.md
test $(wc -l < plugins/agents-initializer/skills/improve-agents/SKILL.md) -lt 500

head -4 plugins/agents-initializer/skills/improve-agents/SKILL.md | grep -q "^name: improve-agents"

grep -q 'Delegate to the `file-evaluator` agent' plugins/agents-initializer/skills/improve-agents/SKILL.md
grep -q 'Delegate to the `codebase-analyzer` agent' plugins/agents-initializer/skills/improve-agents/SKILL.md

grep -q '${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md' plugins/agents-initializer/skills/improve-agents/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/validation-criteria.md' plugins/agents-initializer/skills/improve-agents/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/root-agents-md.md' plugins/agents-initializer/skills/improve-agents/SKILL.md

grep -q 'Self-Validation' plugins/agents-initializer/skills/improve-agents/SKILL.md
grep -q 'IMPROVE Operation' plugins/agents-initializer/skills/improve-agents/SKILL.md

# No inline checklist remains
! grep -q '## Improvement Checklist' plugins/agents-initializer/skills/improve-agents/SKILL.md

test -f plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md
test -f plugins/agents-initializer/skills/improve-agents/references/validation-criteria.md
```

---

### Task 4: REWRITE `plugins/agents-initializer/skills/improve-claude/SKILL.md`

**ACTION**: Complete rewrite of improve-claude skill to use references and assets

**Current state**: 160 lines with inline improvement plan (lines 69-91), inline Phase 4 present+apply with token impact analysis (lines 92-126), "Loading Behavior Reference" table (lines 128-141), and inline "Improvement Checklist" (lines 143-160). No evaluation-criteria or claude-rules-system loading. No self-validation loop.

**Target state**: ~130 lines. All inline content externalized, all 6 references loaded where needed, self-validation added.

**Structure of rewritten file**:

```
---
name: improve-claude
description: [KEEP EXISTING — copy exactly from current line 3]
---

# Improve CLAUDE.md

[KEEP: current lines 8-9 — intro paragraph]

## Why This Matters

[KEEP but SHORTEN: current lines 12-18 — core research citations.
 Remove the "Key metrics from research" list — this data is now in references]

## Hard Rules

[KEEP EXACTLY: current lines 22-33 — <RULES> block unchanged.
 This includes the ROOT TARGET line and MAXIMIZE on-demand loading]

## Process

### Phase 1: Current State Analysis

[NEW: Add evaluation criteria loading BEFORE agent delegation]

Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the scoring rubric
and bloat/staleness indicators.

[KEEP EXACTLY: current lines 39-53 — file-evaluator agent delegation unchanged.
 IMPORTANT: improve-claude's file-evaluator blockquote includes 8 check items
 (vs 6 for improve-agents) — items 7 and 8 are Claude-specific. Preserve exactly.]

### Phase 2: Codebase Comparison

[KEEP EXACTLY: current lines 57-67 — codebase-analyzer agent delegation unchanged.
 IMPORTANT: improve-claude's blockquote includes 4 focus items (vs 3 for improve-agents)
 — item 3 is Claude-specific about .claude/rules/ path-scoping. Preserve exactly.]

### Phase 3: Generate Improvement Plan

[NEW: Add reference and template loading]

Read these reference documents:
- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md` — hierarchy decisions and loading tiers
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md` — content exclusion criteria
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md` — token budget guidelines
- `${CLAUDE_SKILL_DIR}/references/claude-rules-system.md` — .claude/rules/ conventions and path-scoping

Based on both subagent reports, create improvement plan:

[KEEP: current lines 73-91 — Removal → Refactoring → Addition categorization.
 improve-claude's Refactoring section includes Claude-specific items about
 .claude/rules/ conversion and path-scoping. Preserve exactly.]

When generating new or restructured files, use these templates:
- Root CLAUDE.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/root-claude-md.md`
- Scoped CLAUDE.md: Read `${CLAUDE_SKILL_DIR}/assets/templates/scoped-claude-md.md`
- .claude/rules/ files: Read `${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md`
- Domain docs: Read `${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md`

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its
**Validation Loop Instructions** against every improved or newly created file.

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"**
section. For CLAUDE.md files, also check **CLAUDE.md-specific** structural checks
(path-scoping, minimal always-loaded content). Maximum 3 iterations.

### Phase 5: Present and Apply

[KEEP: current lines 94-126 — issue summary with 7 categories, specific changes,
 token impact analysis (always-loaded vs on-demand), confirm, apply, verify, metrics.
 REMOVE the verify sub-items at lines 116-120 since self-validation covers these.
 KEEP the token impact analysis at lines 109-112 — this is unique to improve-claude
 and valuable for showing the user the efficiency gains.]
```

**PRESERVE UNCHANGED**:

- YAML frontmatter (lines 1-4)
- Agent delegation in Phase 1 (lines 39-53) — file-evaluator with 8-item Claude-specific blockquote
- Agent delegation in Phase 2 (lines 57-67) — codebase-analyzer with 4-item Claude-specific blockquote
- Hard Rules `<RULES>` block (lines 22-33) — includes Claude-specific rules
- Improvement Plan categorization (lines 73-91) — Removal → Refactoring → Addition with Claude-specific items
- Token impact analysis in Phase 5 (current lines 109-112) — unique to improve-claude

**REMOVE**:

- "Loading Behavior Reference" table (lines 128-141) — now in `progressive-disclosure-guide.md`
- "Improvement Checklist" section (lines 143-160) — replaced by self-validation loop
- Phase 5 verify sub-items (lines 116-120) — redundant with self-validation

**ADD**:

- `evaluation-criteria.md` loading in Phase 1 (~3 lines)
- 4-reference loading instructions in Phase 3 (~6 lines)
- 4-template loading instructions in Phase 3 (~6 lines)
- Phase 4: Self-Validation with improve + CLAUDE.md-specific notes (~8 lines)
- Phase renumbering: current Phase 4 becomes Phase 5

**GOTCHA**: improve-claude has the MOST references (6) and templates (4) of any skill. Ensure ALL are loaded:

- References: `validation-criteria.md`, `what-not-to-include.md`, `progressive-disclosure-guide.md`, `context-optimization.md`, `evaluation-criteria.md`, `claude-rules-system.md`
- Templates: `root-claude-md.md`, `scoped-claude-md.md`, `claude-rule.md`, `domain-doc.md`

**GOTCHA**: improve-claude's file-evaluator blockquote (lines 41-51) has 8 check items. Items 7 ("Rules files without path-scoping") and 8 ("Content in root CLAUDE.md that only applies to specific file patterns") are Claude-specific. Do NOT simplify to match improve-agents' 6-item version.

**GOTCHA**: improve-claude's codebase-analyzer blockquote (lines 59-65) has 4 focus items. Item 3 ("Detecting file patterns that have specific conventions but lack path-scoped .claude/rules/") is Claude-specific with extensive detail about convention rules AND domain-critical rules. Preserve exactly.

**GOTCHA**: The token impact analysis in Phase 5 (current lines 109-112) is UNIQUE to improve-claude. It shows "Always-loaded tokens: before → after" and "On-demand tokens: before → after" — this is critical for demonstrating the value of the improvements. Do NOT remove it.

**VALIDATE**:

```bash
wc -l plugins/agents-initializer/skills/improve-claude/SKILL.md
test $(wc -l < plugins/agents-initializer/skills/improve-claude/SKILL.md) -lt 500

head -4 plugins/agents-initializer/skills/improve-claude/SKILL.md | grep -q "^name: improve-claude"

grep -q 'Delegate to the `file-evaluator` agent' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q 'Delegate to the `codebase-analyzer` agent' plugins/agents-initializer/skills/improve-claude/SKILL.md

# All 6 references loaded
grep -q '${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/validation-criteria.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/what-not-to-include.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/context-optimization.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/references/claude-rules-system.md' plugins/agents-initializer/skills/improve-claude/SKILL.md

# All 4 templates loaded
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/root-claude-md.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/scoped-claude-md.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/claude-rule.md' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q '${CLAUDE_SKILL_DIR}/assets/templates/domain-doc.md' plugins/agents-initializer/skills/improve-claude/SKILL.md

# Self-validation present with CLAUDE.md-specific mention
grep -q 'Self-Validation' plugins/agents-initializer/skills/improve-claude/SKILL.md
grep -q 'CLAUDE.md-specific' plugins/agents-initializer/skills/improve-claude/SKILL.md

# Token impact analysis preserved
grep -q 'token impact' plugins/agents-initializer/skills/improve-claude/SKILL.md

# No inline checklist or loading table remains
! grep -q '## Improvement Checklist' plugins/agents-initializer/skills/improve-claude/SKILL.md
! grep -q '## Loading Behavior Reference' plugins/agents-initializer/skills/improve-claude/SKILL.md

# All referenced files exist
test -f plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md
test -f plugins/agents-initializer/skills/improve-claude/references/claude-rules-system.md
test -f plugins/agents-initializer/skills/improve-claude/assets/templates/claude-rule.md
test -f plugins/agents-initializer/skills/improve-claude/assets/templates/root-claude-md.md
```

---

## Testing Strategy

### Validation Per Task

Each task's VALIDATE section contains specific bash commands. Run them immediately after completing each rewrite.

### Cross-Task Validation

After all 4 tasks are complete, run these cross-cutting checks:

```bash
# All 4 SKILL.md files exist and are non-empty
for skill in init-agents init-claude improve-agents improve-claude; do
  echo "=== $skill ==="
  wc -l "plugins/agents-initializer/skills/$skill/SKILL.md"
done

# No inline templates remain across all skills (no ```markdown or ```yaml code blocks)
for skill in init-agents init-claude improve-agents improve-claude; do
  count=$(grep -c '^\`\`\`markdown\|^\`\`\`yaml' "plugins/agents-initializer/skills/$skill/SKILL.md" 2>/dev/null || echo 0)
  echo "$skill: $count inline code blocks (should be 0)"
done

# All skills have self-validation phase
for skill in init-agents init-claude improve-agents improve-claude; do
  grep -q 'Self-Validation' "plugins/agents-initializer/skills/$skill/SKILL.md" && echo "$skill: ✓ self-validation" || echo "$skill: ✗ MISSING self-validation"
done

# All skills reference validation-criteria.md
for skill in init-agents init-claude improve-agents improve-claude; do
  grep -q 'validation-criteria.md' "plugins/agents-initializer/skills/$skill/SKILL.md" && echo "$skill: ✓ validation-criteria" || echo "$skill: ✗ MISSING"
done

# Init skills have scope-detector, improve skills have file-evaluator
grep -q 'scope-detector' plugins/agents-initializer/skills/init-agents/SKILL.md && echo "init-agents: ✓ scope-detector"
grep -q 'scope-detector' plugins/agents-initializer/skills/init-claude/SKILL.md && echo "init-claude: ✓ scope-detector"
grep -q 'file-evaluator' plugins/agents-initializer/skills/improve-agents/SKILL.md && echo "improve-agents: ✓ file-evaluator"
grep -q 'file-evaluator' plugins/agents-initializer/skills/improve-claude/SKILL.md && echo "improve-claude: ✓ file-evaluator"

# Claude skills have claude-rules-system.md reference
grep -q 'claude-rules-system.md' plugins/agents-initializer/skills/init-claude/SKILL.md && echo "init-claude: ✓ claude-rules-system"
grep -q 'claude-rules-system.md' plugins/agents-initializer/skills/improve-claude/SKILL.md && echo "improve-claude: ✓ claude-rules-system"

# Improve skills have evaluation-criteria.md reference
grep -q 'evaluation-criteria.md' plugins/agents-initializer/skills/improve-agents/SKILL.md && echo "improve-agents: ✓ evaluation-criteria"
grep -q 'evaluation-criteria.md' plugins/agents-initializer/skills/improve-claude/SKILL.md && echo "improve-claude: ✓ evaluation-criteria"
```

### Edge Cases Checklist

- [ ] `${CLAUDE_SKILL_DIR}` variable appears in every file path reference (not relative paths)
- [ ] No ````markdown` or````yaml` fenced code blocks remain (inline templates removed)
- [ ] Agent delegation blockquotes are byte-identical to originals (especially the Claude-specific extended versions)
- [ ] init-claude and improve-claude both reference `claude-rules-system.md` and `claude-rule.md`
- [ ] improve skills reference `evaluation-criteria.md` while init skills do NOT
- [ ] init skills use `scope-detector` while improve skills do NOT
- [ ] improve skills use `file-evaluator` while init skills do NOT
- [ ] Self-validation phase mentions IMPROVE-specific checks for improve skills
- [ ] Self-validation phase mentions CLAUDE.md-specific checks for claude skills
- [ ] improve-claude preserves token impact analysis in Phase 5

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify all files exist, are non-empty, and under 500 lines
for skill in init-agents init-claude improve-agents improve-claude; do
  file="plugins/agents-initializer/skills/$skill/SKILL.md"
  lines=$(wc -l < "$file")
  if [ "$lines" -gt 0 ] && [ "$lines" -lt 500 ]; then
    echo "✓ $skill: $lines lines"
  else
    echo "✗ $skill: $lines lines (FAIL)"
  fi
done

# Verify YAML frontmatter is valid (has name and description)
for skill in init-agents init-claude improve-agents improve-claude; do
  file="plugins/agents-initializer/skills/$skill/SKILL.md"
  if head -1 "$file" | grep -q '^---$' && grep -q "^name: $skill$" "$file"; then
    echo "✓ $skill: valid frontmatter"
  else
    echo "✗ $skill: invalid frontmatter"
  fi
done
```

**EXPECT**: All 4 skills pass with valid frontmatter and line count under 500.

### Level 2: STRUCTURAL_CHECKS

```bash
# Run cross-task validation script from Testing Strategy above
```

**EXPECT**: All checks pass — no inline templates, all references present, correct agent assignments.

### Level 3: REFERENCE_INTEGRITY

```bash
# For each SKILL.md, extract all ${CLAUDE_SKILL_DIR}/... paths and verify the files exist
for skill in init-agents init-claude improve-agents improve-claude; do
  dir="plugins/agents-initializer/skills/$skill"
  echo "=== $skill ==="
  grep -oP '\$\{CLAUDE_SKILL_DIR\}/[^\s`"]+' "$dir/SKILL.md" | while read -r ref; do
    actual_path="$dir/${ref#\$\{CLAUDE_SKILL_DIR\}/}"
    if [ -f "$actual_path" ]; then
      echo "  ✓ $ref"
    else
      echo "  ✗ $ref (FILE NOT FOUND: $actual_path)"
    fi
  done
done
```

**EXPECT**: Every referenced file exists on disk.

### Level 4: DELEGATION_PRESERVATION

```bash
# Verify agent delegation blockquotes are preserved
# init skills: codebase-analyzer + scope-detector
# improve skills: file-evaluator + codebase-analyzer
for skill in init-agents init-claude; do
  grep -q 'Delegate to the `codebase-analyzer` agent' "plugins/agents-initializer/skills/$skill/SKILL.md" && echo "✓ $skill: codebase-analyzer"
  grep -q 'Delegate to the `scope-detector` agent' "plugins/agents-initializer/skills/$skill/SKILL.md" && echo "✓ $skill: scope-detector"
done
for skill in improve-agents improve-claude; do
  grep -q 'Delegate to the `file-evaluator` agent' "plugins/agents-initializer/skills/$skill/SKILL.md" && echo "✓ $skill: file-evaluator"
  grep -q 'Delegate to the `codebase-analyzer` agent' "plugins/agents-initializer/skills/$skill/SKILL.md" && echo "✓ $skill: codebase-analyzer"
done
```

**EXPECT**: Correct agents assigned to correct skills.

---

## Acceptance Criteria

- [ ] All 4 SKILL.md files rewritten with no inline templates or checklists
- [ ] Every file path reference uses `${CLAUDE_SKILL_DIR}` variable (not relative paths)
- [ ] All referenced `references/` and `assets/templates/` files exist on disk
- [ ] Agent delegation patterns preserved identically (including Claude-specific extended blockquotes)
- [ ] Self-validation phase present in all 4 skills, referencing `validation-criteria.md`
- [ ] Improve skills load `evaluation-criteria.md` in Phase 1
- [ ] Claude skills load `claude-rules-system.md` and reference `claude-rule.md` template
- [ ] All SKILL.md files under 500 lines
- [ ] YAML frontmatter unchanged (name and description fields identical)
- [ ] Hard Rules `<RULES>` blocks unchanged
- [ ] Level 1-4 validation commands all pass

---

## Completion Checklist

- [ ] Task 1: init-agents SKILL.md rewritten and validated
- [ ] Task 2: init-claude SKILL.md rewritten and validated
- [ ] Task 3: improve-agents SKILL.md rewritten and validated
- [ ] Task 4: improve-claude SKILL.md rewritten and validated
- [ ] Level 1: Static analysis passes (line counts, frontmatter)
- [ ] Level 2: Structural checks pass (no inline templates, correct references)
- [ ] Level 3: Reference integrity passes (all referenced files exist)
- [ ] Level 4: Delegation preservation passes (correct agents per skill)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| `${CLAUDE_SKILL_DIR}` not resolving in plugin context | LOW | HIGH | The variable is documented in the Agent Skills spec and Claude Code docs. Test with a simple skill first if uncertain. |
| Agent delegation blockquotes accidentally modified | MEDIUM | HIGH | Each task's VALIDATE section includes grep checks for exact agent names. Diff the blockquote sections before/after rewrite. |
| SKILL.md exceeds 500 line limit after rewrite | LOW | MEDIUM | All rewrites REMOVE more content than they ADD. Estimated sizes: 80, 105, 110, 130 lines. |
| Self-validation loop instruction unclear to executing model | LOW | MEDIUM | The instruction explicitly points to the reference file and names the specific section ("Validation Loop Instructions"). The reference file has exact loop steps. |
| Improve skills lose Claude-specific blockquote extensions | MEDIUM | HIGH | Each task's GOTCHA sections explicitly warn about Claude-specific differences. Validation checks for Claude-specific terms. |

---

## Notes

### Architecture Decision: `${CLAUDE_SKILL_DIR}` vs Relative Paths

We use `${CLAUDE_SKILL_DIR}` for all file references because the executing model's Read tool resolves paths relative to the user's project CWD, not the skill directory. The `${CLAUDE_SKILL_DIR}` variable is substituted by Claude Code at skill load time (see `docs/research-claude-code-skills-format.md:133`), producing absolute paths that the Read tool can resolve correctly.

### Reference Loading Strategy

References are loaded at the point of use (Phase 3 for generation guidance, Phase 4 for validation), not upfront. This follows the same progressive disclosure principle the skills themselves promote — load knowledge when needed, not all at once.

### Task Dependencies

Tasks 1-4 are independent (different files) and CAN be executed in parallel by separate agents. However, sequential execution is recommended so that patterns established in Task 1 (init-agents) can be verified before applying to the remaining 3 skills. Task 1 is the simplest (fewest references/templates) and serves as the baseline pattern.

### Relationship to Phase 5 (Standalone Skills)

Phase 5 will rewrite the standalone `skills/` versions. Standalone skills differ in that they include converted agent reference docs (`references/codebase-analyzer.md`, `references/scope-detector.md`, `references/file-evaluator.md`) instead of delegating to agents. The SKILL.md structure and self-validation loop will be similar but the analysis phases will be "inline following reference instructions" rather than "delegate to named agent".
