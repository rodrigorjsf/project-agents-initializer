# Feature: Docs Corpus Distillation

## Summary

Distill the 39-document evidence corpus (1.1MB, 15,000+ lines across `docs/`) into 16 compact, artifact-type-specific reference files (each ≤200 lines) with source citations, organized to serve the 8 skills of the `agent-customizer` plugin. Each reference file follows the proven format established by `agents-initializer`: title block, source attribution, optional `## Contents` TOC, section-separated content with inline `*Source:*` citations. The files are distributed as copies across all 8 skill directories (34 total file instances), following the copy-not-symlink convention.

## User Story

As a developer using the `agent-customizer` plugin to create or improve Claude Code artifacts
I want each skill's reference files to contain evidence-based guidance distilled from the docs corpus
So that generated/improved artifacts follow documented best practices without requiring me to read 1.1MB of source documentation

## Problem Statement

The `docs/` corpus contains comprehensive best practices for 4 artifact types (skills, hooks, rules, subagents) spread across 39 files and 15,000+ lines. No structured, compact access path exists for artifact generation skills. Without distillation, skills must either load full source docs (blowing context budgets) or operate without evidence grounding (producing lower-quality artifacts).

## Solution Statement

Create 16 unique reference files (≤200 lines each) organized by artifact type, each distilling relevant docs into instruction-oriented guidance with explicit source citations. Reference files serve as the knowledge base for `agent-customizer` skills, loaded progressively by phase. Follow the exact format and conventions proven by `agents-initializer` reference files.

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | HIGH |
| Systems Affected | `plugins/agent-customizer/skills/*/references/` (8 skill directories) |
| Dependencies | None (Phase 1 complete; Phase 3 runs in parallel) |
| Estimated Tasks | 9 |
| GitHub Issue | #31 |

---

## UX Design

### Before State

```
+---------------------------+     +----------------------------+
|   Developer invokes       |     |   agent-customizer skill   |
|   /create-skill           | --> |   (Phase 3: Generate)      |
+---------------------------+     +----------------------------+
                                          |
                                          v
                                  +----------------------------+
                                  |   NO reference files       |
                                  |   NO docs grounding        |
                                  |   NO source citations      |
                                  +----------------------------+
                                          |
                                          v
                                  +----------------------------+
                                  |   Generated artifact:      |
                                  |   - Ungrounded guidance    |
                                  |   - No evidence citations  |
                                  |   - Generic patterns       |
                                  +----------------------------+

DATA_FLOW: User → Skill → (no references) → generic output
PAIN_POINT: 39 docs (1.1MB) exist but are inaccessible to skills
```

### After State

```
+---------------------------+     +----------------------------+
|   Developer invokes       |     |   agent-customizer skill   |
|   /create-skill           | --> |   (Phase 3: Generate)      |
+---------------------------+     +----------------------------+
                                          |
                                          v
                                  +----------------------------+
                                  |   Reads references:        |
                                  |   skill-authoring-guide.md |
                                  |   skill-format-reference.md|
                                  |   prompt-eng-strategies.md |
                                  +----------------------------+
                                          |
                                          v
                                  +----------------------------+
                                  |   Phase 4: Self-Validate   |
                                  |   Reads:                   |
                                  |   skill-validation-criteria|
                                  +----------------------------+
                                          |
                                          v
                                  +----------------------------+
                                  |   Generated artifact:      |
                                  |   - Evidence-grounded      |
                                  |   - Source citations        |
                                  |   - Best-practice patterns |
                                  +----------------------------+

DATA_FLOW: User → Skill → references (≤200 lines each) → evidence-based output
VALUE_ADD: 15,000+ lines distilled to ~2,500 lines across 16 files, fully cited
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `create-*/references/` | Empty (no directory) | 3-4 reference files per skill | Skills generate evidence-grounded artifacts |
| `improve-*/references/` | Empty (no directory) | 4-5 reference files per skill | Evaluation uses type-specific criteria |
| Docs corpus (39 files) | Unused by skills | Cited via Source: attributions | Every recommendation traceable to evidence |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md` | all | Pattern to MIRROR exactly — title block, Source line, Contents TOC, inline citations, section separators |
| P0 | `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md` | all | Pattern to MIRROR for validation criteria files — structure, hard limits table, quality checks, loop instructions |
| P0 | `.claude/rules/reference-files.md` | all | 7 constraints ALL reference files MUST satisfy |
| P1 | `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` | all | Pattern to MIRROR for evaluation criteria files — scoring rubric, bloat/staleness indicators, output template |
| P1 | `plugins/agents-initializer/skills/improve-claude/references/context-optimization.md` | all | Pattern for shared cross-cutting reference files — how to structure evidence-based guidance |
| P1 | `DESIGN-GUIDELINES.md` | 42-55 | Guideline 2: The 200-Line Budget and line count targets |
| P1 | `DESIGN-GUIDELINES.md` | 137-155 | Guideline 7: Skill Authoring Standards and reference file conventions |
| P1 | `DESIGN-GUIDELINES.md` | 179-193 | Guideline 9: Reference files use structured guidance with tables |

---

## Patterns to Mirror

**TITLE_BLOCK — Every reference file starts with this exact pattern:**

