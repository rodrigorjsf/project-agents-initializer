# Phase 9: Standalone Distribution

## Metadata

| Field | Value |
|-------|-------|
| PRD | `.claude/PRPs/prds/agent-customizer-plugin.prd.md` — Phase 9 |
| GitHub Issue | #54 |
| Parent Issue | #29 |
| Branch | `feature/phase-9-standalone-distribution` |
| Status | in-progress |
| Complexity | MEDIUM |

---

## User Story

As a developer using any AI coding tool (not just Claude Code),
I want to install the `create-skill`, `create-hook`, `create-rule`, `create-subagent`, `improve-skill`, `improve-hook`, `improve-rule`, and `improve-subagent` skills via `npx skills add`,
So that I can author and optimize agent artifacts without needing Claude Code's plugin infrastructure.

---

## UX Transformation

### Before

```
Developer (non-Claude-Code user)
    → npx skills add
    → agent-customizer skills NOT available
    → must manually read docs corpus to create/improve artifacts
```

```
Claude Code plugin user
    → installs agent-engineering-toolkit
    → uses agent-customizer:create-skill, etc.
    → subagent delegates analysis (isolated context)
```

### After

```
Developer (any AI tool)
    → npx skills add create-skill  (or improve-skill, etc.)
    → invokes skill → inline analysis via references/artifact-analyzer.md
    → same 4-5 phase workflow, same output quality
    → no plugin infrastructure required
```

```
Claude Code plugin user (unchanged)
    → agent-customizer:create-skill still uses subagent delegation
    → no regression in plugin behavior
```

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `skills/` directory | 4 skills (init/improve-agents/claude) | 12 skills (+8 new) | Full artifact creation coverage for any AI tool |
| Phase 1 analysis | Delegated to registered agent | Inline reference reading | Same output, no Task tool required |
| Phase 1 evaluate (improve-*) | Delegated to type-specific evaluator | Inline evaluator reference reading | Same quality checks, no agent context required |
| Hooks/subagents in suggestions | Plugin: suggest any mechanism | Standalone: suggest only skills + rules | Respects standalone constraints |

---

## Architecture Decision

**Approach**: Mirror each plugin SKILL.md exactly, replacing only:

1. `"Delegate to the [agent] agent..."` blocks → `"Read ${CLAUDE_SKILL_DIR}/references/[agent].md and follow its [purpose] instructions..."`
2. `"subagent-driven"` in description → `"inline"`
3. Add standalone hooks/subagents exclusion note to improve-* Phase 3

**Reference file strategy**: Convert each agent's system prompt (Constraints + Process + Output Format + Self-Verification) into a `references/` document following the `codebase-analyzer.md` pattern:

- Remove YAML frontmatter
- Add title block with `Source: agents/{agent-name}.md`
- Replace "You are a..." with "Follow these ... instructions."
- Add `## Contents` TOC (required for files over 100 lines per `reference-files.md`)
- Each agent is 124-129 lines → converted refs ≈ 120-130 lines (under 200 limit)

**Not building**:

- New reference file content (copy all existing plugin references verbatim)
- New asset templates (copy from plugin verbatim)
- Plugin skill changes (leave plugin skills untouched)
- Cursor plugin standalone (different plugin, separate scope)
- Docs-drift-checker standalone reference (not invoked by any runtime skill)

---

## Discovered Patterns

### P1 — Standalone inline analysis invocation

Source: `skills/init-agents/SKILL.md:44`

```markdown
Read `${CLAUDE_SKILL_DIR}/references/codebase-analyzer.md` and follow its codebase
analysis instructions to analyze the project at the current working directory.

Focus: Return ONLY non-standard, non-obvious information...
```

### P2 — Standalone evaluator invocation with two-step read

Source: `skills/improve-agents/SKILL.md:34-36`

```markdown
Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the complete scoring rubric...
Read `${CLAUDE_SKILL_DIR}/references/file-evaluator.md` and follow its evaluation instructions
to evaluate all AGENTS.md files in the project...
```

### P3 — Converted reference file format

Source: `skills/init-agents/references/codebase-analyzer.md:1-8`

```markdown
# Codebase Analysis Instructions

Structured process for detecting project tech stack, tooling, and non-standard patterns.
Used by INIT and IMPROVE skills for codebase analysis. Source: agents/codebase-analyzer.md

---

Follow these codebase analysis instructions. Analyze the project at the current working directory...
```

### P4 — Standalone hooks/subagents exclusion

Source: `skills/improve-agents/SKILL.md:88`