```markdown
# {Title}

{One-line purpose statement.}
Source: {source-doc-1.md}, {source-doc-2.md}

---
```

SOURCE: `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md:1-6`

**CONTENTS_TOC — Required for files over 100 lines:**

```markdown
## Contents

- {Section 1 description (lowercase, concise)}
- {Section 2 description}
- {Section 3 description}

---
```

SOURCE: `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md:8-17`

**INLINE_CITATION — After each section body:**

```markdown
*Source: {doc-filename.md} lines {N-M}*
```

Or multi-source:

```markdown
*Source: {doc-1.md} lines {N-M}; {doc-2.md} lines {X-Y}*
```

SOURCE: `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md:34,54,73`

**SECTION_SEPARATOR — Between all sections:**

```markdown
---
```

SOURCE: All existing reference files use `---` horizontal rules between every section.

**TABLE_FORMAT — Compact, scannable tables per DESIGN-GUIDELINES.md Guideline 9:**

```markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

SOURCE: `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md:23-28`

**VALIDATION_LOOP — Standard pattern for validation criteria files:**

```markdown
## Validation Loop Instructions

Execute this loop for each generated or improved artifact:

1. Evaluate the artifact against ALL criteria above
2. If ANY criterion fails: identify the specific failure, fix the artifact, restart evaluation
3. Maximum 3 iterations — if still failing after 3 attempts, surface the remaining issues to the user
4. Only proceed to writing artifacts when ALL criteria pass

**Do not skip criteria for "minor" violations.** Hard limits are hard limits.
```

SOURCE: `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md:67-76`

---

## Reference File Constraints

Every reference file MUST satisfy these rules (from `.claude/rules/reference-files.md`):

1. **≤200 lines** — hard ceiling
2. **`## Contents` TOC** — required if file exceeds 100 lines, placed after title block
3. **Instruction-oriented framing** — content reads as guidance, not executable scripts
4. **Source attribution** — header-level `Source:` on line 3-4 + inline `*Source:*` per section
5. **Byte-identical copies** — same-filename references across skills must be identical
6. **Update all copies** — when modifying a shared reference, update every copy
7. **No nested references** — reference files must not import/reference other reference files

---

## Files to Change

### Unique Reference Files to CREATE (16 files)

| File | Target Lines | Source Docs | Used By |
|------|-------------|-------------|---------|
| `skill-authoring-guide.md` | ~180 | `skills/skill-authoring-best-practices.md`, `skills/extend-claude-with-skills.md` | create-skill, improve-skill |
| `skill-format-reference.md` | ~150 | `skills/research-claude-code-skills-format.md`, `skills/extend-claude-with-skills.md` | create-skill, improve-skill |
| `skill-evaluation-criteria.md` | ~170 | `skills/skill-authoring-best-practices.md`, `Evaluating-AGENTS-paper.md` | improve-skill |
| `skill-validation-criteria.md` | ~80 | Derived from skill-authoring-guide content | create-skill, improve-skill |
| `hook-authoring-guide.md` | ~180 | `hooks/automate-workflow-with-hooks.md`, `hooks/claude-hook-reference-doc.md` | create-hook, improve-hook |
| `hook-events-reference.md` | ~200 | `hooks/claude-hook-reference-doc.md` | create-hook, improve-hook |
| `hook-evaluation-criteria.md` | ~170 | `hooks/claude-hook-reference-doc.md`, `hooks/automate-workflow-with-hooks.md` | improve-hook |
| `hook-validation-criteria.md` | ~80 | Derived from hook-authoring-guide content | create-hook, improve-hook |
| `subagent-authoring-guide.md` | ~180 | `subagents/research-subagent-best-practices.md`, `subagents/creating-custom-subagents.md` | create-subagent, improve-subagent |
| `subagent-config-reference.md` | ~160 | `subagents/creating-custom-subagents.md`, `subagents/claude-orchestrate-of-claude-code-sessions.md` | create-subagent, improve-subagent |
| `subagent-evaluation-criteria.md` | ~170 | `subagents/research-subagent-best-practices.md`, `subagents/creating-custom-subagents.md` | improve-subagent |
| `subagent-validation-criteria.md` | ~80 | Derived from subagent-authoring-guide content | create-subagent, improve-subagent |
| `rule-authoring-guide.md` | ~160 | `memory/how-claude-remembers-a-project.md` | create-rule, improve-rule |
| `rule-evaluation-criteria.md` | ~170 | `memory/how-claude-remembers-a-project.md` | improve-rule |
| `rule-validation-criteria.md` | ~80 | Derived from rule-authoring-guide content | create-rule, improve-rule |
| `prompt-engineering-strategies.md` | ~180 | `prompt-engineering-guide.md`, `claude-prompting-best-practices.md` | all 8 skills |

### Distribution Matrix (34 file copies across 8 skill directories)

| Skill Directory | References (copy count) |
|-----------------|------------------------|
| `plugins/agent-customizer/skills/create-skill/references/` | skill-authoring-guide, skill-format-reference, prompt-engineering-strategies, skill-validation-criteria (4) |
| `plugins/agent-customizer/skills/create-hook/references/` | hook-authoring-guide, hook-events-reference, prompt-engineering-strategies, hook-validation-criteria (4) |
| `plugins/agent-customizer/skills/create-rule/references/` | rule-authoring-guide, prompt-engineering-strategies, rule-validation-criteria (3) |
| `plugins/agent-customizer/skills/create-subagent/references/` | subagent-authoring-guide, subagent-config-reference, prompt-engineering-strategies, subagent-validation-criteria (4) |
| `plugins/agent-customizer/skills/improve-skill/references/` | skill-authoring-guide, skill-format-reference, skill-evaluation-criteria, prompt-engineering-strategies, skill-validation-criteria (5) |
| `plugins/agent-customizer/skills/improve-hook/references/` | hook-authoring-guide, hook-events-reference, hook-evaluation-criteria, prompt-engineering-strategies, hook-validation-criteria (5) |
| `plugins/agent-customizer/skills/improve-rule/references/` | rule-authoring-guide, rule-evaluation-criteria, prompt-engineering-strategies, rule-validation-criteria (4) |
| `plugins/agent-customizer/skills/improve-subagent/references/` | subagent-authoring-guide, subagent-config-reference, subagent-evaluation-criteria, prompt-engineering-strategies, subagent-validation-criteria (5) |

---

## NOT Building (Scope Limits)

- **Not creating SKILL.md files** — Phase 4 creates skill entry points; Phase 2 creates only reference files
- **Not creating subagent/agent definition files** — Phase 3 scaffolds agents; references here serve skills, not agents
- **Not creating asset templates** — Phase 3 creates templates; references are guidance, not output templates
- **Not creating standalone distribution references** — Phase 9 handles standalone; Phase 2 is plugin-only
- **Not updating reference-files.md rule** — Phase 3 updates rule paths to include `plugins/agent-customizer/`
- **Not distilling `docs/plugins/claude-create-plugin-doc.md`** — plugin creation docs are for Phase 3 infrastructure, not artifact generation
- **Not distilling `docs/plans/` files** — internal design docs, not evidence corpus for artifact generation

---

## Source Docs Inventory

### Primary Sources by Artifact Type

| Artifact Type | Source Docs (lines) | Analysis Files (lines) | Total Input |
|---------------|--------------------|-----------------------|-------------|
| Skills | `skill-authoring-best-practices.md` (1155), `extend-claude-with-skills.md` (681), `research-claude-code-skills-format.md` (504) | `analysis-skill-authoring-best-practices.md` (695), `analysis-extend-claude-with-skills.md` (669), `analysis-research-claude-code-skills-format.md` (768) | 4,472 lines |
| Hooks | `claude-hook-reference-doc.md` (2077), `automate-workflow-with-hooks.md` (745) | `analysis-claude-hook-reference-doc.md` (517), `analysis-automate-workflow-with-hooks.md` (848) | 4,187 lines |
| Subagents | `creating-custom-subagents.md` (900), `research-subagent-best-practices.md` (1044), `claude-orchestrate-of-claude-code-sessions.md` (393) | `analysis-creating-custom-subagents.md` (503), `analysis-research-subagent-best-practices.md` (475), `analysis-claude-orchestrate-of-claude-code-sessions.md` (325) | 3,640 lines |
| Rules | `how-claude-remembers-a-project.md` (361) | `analysis-how-claude-remembers-a-project.md` (441) | 802 lines |
| Cross-cutting | `prompt-engineering-guide.md` (508), `claude-prompting-best-practices.md` (753), `research-llm-context-optimization.md` (567), `Evaluating-AGENTS-paper.md` (613), `a-guide-to-agents.md` (238), `a-guide-to-claude.md` (224) | `analysis-prompt-engineering-guide.md` (802), `analysis-claude-prompting-best-practices.md` (425), `analysis-research-llm-context-optimization.md` (728), `analysis-evaluating-agents-paper.md` (480), `analysis-a-guide-to-agents.md` (324), `analysis-a-guide-to-claude.md` (430) | 6,092 lines |

**Total distillation input: ~19,193 lines → 16 reference files (~2,500 lines total)**

### Analysis Files Usage

The 16 `docs/analysis/` files are pre-synthesized summaries in Portuguese. Use them as accelerators during distillation — they identify key patterns, tables, and insights already extracted from primary sources. Always verify against the primary source before citing. Reference files must be written in English. Cite primary source docs (not analysis files) in `Source:` attributions.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE skill reference files

- **ACTION**: Read skill docs, distill into 2 reference files
- **READ**: `docs/skills/skill-authoring-best-practices.md` (1155 lines), `docs/skills/extend-claude-with-skills.md` (681 lines), `docs/skills/research-claude-code-skills-format.md` (504 lines)
- **ACCELERATORS**: `docs/analysis/analysis-skill-authoring-best-practices.md`, `docs/analysis/analysis-extend-claude-with-skills.md`, `docs/analysis/analysis-research-claude-code-skills-format.md`
- **MIRROR**: `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md` — follow identical title block, Source line, Contents TOC, section separators, inline citations
- **OUTPUT 1**: `plugins/agent-customizer/skills/create-skill/references/skill-authoring-guide.md` (~180 lines)
  - **Content focus**: SKILL.md structure and phases, frontmatter fields (`description`, `user-invocable`, `disable-model-invocation`, `context`), progressive disclosure via `references/` and `assets/`, reference file conventions, testing with all models, conciseness principles, common anti-patterns
  - **Must cite**: `skills/skill-authoring-best-practices.md` with line ranges, `skills/extend-claude-with-skills.md` with line ranges