```markdown
This is the standalone distribution — suggest only skills and path-scoped rules. Do not suggest
hooks or subagents (these require Claude Code). When automation-migration-guide.md references
hooks or subagents, substitute with the closest available mechanism.
```

### P5 — Plugin Phase 1 delegation pattern (to replace)

Source: `plugins/agent-customizer/skills/create-skill/SKILL.md:41-45`

```markdown
Delegate to the `artifact-analyzer` agent with this task:

> Analyze the project to understand existing skills, naming conventions...

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context.
Wait for it to complete and parse its structured output.
```

### P6 — Plugin improve Phase 1 evaluator delegation (to replace)

Source: `plugins/agent-customizer/skills/improve-skill/SKILL.md:42-46`

```markdown
Delegate to the `skill-evaluator` agent with this task:

> Evaluate the skill at `{target-path}`. Read the SKILL.md and all files in the skill directory.
> Check hard limits...

The agent runs on Sonnet with read-only tools. Wait for it to complete and parse its structured output.
```

---

## Reference Files Inventory

### Files to copy verbatim from plugin (per skill)

| Plugin Skill | Reference Files to Copy |
|--------------|------------------------|
| `create-skill` | `skill-authoring-guide.md`, `skill-format-reference.md`, `skill-validation-criteria.md`, `prompt-engineering-strategies.md` |
| `create-hook` | `hook-authoring-guide.md`, `hook-events-reference.md`, `hook-validation-criteria.md`, `prompt-engineering-strategies.md` |
| `create-rule` | `rule-authoring-guide.md`, `rule-validation-criteria.md`, `prompt-engineering-strategies.md` |
| `create-subagent` | `subagent-authoring-guide.md`, `subagent-config-reference.md`, `subagent-validation-criteria.md`, `prompt-engineering-strategies.md` |
| `improve-skill` | `skill-authoring-guide.md`, `skill-evaluation-criteria.md`, `skill-format-reference.md`, `skill-validation-criteria.md`, `prompt-engineering-strategies.md` |
| `improve-hook` | `hook-authoring-guide.md`, `hook-evaluation-criteria.md`, `hook-events-reference.md`, `hook-validation-criteria.md`, `prompt-engineering-strategies.md` |
| `improve-rule` | `rule-authoring-guide.md`, `rule-evaluation-criteria.md`, `rule-validation-criteria.md`, `prompt-engineering-strategies.md` |
| `improve-subagent` | `subagent-authoring-guide.md`, `subagent-config-reference.md`, `subagent-evaluation-criteria.md`, `subagent-validation-criteria.md`, `prompt-engineering-strategies.md` |

### New reference files to create (converted from agents)

| New File | Source Agent | Used By |
|----------|-------------|---------|
| `references/artifact-analyzer.md` | `plugins/agent-customizer/agents/artifact-analyzer.md` | All 8 standalone skills (bundled per skill) |
| `references/skill-evaluator.md` | `plugins/agent-customizer/agents/skill-evaluator.md` | `skills/improve-skill/` only |
| `references/hook-evaluator.md` | `plugins/agent-customizer/agents/hook-evaluator.md` | `skills/improve-hook/` only |
| `references/rule-evaluator.md` | `plugins/agent-customizer/agents/rule-evaluator.md` | `skills/improve-rule/` only |
| `references/subagent-evaluator.md` | `plugins/agent-customizer/agents/subagent-evaluator.md` | `skills/improve-subagent/` only |

### Asset templates to copy verbatim from plugin (per skill)

| Plugin Skill | Template to Copy |
|--------------|-----------------|
| `create-skill` | `assets/templates/skill-md.md` |
| `create-hook` | `assets/templates/hook-config.md` |
| `create-rule` | `assets/templates/rule-file.md` |
| `create-subagent` | `assets/templates/subagent-definition.md` |
| `improve-skill` | `assets/templates/skill-md.md` |
| `improve-hook` | `assets/templates/hook-config.md` |
| `improve-rule` | `assets/templates/rule-file.md` |
| `improve-subagent` | `assets/templates/subagent-definition.md` |

---

## SKILL.md Conversion Specification

### Description field changes

| Skill | Plugin Description | Standalone Change |
|-------|-------------------|------------------|
| `create-skill` | "Uses subagent-driven codebase analysis and evidence-based guidance. Use when creating a new Claude Code skill from scratch." | Replace "subagent-driven" → "inline"; "Claude Code skill" → "skill" |
| `create-hook` | "Uses subagent-driven codebase analysis." | Replace "subagent-driven" → "inline" |
| `create-rule` | "Uses subagent-driven codebase analysis." | Replace "subagent-driven" → "inline" |
| `create-subagent` | "Uses subagent-driven codebase analysis." | Replace "subagent-driven" → "inline" |
| `improve-skill` | No "subagent-driven" mention | No change needed |
| `improve-hook` | No "subagent-driven" mention | No change needed |
| `improve-rule` | No "subagent-driven" mention | No change needed |
| `improve-subagent` | No "subagent-driven" mention | No change needed |

### Phase 1 replacement (create-* skills)

Replace (for each create-* skill):

```markdown
Delegate to the `artifact-analyzer` agent with this task:

> [task description including focus areas]

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context. Wait for it to complete and parse its structured output.
```

With:

```markdown
Read `${CLAUDE_SKILL_DIR}/references/artifact-analyzer.md` and follow its analysis instructions to analyze the project at the current working directory.

Focus on: [same focus areas as were in the agent task description]
```

**Per-skill focus areas** (copy from plugin SKILL.md task description):

- `create-skill`: existing skill directory structure, naming patterns, which skills delegate to agents, plugin conventions in CLAUDE.md files, and any skill that is similar to `{requested-name}` in purpose
- `create-hook`: existing hook configurations in `.claude/settings.json`, `.claude/settings.local.json`, `hooks/hooks.json`; hook scripts in `.claude/hooks/` and `scripts/`; event types currently covered and gaps; also read `CLAUDE.md` and README files for tooling conventions
- `create-rule`: all `.claude/rules/` files and their path scopes; detect overlapping globs, naming conventions, and any conventions already documented in `CLAUDE.md` that would be redundant in a new rule
- `create-subagent`: all agents in `.claude/agents/` and `plugins/*/agents/`; their tool restrictions, model choices, `maxTurns` values; which skills delegate to which agents; naming conventions used for existing agents

### Phase 1 replacement (improve-* skills — evaluator phase)

Replace evaluator delegation with:

```markdown
Read `${CLAUDE_SKILL_DIR}/references/{type}-evaluator.md` and follow its evaluation instructions to evaluate the {artifact} at `{target-path}`. Check hard limits, structural quality, and token efficiency. Return structured evaluation results with severity classifications (AUTO-FAIL/HIGH/MEDIUM/LOW).
```

**Per-skill replacements**:

- `improve-skill`: `skill-evaluator.md`, evaluate the skill at `{target-path}`. Hard limits: body ≤500 lines, references ≤200 lines, frontmatter valid. Check structural quality (progressive disclosure, phase structure, reference loading) and token efficiency.
- `improve-hook`: `hook-evaluator.md`, evaluate the hook configuration at `{target-path}`. Hard limits: JSON validity, valid event names, handler types, script existence, exit code behavior. Check event intent matching, matcher specificity, error handling, no hardcoded secrets.
- `improve-rule`: `rule-evaluator.md`, evaluate the rule file at `{target-path}`. Hard limits: ≤50 lines, valid YAML frontmatter, `paths:` required, no contradictions. Check actionability, one scope per file, no obvious conventions.
- `improve-subagent`: `subagent-evaluator.md`, evaluate the subagent definition at `{target-path}`. Hard limits: valid YAML, `name` lowercase+hyphens, `description` present, `model` recognized, `maxTurns` ≤30, non-empty system prompt. Check description routing specificity, appropriate model, minimum-necessary tools.

### Phase 2 replacement (improve-* skills — context phase)

Replace artifact-analyzer delegation with:

```markdown
Read `${CLAUDE_SKILL_DIR}/references/artifact-analyzer.md` and follow its analysis instructions.

Focus on: [same focus areas from the plugin Phase 2 task description]
```

**Per-skill focus areas for Phase 2**:

- `improve-skill`: which agents the skill delegates to and whether those agents still exist, naming conventions for similar skills, any other skills that overlap in purpose, and the plugin structure
- `improve-hook`: all hook definitions and scripts, event coverage gaps, matcher patterns already in use
- `improve-rule`: all rule files and topics, glob pattern staleness (do globs still match files), CLAUDE.md overlaps
- `improve-subagent`: all agents and their roles, which skills delegate to which agents, tool restrictions, model choices, agents with similar purposes, naming conventions

### Phase 3 standalone note (improve-* skills only)

In Phase 3 (Generate Improvement Plan), after the last bullet in the improvement categories list, add:

```markdown
**Standalone constraint**: This is the standalone distribution — suggest only skills and path-scoped rules as improvement targets. Do not suggest creating hooks or subagents (these require Claude Code plugin infrastructure). When evaluation criteria mention hooks or subagents as improvement mechanisms, substitute with the closest available mechanism (a rule for path-scoped enforcement, a skill for workflow guidance).
```

---