- **OUTPUT 2**: `plugins/agent-customizer/skills/create-skill/references/skill-format-reference.md` (~150 lines)
  - **Content focus**: `${CLAUDE_SKILL_DIR}` variable usage, directory structure (`SKILL.md`, `references/`, `assets/templates/`), frontmatter YAML format (all valid fields), available variables (`$ARGUMENTS`, `$USER_PROMPT`), file naming conventions, skill discovery and loading mechanism
  - **Must cite**: `skills/research-claude-code-skills-format.md` with line ranges, `skills/extend-claude-with-skills.md` with line ranges
- **VALIDATE**: `wc -l` both files ≤200; files >100 lines have `## Contents`; both contain `Source:` header; both contain `*Source:*` inline citations

### Task 2: CREATE hook reference files

- **ACTION**: Read hook docs, distill into 2 reference files
- **READ**: `docs/hooks/claude-hook-reference-doc.md` (2077 lines), `docs/hooks/automate-workflow-with-hooks.md` (745 lines)
- **ACCELERATORS**: `docs/analysis/analysis-claude-hook-reference-doc.md`, `docs/analysis/analysis-automate-workflow-with-hooks.md`
- **MIRROR**: Same pattern as Task 1
- **OUTPUT 1**: `plugins/agent-customizer/skills/create-hook/references/hook-authoring-guide.md` (~180 lines)
  - **Content focus**: Hook configuration in `settings.json`, when to use hooks vs rules vs skills (decision criteria), event selection strategy, matcher patterns and glob syntax, three hook types (`command`, `prompt`, `agent`) and when to use each, exit codes and error handling, security considerations, best practices for reliable hooks
  - **Must cite**: `hooks/automate-workflow-with-hooks.md` with line ranges, `hooks/claude-hook-reference-doc.md` with line ranges
- **OUTPUT 2**: `plugins/agent-customizer/skills/create-hook/references/hook-events-reference.md` (~200 lines)
  - **Content focus**: Complete reference table of all 14 hook event types (PreToolUse, PostToolUse, Stop, etc.) with descriptions, JSON schema for hook configuration, input/output contracts per event type, matcher examples per event, common patterns (pre-commit validation, file watching, security enforcement)
  - **Must cite**: `hooks/claude-hook-reference-doc.md` with line ranges
  - **GOTCHA**: 2077 lines → 200 lines requires aggressive distillation. Focus on the reference table + JSON schema + most common patterns. Omit lengthy examples; keep only the most illustrative one per event type.
- **VALIDATE**: `wc -l` both files ≤200; files >100 lines have `## Contents`; Source attributions present

### Task 3: CREATE subagent reference files

- **ACTION**: Read subagent docs, distill into 2 reference files
- **READ**: `docs/subagents/creating-custom-subagents.md` (900 lines), `docs/subagents/research-subagent-best-practices.md` (1044 lines), `docs/subagents/claude-orchestrate-of-claude-code-sessions.md` (393 lines)
- **ACCELERATORS**: `docs/analysis/analysis-creating-custom-subagents.md`, `docs/analysis/analysis-research-subagent-best-practices.md`, `docs/analysis/analysis-claude-orchestrate-of-claude-code-sessions.md`
- **MIRROR**: Same pattern as Task 1
- **OUTPUT 1**: `plugins/agent-customizer/skills/create-subagent/references/subagent-authoring-guide.md` (~180 lines)
  - **Content focus**: When to use subagents vs other mechanisms (decision criteria), YAML frontmatter fields and their effects, model selection heuristics (Haiku for fast/cheap, Sonnet for balanced, Opus for complex), tool restriction strategies (`allowedTools` patterns), read-only vs read-write agent design, context isolation benefits, task decomposition patterns, common anti-patterns (too many turns, too broad tools, missing constraints)
  - **Must cite**: `subagents/research-subagent-best-practices.md`, `subagents/creating-custom-subagents.md` with line ranges
- **OUTPUT 2**: `plugins/agent-customizer/skills/create-subagent/references/subagent-config-reference.md` (~160 lines)
  - **Content focus**: Complete YAML frontmatter specification (all valid fields), model IDs and capabilities table, `maxTurns` guidelines by task type, `allowedTools` patterns (glob, explicit list), orchestration patterns (parallel, sequential, pipeline), agent communication patterns, `worktree` isolation mode, constraints (`agents cannot spawn other agents`, `no hooks or mcpServers`)
  - **Must cite**: `subagents/creating-custom-subagents.md`, `subagents/claude-orchestrate-of-claude-code-sessions.md` with line ranges
- **VALIDATE**: `wc -l` both files ≤200; Source attributions present

### Task 4: CREATE rule reference file