## Converted Agent Reference File Specification

### `references/artifact-analyzer.md` — conversion from `agents/artifact-analyzer.md`

Source: `plugins/agent-customizer/agents/artifact-analyzer.md` (126 lines)

Conversion steps:

1. Remove YAML frontmatter (lines 1-7)
2. Replace title line (`# Artifact Analyzer`) with: `# Artifact Analysis Instructions`
3. After title, add: `Structured process for inventorying existing Claude Code artifacts and conventions.\nUsed by CREATE and IMPROVE skills for codebase context analysis. Source: agents/artifact-analyzer.md`
4. Add `---` separator
5. Replace opening paragraph `"You are a codebase artifact analysis specialist. Analyze the project..."` with: `"Follow these analysis instructions. Analyze the project at the current working directory and return a structured summary of its existing Claude Code artifacts and conventions."`
6. Add `## Contents` TOC (required since >100 lines): Constraints, Process (5 steps), Output Format, Self-Verification
7. Keep all other sections verbatim (Constraints, Process steps 1-5, Output Format, Self-Verification)
8. Final line count target: ~125 lines (within 200 limit)

Validate: `wc -l skills/create-skill/references/artifact-analyzer.md` → should be ≤200

### `references/skill-evaluator.md` — conversion from `agents/skill-evaluator.md`

Source: `plugins/agent-customizer/agents/skill-evaluator.md` (126 lines)

Conversion steps:

1. Remove YAML frontmatter (lines 1-7)
2. Replace title with: `# Skill Evaluation Instructions`
3. Add subtitle: `Structured process for evaluating SKILL.md files against evidence-based quality criteria.\nUsed by IMPROVE-SKILL skill for current state analysis. Source: agents/skill-evaluator.md`
4. Add `---` separator
5. Replace `"You are a skill quality assessment specialist."` with: `"Follow these evaluation instructions. Analyze the target SKILL.md file and evaluate it against evidence-based criteria."`
6. Add `## Contents` TOC: Constraints, Quality Criteria (Hard Limits, Quality Checks), Process, Output Format, Self-Verification
7. Keep all other sections verbatim
8. Final line count target: ~125 lines

### `references/hook-evaluator.md` — conversion from `agents/hook-evaluator.md`

Source: `plugins/agent-customizer/agents/hook-evaluator.md` (125 lines)

Same conversion pattern: remove frontmatter, replace title with `# Hook Evaluation Instructions`, add subtitle with `Source: agents/hook-evaluator.md`, replace "You are a..." with "Follow these evaluation instructions.", add `## Contents` TOC, keep rest verbatim. Target: ~124 lines.

### `references/rule-evaluator.md` — conversion from `agents/rule-evaluator.md`

Source: `plugins/agent-customizer/agents/rule-evaluator.md` (129 lines)

Same conversion pattern. Title: `# Rule Evaluation Instructions`. Source: `agents/rule-evaluator.md`. Target: ~128 lines.

### `references/subagent-evaluator.md` — conversion from `agents/subagent-evaluator.md`

Source: `plugins/agent-customizer/agents/subagent-evaluator.md` (124 lines)

Same conversion pattern. Title: `# Subagent Evaluation Instructions`. Source: `agents/subagent-evaluator.md`. Target: ~123 lines.

---

## Rule Update Specification

### File: `.claude/rules/standalone-skills.md`

Current line 8:

```markdown
- Never reference `codebase-analyzer`, `scope-detector`, or `file-evaluator` agents
```

Updated line 8 (add agent-customizer agent names):