- **ACTION**: Read memory/rules docs, distill into 1 reference file
- **READ**: `docs/memory/how-claude-remembers-a-project.md` (361 lines)
- **ACCELERATORS**: `docs/analysis/analysis-how-claude-remembers-a-project.md`
- **ALSO READ**: `plugins/agents-initializer/skills/improve-claude/references/claude-rules-system.md` (162 lines) — the existing agents-initializer already distilled rules system content; use as reference for what's been covered but DO NOT copy content (different scope: agents-initializer's version is about CLAUDE.md generation, this version is about rule authoring)
- **MIRROR**: Same pattern as Task 1
- **OUTPUT**: `plugins/agent-customizer/skills/create-rule/references/rule-authoring-guide.md` (~160 lines)
  - **Content focus**: Rule file structure (`.claude/rules/*.md`), YAML frontmatter `paths:` array for path scoping, glob pattern syntax and examples, rule loading precedence (always-loaded vs path-scoped), when to use rules vs hooks vs skills (decision criteria), content guidelines (concise, actionable, one scope per file), line count targets (10-30 lines for scoped rules), common anti-patterns (too broad scope, too many rules, vague instructions)
  - **Must cite**: `memory/how-claude-remembers-a-project.md` with line ranges
- **VALIDATE**: `wc -l` ≤200 (≤160 target); Source attribution present

### Task 5: CREATE prompt engineering strategies reference (shared)

- **ACTION**: Read prompt engineering docs, create per-artifact-type strategy matrix
- **READ**: `docs/prompt-engineering-guide.md` (508 lines), `docs/claude-prompting-best-practices.md` (753 lines)
- **ACCELERATORS**: `docs/analysis/analysis-prompt-engineering-guide.md`, `docs/analysis/analysis-claude-prompting-best-practices.md`
- **ALSO READ**: `docs/research-llm-context-optimization.md` (567 lines) — for context-aware strategy selection
- **MIRROR**: Same reference file format as Task 1
- **OUTPUT**: `plugins/agent-customizer/skills/create-skill/references/prompt-engineering-strategies.md` (~180 lines)
  - **Content focus**:
    - **Strategy matrix table**: Rows = artifact types (skill, hook, rule, subagent), Columns = recommended techniques (XML structuring, examples, constraints, chain-of-thought, etc.)
    - **Universal principles**: Be specific over vague, use XML tags for structure, put critical instructions at start/end (lost-in-the-middle), use examples for complex patterns
    - **Per-artifact-type recommendations**:
      - Skills: Progressive disclosure phases, instruction-oriented language, conditional reference loading
      - Hooks: JSON schema precision, event-matcher specificity, exit code documentation
      - Rules: Path-scoping clarity, glob pattern documentation, one-scope-per-file
      - Subagents: Task decomposition clarity, tool restriction rationale, model selection justification
    - **Anti-patterns**: Over-prompting, contradictory instructions, vague directives, excessive examples
  - **Must cite**: `prompt-engineering-guide.md`, `claude-prompting-best-practices.md` with line ranges
  - **Also cite**: `research-llm-context-optimization.md` for context budget principles, `Evaluating-AGENTS-paper.md` for minimal-artifact evidence
- **VALIDATE**: `wc -l` ≤200; `## Contents` present (>100 lines expected); Source attributions include both primary prompt engineering docs

### Task 6: CREATE evaluation criteria files (4 files)

- **ACTION**: Create artifact-type-specific evaluation criteria for the 4 improve skills
- **MIRROR**: `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` — follow identical structure: hard limits table, bloat indicators, staleness indicators, quality assessment, scoring rubric, output template
- **GOTCHA**: The existing `evaluation-criteria.md` evaluates CLAUDE.md/AGENTS.md files. Each new evaluation criteria file evaluates a DIFFERENT artifact type. Adapt dimensions to match the artifact type being evaluated.
- **OUTPUT 1**: `plugins/agent-customizer/skills/improve-skill/references/skill-evaluation-criteria.md` (~170 lines)
  - **Hard limits**: SKILL.md length (≤500 lines for simple skills, adapt per complexity), reference files ≤200 lines, frontmatter present
  - **Bloat indicators**: Inlined reference content (should be in `references/`), redundant phase instructions, over-specified tool restrictions, hardcoded file paths
  - **Staleness indicators**: Deprecated frontmatter fields, references to removed features, outdated model names
  - **Quality dimensions**: Conciseness, progressive disclosure, evidence grounding, phase structure, frontmatter correctness, testing coverage
  - **Must cite**: `skills/skill-authoring-best-practices.md`, `Evaluating-AGENTS-paper.md` with line ranges
- **OUTPUT 2**: `plugins/agent-customizer/skills/improve-hook/references/hook-evaluation-criteria.md` (~170 lines)
  - **Hard limits**: Valid JSON schema, recognized event type, valid matcher pattern
  - **Bloat indicators**: Overly broad matchers, redundant hooks for same event, unnecessary agent-type hooks when command suffices
  - **Staleness indicators**: Deprecated event types, invalid tool names in matchers
  - **Quality dimensions**: Event selection precision, matcher specificity, error handling, security posture, exit code usage
  - **Must cite**: `hooks/claude-hook-reference-doc.md`, `hooks/automate-workflow-with-hooks.md` with line ranges