```markdown
- Never reference `codebase-analyzer`, `scope-detector`, `file-evaluator`, `artifact-analyzer`, `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, or `subagent-evaluator` agents
```

No other changes to standalone-skills.md needed — the existing rule `No Task tool, no agent delegation — skills must work with any AI coding tool` (line 9) already enforces the constraint for all new agents.

---

## Implementation Tasks

> Tasks in the same parallel group can run concurrently.

### Task 0 — Branch setup

```bash
git checkout -b feature/phase-9-standalone-distribution
```

Validation: `git branch --show-current` → `feature/phase-9-standalone-distribution`

---

### Task Group A — Create converted agent reference docs (sequential, all other tasks depend on these)

> These define the content once; tasks B and C bundle copies per skill.

**A1 — Create `artifact-analyzer.md` reference template**

Read `plugins/agent-customizer/agents/artifact-analyzer.md` (full content).
Create `skills/.standalone-references/artifact-analyzer.md` as a staging file following the conversion specification above. This file will be copied into each skill's `references/` directory in Tasks B and C.

Validation:

```bash
wc -l skills/.standalone-references/artifact-analyzer.md   # must be ≤ 200
head -5 skills/.standalone-references/artifact-analyzer.md  # must start with "# Artifact Analysis Instructions"
grep -c "Follow these analysis instructions" skills/.standalone-references/artifact-analyzer.md  # must be 1
grep -c "## Contents" skills/.standalone-references/artifact-analyzer.md  # must be 1 (required for >100 lines)
```

**A2 — Create `skill-evaluator.md` reference**

Read `plugins/agent-customizer/agents/skill-evaluator.md` (full content).
Create `skills/.standalone-references/skill-evaluator.md` following conversion specification.

Validation:

```bash
wc -l skills/.standalone-references/skill-evaluator.md   # ≤ 200
grep "Follow these evaluation instructions" skills/.standalone-references/skill-evaluator.md  # must exist
grep "## Contents" skills/.standalone-references/skill-evaluator.md  # must exist
```

**A3 — Create `hook-evaluator.md` reference**

Read `plugins/agent-customizer/agents/hook-evaluator.md` (full content).
Create `skills/.standalone-references/hook-evaluator.md` following conversion specification.

Validation: same pattern as A2 (`hook-evaluator.md`).

**A4 — Create `rule-evaluator.md` reference**

Read `plugins/agent-customizer/agents/rule-evaluator.md` (full content).
Create `skills/.standalone-references/rule-evaluator.md` following conversion specification.

Validation: same pattern as A2 (`rule-evaluator.md`).

**A5 — Create `subagent-evaluator.md` reference**

Read `plugins/agent-customizer/agents/subagent-evaluator.md` (full content).
Create `skills/.standalone-references/subagent-evaluator.md` following conversion specification.

Validation: same pattern as A2 (`subagent-evaluator.md`).

---

### Task Group B — Create standalone `create-*` skills (parallel, all depend on A1)

**B1 — Create `skills/create-skill/`**

Files to create:

1. `skills/create-skill/SKILL.md` — adapt from `plugins/agent-customizer/skills/create-skill/SKILL.md`:
   - Change `description` field: replace `"subagent-driven codebase analysis"` → `"inline codebase analysis"`; replace `"new Claude Code skill from scratch"` → `"new skill from scratch"`
   - Replace Phase 1 delegation block (lines 41-45) with inline reference read using focus area: `"existing skill directory structure, naming patterns, which skills delegate to agents, plugin conventions in CLAUDE.md files, and any skill that is similar to {requested-name} in purpose"`
   - All other phases: copy verbatim
2. `skills/create-skill/references/skill-authoring-guide.md` — copy from `plugins/agent-customizer/skills/create-skill/references/skill-authoring-guide.md`
3. `skills/create-skill/references/skill-format-reference.md` — copy from plugin
4. `skills/create-skill/references/skill-validation-criteria.md` — copy from plugin
5. `skills/create-skill/references/prompt-engineering-strategies.md` — copy from plugin
6. `skills/create-skill/references/artifact-analyzer.md` — copy from `skills/.standalone-references/artifact-analyzer.md`
7. `skills/create-skill/assets/templates/skill-md.md` — copy from `plugins/agent-customizer/skills/create-skill/assets/templates/skill-md.md`

Validation:

```bash
# No agent delegation references
grep -n "Delegate to" skills/create-skill/SKILL.md  # must return empty
grep -n "artifact-analyzer agent" skills/create-skill/SKILL.md  # must return empty
# Has inline reference read
grep -n "references/artifact-analyzer.md" skills/create-skill/SKILL.md  # must return 1 match
# Size limits
wc -l skills/create-skill/SKILL.md  # ≤ 500
for f in skills/create-skill/references/*.md; do echo "$f: $(wc -l < $f)"; done  # all ≤ 200
# Structure
ls skills/create-skill/references/  # must list 5 files
ls skills/create-skill/assets/templates/  # must list skill-md.md
```

**B2 — Create `skills/create-hook/`**

Files to create:

1. `skills/create-hook/SKILL.md` — adapt from `plugins/agent-customizer/skills/create-hook/SKILL.md`:
   - Change `description` field: replace `"subagent-driven"` → `"inline"`
   - Replace Phase 1 delegation block with inline reference read using focus area: `"existing hook configurations in .claude/settings.json, .claude/settings.local.json, hooks/hooks.json; hook scripts in .claude/hooks/ and scripts/; event types currently covered and gaps; also read CLAUDE.md and README files for tooling conventions"`
   - All other phases: copy verbatim
2. `references/hook-authoring-guide.md` — copy from plugin
3. `references/hook-events-reference.md` — copy from plugin
4. `references/hook-validation-criteria.md` — copy from plugin
5. `references/prompt-engineering-strategies.md` — copy from plugin
6. `references/artifact-analyzer.md` — copy from `skills/.standalone-references/artifact-analyzer.md`
7. `assets/templates/hook-config.md` — copy from plugin

Validation: same structure checks as B1 (adapted to hook names). Verify no delegation blocks in SKILL.md.

**B3 — Create `skills/create-rule/`**

Files to create:

1. `skills/create-rule/SKILL.md` — adapt from `plugins/agent-customizer/skills/create-rule/SKILL.md`:
   - Change `description` field: replace `"subagent-driven"` → `"inline"`
   - Replace Phase 1 delegation block with inline reference read using focus area: `"all .claude/rules/ files and their path scopes; detect overlapping globs, naming conventions, and any conventions already documented in CLAUDE.md that would be redundant in a new rule"`
   - All other phases: copy verbatim
2. `references/rule-authoring-guide.md` — copy from plugin
3. `references/rule-validation-criteria.md` — copy from plugin
4. `references/prompt-engineering-strategies.md` — copy from plugin
5. `references/artifact-analyzer.md` — copy from staging
6. `assets/templates/rule-file.md` — copy from plugin

Validation: same checks as B1 (adapted to rule names). 4 reference files (fewer than create-skill).

**B4 — Create `skills/create-subagent/`**

Files to create:

1. `skills/create-subagent/SKILL.md` — adapt from `plugins/agent-customizer/skills/create-subagent/SKILL.md`:
   - Change `description` field: replace `"subagent-driven"` → `"inline"`
   - Replace Phase 1 delegation block with inline reference read using focus area: `"all agents in .claude/agents/ and plugins/*/agents/; their tool restrictions, model choices, maxTurns values; which skills delegate to which agents; naming conventions used for existing agents"`
   - All other phases: copy verbatim