- **OUTPUT 3**: `plugins/agent-customizer/skills/improve-subagent/references/subagent-evaluation-criteria.md` (~170 lines)
  - **Hard limits**: Valid YAML frontmatter, recognized model ID, `allowedTools` present for non-trivial agents
  - **Bloat indicators**: Excessive `maxTurns`, overly broad tool access, agent instructions exceeding purpose
  - **Staleness indicators**: Deprecated model IDs, references to removed tools
  - **Quality dimensions**: Task specificity, model selection appropriateness, tool restriction, context isolation, instruction clarity
  - **Must cite**: `subagents/research-subagent-best-practices.md`, `subagents/creating-custom-subagents.md` with line ranges
- **OUTPUT 4**: `plugins/agent-customizer/skills/improve-rule/references/rule-evaluation-criteria.md` (~170 lines)
  - **Hard limits**: Valid YAML frontmatter with `paths:` array (if path-scoped), rule file ≤50 lines
  - **Bloat indicators**: Too-broad glob patterns, duplicated rules across files, vague instructions
  - **Staleness indicators**: Path globs matching no existing files, references to removed conventions
  - **Quality dimensions**: Path specificity, instruction actionability, scope separation, conciseness
  - **Must cite**: `memory/how-claude-remembers-a-project.md` with line ranges
- **VALIDATE**: `wc -l` each ≤200; each has `## Contents` (>100 lines expected); each has evaluation output template section; Source attributions present

### Task 7: CREATE validation criteria files (4 files)

- **ACTION**: Create artifact-type-specific validation criteria for all 8 skills (create and improve)
- **MIRROR**: `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md` — follow identical structure: hard limits table, quality checks, improve-specific checks, structural checks, validation loop instructions
- **OUTPUT 1**: `plugins/agent-customizer/skills/create-skill/references/skill-validation-criteria.md` (~80 lines)
  - **Hard limits**: Frontmatter present with `description`, phases defined, `${CLAUDE_SKILL_DIR}` used for file paths, references ≤200 lines
  - **Quality checks**: Progressive disclosure applied (references loaded per phase, not all at once), instruction-oriented language, no hardcoded paths, testing guidance included, no nested references within references
  - **Improve-specific**: Existing functionality preserved, phase structure not flattened, evidence citations not removed
  - **Validation loop**: Same 3-iteration max pattern
- **OUTPUT 2**: `plugins/agent-customizer/skills/create-hook/references/hook-validation-criteria.md` (~80 lines)
  - **Hard limits**: Valid JSON structure, event type from recognized list, matcher is valid glob/regex
  - **Quality checks**: Event type matches intent, matcher is specific (not `*`), error handling defined, command path valid or `prompt`/`agent` type properly configured
  - **Improve-specific**: Existing hooks not broken, matcher changes don't widen scope unintentionally
  - **Validation loop**: Same 3-iteration max pattern
- **OUTPUT 3**: `plugins/agent-customizer/skills/create-subagent/references/subagent-validation-criteria.md` (~80 lines)
  - **Hard limits**: Valid YAML frontmatter, model ID recognized, `maxTurns` ≤ 30
  - **Quality checks**: Model appropriate for task complexity, `allowedTools` restricts to needed tools, instructions are task-specific not generic, no agent-spawning instructions
  - **Improve-specific**: Tool restrictions not loosened without rationale, model not downgraded without analysis
  - **Validation loop**: Same 3-iteration max pattern
- **OUTPUT 4**: `plugins/agent-customizer/skills/create-rule/references/rule-validation-criteria.md` (~80 lines)
  - **Hard limits**: `paths:` array present if path-scoped, ≤50 lines for scoped rules, ≤30 lines for always-loaded rules
  - **Quality checks**: All instructions actionable, one scope per file, glob patterns tested against actual project structure, no overlap with existing rules
  - **Improve-specific**: Path scope not broadened without rationale, existing coverage not reduced
  - **Validation loop**: Same 3-iteration max pattern
- **VALIDATE**: `wc -l` each ≤100 (no `## Contents` needed); each has validation loop section; Source attributions present

### Task 8: DISTRIBUTE reference copies to all 8 skill directories

- **ACTION**: Copy each reference file to every skill directory that needs it
- **PREREQUISITE**: Tasks 1-7 complete (all 16 unique reference files exist)
- **IMPLEMENT**:
  1. Create all 8 reference directories: `mkdir -p plugins/agent-customizer/skills/{create-skill,create-hook,create-rule,create-subagent,improve-skill,improve-hook,improve-rule,improve-subagent}/references/`
  2. Copy authoritative files from their creation location (Tasks 1-7 outputs) to all target locations per the Distribution Matrix above
  3. For each shared file, verify byte-identity across all copies: `diff file1 file2`
- **SHARED FILE COPY MAP**:
  - `prompt-engineering-strategies.md`: create-skill → 7 other skills
  - `skill-authoring-guide.md`: create-skill → improve-skill
  - `skill-format-reference.md`: create-skill → improve-skill
  - `skill-validation-criteria.md`: create-skill → improve-skill
  - `hook-authoring-guide.md`: create-hook → improve-hook
  - `hook-events-reference.md`: create-hook → improve-hook
  - `hook-validation-criteria.md`: create-hook → improve-hook
  - `subagent-authoring-guide.md`: create-subagent → improve-subagent
  - `subagent-config-reference.md`: create-subagent → improve-subagent
  - `subagent-validation-criteria.md`: create-subagent → improve-subagent
  - `rule-authoring-guide.md`: create-rule → improve-rule
  - `rule-validation-criteria.md`: create-rule → improve-rule