2. `references/subagent-authoring-guide.md` — copy from plugin
3. `references/subagent-config-reference.md` — copy from plugin
4. `references/subagent-validation-criteria.md` — copy from plugin
5. `references/prompt-engineering-strategies.md` — copy from plugin
6. `references/artifact-analyzer.md` — copy from staging
7. `assets/templates/subagent-definition.md` — copy from plugin

Validation: same checks as B1 (adapted to subagent names). 5 reference files.

---

### Task Group C — Create standalone `improve-*` skills (parallel, depend on A1+A2-A5)

**C1 — Create `skills/improve-skill/`**

Files to create:

1. `skills/improve-skill/SKILL.md` — adapt from `plugins/agent-customizer/skills/improve-skill/SKILL.md`:
   - `description` field: no change needed (no "subagent-driven" mention)
   - Replace Phase 1 evaluator delegation (lines 42-46) with: inline `skill-evaluator.md` read (see Phase 1 replacement spec)
   - Replace Phase 2 artifact-analyzer delegation (lines 50-54) with: inline `artifact-analyzer.md` read, focus on: `"which agents the skill delegates to and whether those agents still exist, naming conventions for similar skills, any other skills that overlap in purpose, and the plugin structure"`
   - Add standalone constraint note at end of Phase 3 (see Phase 3 spec)
   - All other phases: copy verbatim
2. `references/skill-authoring-guide.md` — copy from plugin
3. `references/skill-evaluation-criteria.md` — copy from plugin
4. `references/skill-format-reference.md` — copy from plugin
5. `references/skill-validation-criteria.md` — copy from plugin
6. `references/prompt-engineering-strategies.md` — copy from plugin
7. `references/skill-evaluator.md` — copy from `skills/.standalone-references/skill-evaluator.md`
8. `references/artifact-analyzer.md` — copy from `skills/.standalone-references/artifact-analyzer.md`
9. `assets/templates/skill-md.md` — copy from plugin

Validation:

```bash
# No delegation blocks
grep -n "Delegate to" skills/improve-skill/SKILL.md  # must return empty
grep -n "skill-evaluator agent" skills/improve-skill/SKILL.md  # must return empty
# Has both inline reads
grep -n "references/skill-evaluator.md" skills/improve-skill/SKILL.md  # 1 match
grep -n "references/artifact-analyzer.md" skills/improve-skill/SKILL.md  # 1 match
# Has standalone constraint note
grep -n "standalone distribution" skills/improve-skill/SKILL.md  # 1 match
# Size limits
wc -l skills/improve-skill/SKILL.md  # ≤ 500
for f in skills/improve-skill/references/*.md; do echo "$f: $(wc -l < $f)"; done  # all ≤ 200
# Structure: 7 reference files + 1 template
ls skills/improve-skill/references/ | wc -l  # must be 7
ls skills/improve-skill/assets/templates/  # must list skill-md.md
```

**C2 — Create `skills/improve-hook/`**

Files to create:

1. `skills/improve-hook/SKILL.md` — adapt from `plugins/agent-customizer/skills/improve-hook/SKILL.md`:
   - Replace Phase 1 hook-evaluator delegation with inline `hook-evaluator.md` read (see Phase 1 replacement spec)
   - Replace Phase 2 artifact-analyzer delegation with inline `artifact-analyzer.md` read, focus on: `"all hook definitions and scripts, event coverage gaps, matcher patterns already in use"`
   - Add standalone constraint note at end of Phase 3
   - All other phases: copy verbatim
2. `references/hook-authoring-guide.md` — copy from plugin
3. `references/hook-evaluation-criteria.md` — copy from plugin
4. `references/hook-events-reference.md` — copy from plugin
5. `references/hook-validation-criteria.md` — copy from plugin
6. `references/prompt-engineering-strategies.md` — copy from plugin
7. `references/hook-evaluator.md` — copy from `skills/.standalone-references/hook-evaluator.md`
8. `references/artifact-analyzer.md` — copy from staging
9. `assets/templates/hook-config.md` — copy from plugin

Validation: same pattern as C1 (adapted to hook names). 7 reference files.

**C3 — Create `skills/improve-rule/`**

Files to create:

1. `skills/improve-rule/SKILL.md` — adapt from `plugins/agent-customizer/skills/improve-rule/SKILL.md`:
   - Replace Phase 1 rule-evaluator delegation with inline `rule-evaluator.md` read
   - Replace Phase 2 artifact-analyzer delegation with inline `artifact-analyzer.md` read, focus on: `"all rule files and topics, glob pattern staleness (do globs still match files), CLAUDE.md overlaps"`
   - Add standalone constraint note at end of Phase 3
   - All other phases: copy verbatim
2. `references/rule-authoring-guide.md` — copy from plugin
3. `references/rule-evaluation-criteria.md` — copy from plugin
4. `references/rule-validation-criteria.md` — copy from plugin
5. `references/prompt-engineering-strategies.md` — copy from plugin
6. `references/rule-evaluator.md` — copy from staging
7. `references/artifact-analyzer.md` — copy from staging
8. `assets/templates/rule-file.md` — copy from plugin

Validation: same pattern. 6 reference files.

**C4 — Create `skills/improve-subagent/`**

Files to create:

1. `skills/improve-subagent/SKILL.md` — adapt from `plugins/agent-customizer/skills/improve-subagent/SKILL.md`:
   - Replace Phase 1 subagent-evaluator delegation with inline `subagent-evaluator.md` read
   - Replace Phase 2 artifact-analyzer delegation with inline `artifact-analyzer.md` read, focus on: `"all agents and their roles, which skills delegate to which agents, tool restrictions, model choices, agents with similar purposes, naming conventions"`
   - Add standalone constraint note at end of Phase 3
   - All other phases: copy verbatim
2. `references/subagent-authoring-guide.md` — copy from plugin
3. `references/subagent-config-reference.md` — copy from plugin
4. `references/subagent-evaluation-criteria.md` — copy from plugin
5. `references/subagent-validation-criteria.md` — copy from plugin
6. `references/prompt-engineering-strategies.md` — copy from plugin
7. `references/subagent-evaluator.md` — copy from staging
8. `references/artifact-analyzer.md` — copy from staging
9. `assets/templates/subagent-definition.md` — copy from plugin

Validation: same pattern. 7 reference files.

---

### Task D — Update `standalone-skills.md` rule (independent, can run any time)

Update `.claude/rules/standalone-skills.md` line 8:

Old:

```markdown
- Never reference `codebase-analyzer`, `scope-detector`, or `file-evaluator` agents
```

New:

```markdown
- Never reference `codebase-analyzer`, `scope-detector`, `file-evaluator`, `artifact-analyzer`, `skill-evaluator`, `hook-evaluator`, `rule-evaluator`, or `subagent-evaluator` agents
```

Validation:

```bash
grep -n "artifact-analyzer" .claude/rules/standalone-skills.md  # must return match on line 8
grep -n "subagent-evaluator" .claude/rules/standalone-skills.md  # must return match on line 8
```

---

### Task E — Clean up staging directory

After all skill directories are created, remove the staging directory:

```bash
rm -rf skills/.standalone-references/
```

Validation:

```bash
ls skills/  # .standalone-references must NOT appear
```

---