- **VALIDATE**: `find plugins/agent-customizer/skills/*/references/ -name "*.md" | wc -l` = 34; for each shared filename, `diff` all copies to confirm byte-identity

### Task 9: VERIFY completeness and docs corpus coverage

- **ACTION**: Full verification pass across all reference files
- **CHECKS**:
  1. **Line count**: `wc -l` every reference file, confirm all ≤200
  2. **TOC presence**: Every file >100 lines has `## Contents` section
  3. **Source attribution**: Every file has header-level `Source:` line AND at least one inline `*Source:*` citation
  4. **Docs corpus coverage**: Verify these docs are cited by at least one reference file:
     - `skills/skill-authoring-best-practices.md` ✓ (skill-authoring-guide)
     - `skills/extend-claude-with-skills.md` ✓ (skill-authoring-guide, skill-format-reference)
     - `skills/research-claude-code-skills-format.md` ✓ (skill-format-reference)
     - `hooks/claude-hook-reference-doc.md` ✓ (hook-events-reference, hook-authoring-guide)
     - `hooks/automate-workflow-with-hooks.md` ✓ (hook-authoring-guide)
     - `subagents/creating-custom-subagents.md` ✓ (subagent-authoring-guide, subagent-config-reference)
     - `subagents/research-subagent-best-practices.md` ✓ (subagent-authoring-guide)
     - `subagents/claude-orchestrate-of-claude-code-sessions.md` ✓ (subagent-config-reference)
     - `memory/how-claude-remembers-a-project.md` ✓ (rule-authoring-guide)
     - `prompt-engineering-guide.md` ✓ (prompt-engineering-strategies)
     - `claude-prompting-best-practices.md` ✓ (prompt-engineering-strategies)
     - `research-llm-context-optimization.md` ✓ (prompt-engineering-strategies, evaluation criteria)
     - `Evaluating-AGENTS-paper.md` ✓ (evaluation criteria, prompt-engineering-strategies)
     - `a-guide-to-agents.md` ✓ (authoring guides)
     - `a-guide-to-claude.md` ✓ (authoring guides)
  5. **No nested references**: `grep -r "references/" plugins/agent-customizer/skills/*/references/` returns no imports
  6. **Byte-identity**: For each shared filename, all copies are identical
- **VALIDATE**: All 6 checks pass; create a brief verification summary

---

## Testing Strategy

### Verification Checks

| Check | Command | Expected |
|-------|---------|----------|
| File count | `find plugins/agent-customizer/skills/*/references/ -name "*.md" \| wc -l` | 34 |
| Unique files | `find plugins/agent-customizer/skills/*/references/ -name "*.md" -exec basename {} \; \| sort -u \| wc -l` | 16 |
| Max line count | `wc -l plugins/agent-customizer/skills/*/references/*.md \| sort -rn \| head -1` | ≤200 |
| TOC presence (>100 lines) | For each file >100 lines: `grep -c "## Contents"` | ≥1 |
| Source attribution | `grep -rL "^Source:" plugins/agent-customizer/skills/*/references/` | Empty (all files have Source:) |
| Inline citations | `grep -rL "\*Source:" plugins/agent-customizer/skills/*/references/` | Empty (all files have inline citations) |
| No nested refs | `grep -r "references/" plugins/agent-customizer/skills/*/references/*.md` | Empty |
| Shared file parity | `diff` each shared filename across all copies | No differences |

### Edge Cases Checklist

- [ ] Hook events reference fits within 200 lines despite 2077-line source (aggressive distillation)
- [ ] Rules reference covers path-scoping patterns despite only 361-line source (may need to draw from `claude-rules-system.md` as secondary reference)
- [ ] Evaluation criteria files follow consistent structure across 4 artifact types while having type-specific dimensions
- [ ] Prompt engineering strategies matrix is useful for all 4 artifact types without being generic
- [ ] Source citations use correct doc-relative paths (e.g., `skills/skill-authoring-best-practices.md` not `docs/skills/...`)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Check all files exist and count
find plugins/agent-customizer/skills/*/references/ -name "*.md" | wc -l
# Expected: 34

# Check no file exceeds 200 lines
wc -l plugins/agent-customizer/skills/*/references/*.md | awk '$1 > 200 {print "FAIL: " $2 " has " $1 " lines"}'
# Expected: no output

# Check TOC presence for files >100 lines
for f in $(wc -l plugins/agent-customizer/skills/*/references/*.md | awk '$1 > 100 && $2 != "total" {print $2}'); do
  grep -q "## Contents" "$f" || echo "FAIL: $f missing ## Contents"
done
# Expected: no output
```

### Level 2: SOURCE_ATTRIBUTION

```bash
# Check header-level Source: attribution
grep -rL "^Source:" plugins/agent-customizer/skills/*/references/
# Expected: empty (all files have it)