### Task F — Parity verification (runs after B and C groups complete)

Verify structural parity between plugin and standalone skills:

```bash
# Verify all 8 standalone skills exist
for skill in create-skill create-hook create-rule create-subagent improve-skill improve-hook improve-rule improve-subagent; do
  echo "=== $skill ==="
  ls skills/$skill/references/
  ls skills/$skill/assets/templates/
done

# Verify no agent delegation in any standalone SKILL.md
grep -rn "Delegate to" skills/*/SKILL.md  # must return empty

# Verify all standalone SKILL.md files use ${CLAUDE_SKILL_DIR}
for skill in create-skill create-hook create-rule create-subagent improve-skill improve-hook improve-rule improve-subagent; do
  grep -c "CLAUDE_SKILL_DIR" skills/$skill/SKILL.md
done  # each must be > 0

# Verify all reference files under 200 lines
for f in skills/*/references/*.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 200 ]; then echo "OVER LIMIT: $f ($lines lines)"; fi
done

# Verify all SKILL.md files under 500 lines
for f in skills/*/SKILL.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 500 ]; then echo "OVER LIMIT: $f ($lines lines)"; fi
done

# Verify standalone constraint note in all improve-* skills
for skill in improve-skill improve-hook improve-rule improve-subagent; do
  grep -c "standalone distribution" skills/$skill/SKILL.md
done  # each must be 1

# Verify converted references have Contents TOC (required for >100 lines)
for skill in create-skill create-hook create-rule create-subagent improve-skill improve-hook improve-rule improve-subagent; do
  lines=$(wc -l < "skills/$skill/references/artifact-analyzer.md")
  if [ "$lines" -gt 100 ]; then
    grep -c "## Contents" skills/$skill/references/artifact-analyzer.md
  fi
done  # each must be ≥ 1

# Verify improve-* skills have evaluator references
for skill in improve-skill improve-hook improve-rule improve-subagent; do
  type=$(echo $skill | sed 's/improve-//')
  ls skills/$skill/references/${type}-evaluator.md  # must exist
done
```

---

### Task G — Update PRD (runs after Task F)

Update `.claude/PRPs/prds/agent-customizer-plugin.prd.md` Phase 9 row:

- Change `Status: pending` → `Status: in-progress`
- Set `PRP Plan` column: `.claude/PRPs/plans/standalone-distribution.plan.md`

```bash
grep -n "Standalone Distribution" .claude/PRPs/prds/agent-customizer-plugin.prd.md  # verify row exists
```

---

## File Scope Summary

| Action | Count | Files |
|--------|-------|-------|
| CREATE (SKILL.md) | 8 | `skills/{skill}/SKILL.md` ×8 |
| CREATE (artifact-analyzer.md) | 8 | Bundled in each skill's `references/` |
| CREATE (type-specific evaluators) | 4 | Bundled in each `improve-*` skill's `references/` |
| COPY (plugin reference files) | 35 | Per-skill reference copies (≠ shared symlinks) |
| COPY (template files) | 8 | Per-skill `assets/templates/` copies |
| UPDATE | 1 | `.claude/rules/standalone-skills.md` (line 8) |
| UPDATE | 1 | `agent-customizer-plugin.prd.md` (Phase 9 status) |
| **TOTAL** | **65** | |

---

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Converted agent references exceed 200 lines | Low | Source agents are 124-129 lines; conversion removes 7-line frontmatter, adds ~8-line TOC = net ~125-130 lines |
| standalone SKILL.md exceeds 500 lines | Low | Plugin SKILL.md files are 79-108 lines; standalone adds ~3 lines per replaced delegation = still ≤115 lines |
| Standalone hooks/subagents exclusion missed in an improve-* skill | Medium | Task F parity check greps for "standalone distribution" in all improve-* SKILL.md files |
| Staging directory left behind | Low | Task E explicitly removes it; Task F checks `ls skills/` |
| Reference parity drift (plugin updates not reflected in standalone) | Medium | No mitigation in this phase — standalone is an initial copy. Document in project notes. |

---

## Success Signal

From PRD Phase 9:
> "All standalone skills produce identical output to plugin versions; parity check passes; works with any AI coding tool"

Measurable exit criteria:

1. `grep -rn "Delegate to" skills/*/SKILL.md` returns empty
2. All 8 standalone skills have `references/artifact-analyzer.md`
3. All 4 improve-* standalone skills have `references/{type}-evaluator.md`
4. All reference files ≤200 lines, all SKILL.md ≤500 lines
5. `standalone-skills.md` includes agent-customizer agent names in exclusion list
6. PRD Phase 9 shows `in-progress`