# Check inline *Source:* citations
grep -rL "\*Source:" plugins/agent-customizer/skills/*/references/
# Expected: empty (all files have it)
```

### Level 3: SHARED_FILE_PARITY

```bash
# For each shared filename, verify all copies are identical
for name in $(find plugins/agent-customizer/skills/*/references/ -name "*.md" -exec basename {} \; | sort | uniq -d); do
  files=$(find plugins/agent-customizer/skills/*/references/ -name "$name")
  first=$(echo "$files" | head -1)
  for f in $files; do
    diff -q "$first" "$f" || echo "PARITY FAIL: $name differs between copies"
  done
done
# Expected: no output
```

### Level 4: CORPUS_COVERAGE

```bash
# Verify key docs are cited (spot check)
grep -rl "skill-authoring-best-practices.md" plugins/agent-customizer/skills/*/references/ | head -1
grep -rl "claude-hook-reference-doc.md" plugins/agent-customizer/skills/*/references/ | head -1
grep -rl "creating-custom-subagents.md" plugins/agent-customizer/skills/*/references/ | head -1
grep -rl "how-claude-remembers-a-project.md" plugins/agent-customizer/skills/*/references/ | head -1
grep -rl "prompt-engineering-guide.md" plugins/agent-customizer/skills/*/references/ | head -1
# Expected: each returns at least one file path
```

---

## Acceptance Criteria

- [ ] 16 unique reference files created, all ≤200 lines
- [ ] 34 total file copies distributed across 8 skill directories
- [ ] All files >100 lines include `## Contents` table of contents
- [ ] Every file has header-level `Source:` attribution AND inline `*Source:*` citations with line ranges
- [ ] All 15 docs corpus files (excluding `plugins/`, `plans/`, `analysis/`) are cited by at least one reference file
- [ ] Shared files are byte-identical across all copies
- [ ] No nested references (no reference file imports another)
- [ ] Content is framed as instruction-oriented guidance, not executable scripts
- [ ] Reference file format mirrors existing `agents-initializer` patterns exactly (title block, separator, TOC, sections, citations)

---

## Completion Checklist

- [ ] Task 1: Skill reference files created (2 unique)
- [ ] Task 2: Hook reference files created (2 unique)
- [ ] Task 3: Subagent reference files created (2 unique)
- [ ] Task 4: Rule reference file created (1 unique)
- [ ] Task 5: Prompt engineering strategies created (1 unique, shared)
- [ ] Task 6: Evaluation criteria created (4 unique)
- [ ] Task 7: Validation criteria created (4 unique)
- [ ] Task 8: All copies distributed (34 total files)
- [ ] Task 9: Completeness verified (all checks pass)
- [ ] Level 1 validation: static analysis passes
- [ ] Level 2 validation: source attribution passes
- [ ] Level 3 validation: shared file parity passes
- [ ] Level 4 validation: corpus coverage passes

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hook events reference (2077 lines → 200 lines) loses critical event details | HIGH | MEDIUM | Focus on reference table + JSON schema + 3 most common patterns; defer edge cases to the source doc which skills can read on demand |
| Analysis files in Portuguese introduce translation inconsistencies | LOW | LOW | Use analysis files only as accelerators; always verify against English primary source before citing |
| Phase 3 creates directories that conflict with Phase 2 directory creation | LOW | LOW | Both use `mkdir -p` (idempotent); directories merge cleanly |
| Reference file rule doesn't scope to `plugins/agent-customizer/` yet | MEDIUM | LOW | Files will conform to the rule format regardless; Phase 3 updates the rule paths — no functional impact until then |
| Distillation loses nuance needed for improve skills to evaluate artifacts | MEDIUM | MEDIUM | Evaluation criteria files include explicit scoring rubric with type-specific dimensions; link to source doc + line range for deep dives |

---

## Notes

- **Phase 3 dependency note**: Phase 3 (Plugin Scaffold & Infrastructure) will update `.claude/rules/reference-files.md` to add `plugins/agent-customizer/skills/*/references/*.md` to the `paths:` array. Until then, the rule won't auto-trigger on new reference files. Phase 2 files must still conform to all 7 rule constraints proactively.

- **Standalone distribution**: Phase 9 will create standalone copies of these reference files at `skills/*/references/`. Additionally, Phase 9 will create standalone-specific agent-replacement references (e.g., `artifact-analyzer.md`) following the same pattern as `agents-initializer`'s `codebase-analyzer.md`, `scope-detector.md`, and `file-evaluator.md` standalone references.

- **Analysis files as accelerators**: The 16 `docs/analysis/` files (in Portuguese) contain pre-synthesized tables, key patterns, and critical insights already extracted from primary sources. The implementation agent should read the analysis file FIRST for each artifact type to build a mental model, then read the primary source to extract specific line ranges for citations. This approach significantly speeds distillation.

- **Naming convention**: Reference files use `{artifact-type}-{purpose}.md` naming (e.g., `skill-authoring-guide.md`, `hook-events-reference.md`). This differs from `agents-initializer` which uses topic-based naming (e.g., `progressive-disclosure-guide.md`, `context-optimization.md`). The artifact-type prefix makes each file's scope immediately clear and avoids namespace collisions with `agents-initializer` references.
