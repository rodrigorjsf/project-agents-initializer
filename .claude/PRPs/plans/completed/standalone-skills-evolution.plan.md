# Feature: Standalone Skills Evolution

## Summary

Rewrite all 4 standalone SKILL.md files (`skills/init-agents/`, `skills/improve-agents/`, `skills/init-claude/`, `skills/improve-claude/`) to achieve feature parity with the evolved plugin versions. The transformation replaces inline bash analysis blocks and inline templates with reference document reads (`${CLAUDE_SKILL_DIR}/references/`) and template file reads (`${CLAUDE_SKILL_DIR}/assets/templates/`), adds a Phase 4 self-validation loop that reads `validation-criteria.md`, and restructures each file from 4 phases to 5 phases matching the plugin pattern. All `references/` and `assets/templates/` directories already exist from Phases 1-3 and 5b — only the SKILL.md orchestration files need rewriting.

## User Story

As a developer using any Agent Skills-compliant tool (Copilot, Codex, Gemini CLI)
I want standalone skills to use evidence-based references and self-validation
So that I get the same quality CLAUDE.md/AGENTS.md output as Claude Code plugin users

## Problem Statement

The 4 standalone SKILL.md files contain inline bash blocks and inline markdown templates that bypass the reference documents and templates already created in Phases 1-3. They lack a self-validation loop, producing unverified output. Their 4-phase structure (analysis → detection → generate → present) misses the validation step that plugin skills include as Phase 4.

## Solution Statement

Replace inline analysis with reference-doc-guided analysis (`Read ${CLAUDE_SKILL_DIR}/references/codebase-analyzer.md and follow its instructions`), replace inline templates with template file reads, add a self-validation Phase 4 that reads `validation-criteria.md`, and renumber "Present and Write" to Phase 5. The standalone skills use the same evidence-based references as the plugin but execute analysis inline (per standalone conventions) rather than delegating to agents.

## Metadata

| Field            | Value                                                      |
| ---------------- | ---------------------------------------------------------- |
| Type             | ENHANCEMENT                                                |
| Complexity       | HIGH                                                       |
| Systems Affected | skills/init-agents, skills/improve-agents, skills/init-claude, skills/improve-claude |
| Dependencies     | None (all references/assets already exist from Phases 1-3, 5b) |
| Estimated Tasks  | 4                                                          |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐             ║
║   │  User runs   │ ───► │  SKILL.md    │ ───► │  Raw output  │             ║
║   │  /init-agents│      │  (143 lines) │      │  (unvalidated)│            ║
║   └──────────────┘      └──────┬───────┘      └──────────────┘             ║
║                                │                                            ║
║                     ┌──────────┴──────────┐                                 ║
║                     │  Inline bash blocks │  references/ ← UNUSED          ║
║                     │  Inline templates   │  assets/     ← UNUSED          ║
║                     │  No validation loop │  validation-criteria ← UNUSED  ║
║                     └─────────────────────┘                                 ║
║                                                                             ║
║   USER_FLOW: invoke skill → inline bash analysis → inline templates →      ║
║              present to user → write files                                  ║
║   PAIN_POINT: Analysis relies on model's general knowledge, not evidence-  ║
║              based reference docs. No quality validation before output.     ║
║   DATA_FLOW: bash output → model context → inline template → raw files     ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐             ║
║   │  User runs   │ ───► │  SKILL.md    │ ───► │  Validated   │             ║
║   │  /init-agents│      │  (~80 lines) │      │  output      │             ║
║   └──────────────┘      └──────┬───────┘      └──────────────┘             ║
║                                │                                            ║
║              ┌─────────────────┼─────────────────┐                          ║
║              ▼                 ▼                  ▼                          ║
║   ┌─────────────────┐ ┌────────────────┐ ┌──────────────────┐              ║
║   │ references/     │ │ assets/        │ │ validation-      │              ║
║   │ codebase-*.md   │ │ templates/     │ │ criteria.md      │              ║
║   │ scope-*.md      │ │ root-*.md      │ │ (3-iter loop)    │              ║
║   │ context-opt.md  │ │ scoped-*.md    │ └──────────────────┘              ║
║   │ what-not-*.md   │ │ domain-doc.md  │                                   ║
║   │ progressive-*.md│ └────────────────┘                                   ║
║   └─────────────────┘                                                       ║
║                                                                             ║
║   USER_FLOW: invoke skill → reference-guided analysis → template-based     ║
║              generation → self-validation loop → present to user → write   ║
║   VALUE_ADD: Evidence-based analysis, consistent templates, validated      ║
║              output — identical quality to plugin skills on any tool       ║
║   DATA_FLOW: ref docs → guided analysis → templates → validated files     ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Phase 1-2 | Inline bash, model general knowledge | Reference-doc-guided analysis | More thorough, evidence-based detection |
| Phase 3 | Inline markdown templates embedded in SKILL.md | External template file reads via `${CLAUDE_SKILL_DIR}` | Consistent structure, shorter SKILL.md |
| Phase 4 | None (skipped) | Self-validation loop (max 3 iterations) | Output passes all quality criteria before writing |
| SKILL.md size | 143-204 lines (bloated) | ~80-155 lines (matches plugin) | Faster skill loading, less token cost |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | all | Plugin pattern to MIRROR for init-agents |
| P0 | `plugins/agents-initializer/skills/improve-agents/SKILL.md` | all | Plugin pattern to MIRROR for improve-agents |
| P0 | `plugins/agents-initializer/skills/init-claude/SKILL.md` | all | Plugin pattern to MIRROR for init-claude |
| P0 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | all | Plugin pattern to MIRROR for improve-claude |
| P0 | `skills/init-agents/SKILL.md` | all | Current standalone to REWRITE |
| P0 | `skills/improve-agents/SKILL.md` | all | Current standalone to REWRITE |
| P0 | `skills/init-claude/SKILL.md` | all | Current standalone to REWRITE |
| P0 | `skills/improve-claude/SKILL.md` | all | Current standalone to REWRITE |
| P1 | `skills/init-agents/references/codebase-analyzer.md` | 1-18 | Understand converted reference doc format |
| P1 | `skills/init-agents/references/validation-criteria.md` | 67-77 | Validation Loop Instructions the skills will reference |
| P2 | `.claude/rules/standalone-skills.md` | all | Constraints for standalone skills |
| P2 | `.claude/rules/plugin-skills.md` | all | Understand plugin constraints (contrast) |

---

## Patterns to Mirror

**PLUGIN INIT SKILL PATTERN (init-agents, init-claude):**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:29-78
// COPY THIS STRUCTURE (adapt mechanism for standalone):

### Phase 1: Codebase Analysis

Delegate to the `codebase-analyzer` agent with this task:
> [task description]

### Phase 2: Scope Detection

Delegate to the `scope-detector` agent with this task:
> [task description]

### Phase 3: Generate Files

Before generating, read these reference documents:
- `${CLAUDE_SKILL_DIR}/references/progressive-disclosure-guide.md`
- `${CLAUDE_SKILL_DIR}/references/what-not-to-include.md`
- `${CLAUDE_SKILL_DIR}/references/context-optimization.md`

[template reads with ${CLAUDE_SKILL_DIR}/assets/templates/]

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its
**Validation Loop Instructions** against every generated file.

### Phase 5: Present and Write
```

**PLUGIN IMPROVE SKILL PATTERN (improve-agents, improve-claude):**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-agents/SKILL.md:32-134
// COPY THIS STRUCTURE:

### Phase 1: Current State Analysis

Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the scoring rubric.
Delegate to the `file-evaluator` agent with this task:
> [evaluation task]

### Phase 2: Codebase Comparison

Delegate to the `codebase-analyzer` agent with this task:
> [comparison task]

### Phase 3: Generate Improvement Plan

Read these reference documents:
- [same 3-4 references as init]

[template reads]

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its
**Validation Loop Instructions**.
For improve operations, also evaluate the "If This Is an IMPROVE Operation" section.

### Phase 5: Present and Apply
```

**STANDALONE DELEGATION REPLACEMENT PATTERN:**

```markdown
// SOURCE: skills/init-agents/references/codebase-analyzer.md:1-10
// USE THIS PATTERN to replace "Delegate to agent" with "Read reference doc":

// PLUGIN says:
//   Delegate to the `codebase-analyzer` agent with this task:
//   > [task]
//   The agent runs on Sonnet with read-only tools. Wait for it to complete.

// STANDALONE says:
//   Read `${CLAUDE_SKILL_DIR}/references/codebase-analyzer.md` and follow its
//   codebase analysis instructions to analyze the project at the current
//   working directory.
//   [task-specific focus directive preserved]
```

**SELF-VALIDATION LOOP PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:67-71
// COPY THIS PATTERN EXACTLY:

### Phase 4: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/validation-criteria.md` and execute its
**Validation Loop Instructions** against every generated file.

The loop evaluates all hard limits and quality checks, fixes any failures,
and re-evaluates — maximum 3 iterations. Do not proceed to Phase 5 until
ALL criteria pass for ALL files.
```

**IMPROVE-SPECIFIC VALIDATION ADDITIONS:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-agents/SKILL.md:101-107
// ADD THIS for improve-agents:

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"**
section in validation-criteria.md — checking information preservation, custom
command retention, and progressive disclosure structure preservation.

Maximum 3 iterations. Do not proceed to Phase 5 until ALL criteria pass.
```

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:107-111
// ADD THIS for improve-claude:

For improve operations, also evaluate the **"If This Is an IMPROVE Operation"**
section. For CLAUDE.md files, also check **CLAUDE.md-specific** structural checks
(path-scoping, minimal always-loaded content). Maximum 3 iterations.
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `skills/init-agents/SKILL.md` | REWRITE | Replace 4-phase inline to 5-phase reference-based |
| `skills/improve-agents/SKILL.md` | REWRITE | Replace 4-phase inline to 5-phase reference-based |
| `skills/init-claude/SKILL.md` | REWRITE | Replace 4-phase inline to 5-phase reference-based |
| `skills/improve-claude/SKILL.md` | REWRITE | Replace 4-phase inline to 5-phase reference-based |

**NO files to CREATE** — all reference and asset files already exist.

---

## NOT Building (Scope Limits)

- **No changes to plugin SKILL.md files** — Phase 4 already evolved these; they're the pattern source
- **No changes to reference files** — Phase 1 + 5b already created and enriched these
- **No changes to asset templates** — Phase 2 already created these
- **No changes to converted agent references** — Phase 3 already converted these
- **No changes to `.claude/rules/`** — Phase 7 handles rules updates
- **No changes to CLAUDE.md files** — Phase 7 handles documentation updates
- **No new reference or asset files** — everything needed already exists
- **No `scripts/` directories** — validation stays as SKILL.md instructions per PRD decision

---

## Step-by-Step Tasks

Execute in any order — all 4 tasks are independent. Each rewrites one standalone SKILL.md.

### Task 1: REWRITE `skills/init-agents/SKILL.md`

- **ACTION**: Replace entire Process section with 5-phase reference-based structure
- **READ FIRST**: `plugins/agents-initializer/skills/init-agents/SKILL.md` (the pattern to mirror)
- **READ SECOND**: `skills/init-agents/SKILL.md` (current file to rewrite)

**TRANSFORMATION RULES:**

1. **Keep unchanged**: Frontmatter (`name`, `description`), `# Initialize AGENTS.md` heading, `## Why This Approach` section, `## Hard Rules` section — these are identical to plugin and already correct
2. **Phase 1 — Replace inline bash (current lines 29-55) with**:

   ```markdown
   ### Phase 1: Codebase Analysis

   Read `${CLAUDE_SKILL_DIR}/references/codebase-analyzer.md` and follow its codebase analysis instructions to analyze the project at the current working directory.

   Focus: Return ONLY non-standard, non-obvious information that would cause an agent to make mistakes if it didn't know them. Be ruthlessly minimal.
   ```

3. **Phase 2 — Replace inline bash (current lines 57-71) with**:

   ```markdown
   ### Phase 2: Scope Detection

   Read `${CLAUDE_SKILL_DIR}/references/scope-detector.md` and follow its scope detection instructions for the project at the current working directory.

   Focus: Only flag scopes with genuinely different tooling or conventions. A simple single-package project should have ZERO additional scopes.
   ```

4. **Phase 3 — Replace inline templates (current lines 73-126) with**: Copy Phase 3 from `plugins/agents-initializer/skills/init-agents/SKILL.md:45-65` exactly (reference reads + template reads)
5. **Phase 4 — Add new section**: Copy Phase 4 from `plugins/agents-initializer/skills/init-agents/SKILL.md:67-71` exactly
6. **Phase 5 — Renumber current Phase 4**: Copy Phase 5 from `plugins/agents-initializer/skills/init-agents/SKILL.md:73-78` exactly
7. **Remove**: `## What NOT to Include (Evidence-Based)` trailing table (current lines 134-143) — this content is now in `references/what-not-to-include.md`

**TARGET LINE COUNT**: ~80 lines (plugin is 78)
**MIRROR**: `plugins/agents-initializer/skills/init-agents/SKILL.md`
**GOTCHA**: Do NOT use "Delegate to agent" language — use "Read reference and follow its instructions". Do NOT include "The agent runs on Sonnet" or "Wait for it to complete" — these are plugin-specific.
**VALIDATE**:

```bash
wc -l skills/init-agents/SKILL.md  # Must be < 500 (target ~80)
grep -c "Delegate to" skills/init-agents/SKILL.md  # Must be 0
grep -c "agent with this task" skills/init-agents/SKILL.md  # Must be 0
grep -c "CLAUDE_SKILL_DIR" skills/init-agents/SKILL.md  # Must be >= 7 (refs + templates)
grep -c "Phase [1-5]" skills/init-agents/SKILL.md  # Must be 5
grep -c "validation-criteria" skills/init-agents/SKILL.md  # Must be >= 1
```

---

### Task 2: REWRITE `skills/improve-agents/SKILL.md`

- **ACTION**: Replace entire Process section with 5-phase reference-based structure
- **READ FIRST**: `plugins/agents-initializer/skills/improve-agents/SKILL.md` (pattern to mirror)
- **READ SECOND**: `skills/improve-agents/SKILL.md` (current file to rewrite)

**TRANSFORMATION RULES:**

1. **Keep unchanged**: Frontmatter, `# Improve AGENTS.md` heading, `## Why This Matters` section, `## Hard Rules` section — identical to plugin
2. **Phase 1 — Replace inline bash (current lines 32-56) with**:

   ```markdown
   ### Phase 1: Current State Analysis

   Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the complete scoring rubric, bloat indicators table, and staleness detection patterns. Use this to inform the evaluation and to understand the expected output format.

   Read `${CLAUDE_SKILL_DIR}/references/file-evaluator.md` and follow its evaluation instructions to evaluate all AGENTS.md files in the project at the current working directory.

   Check for:

   1. Files over 200 lines
   2. Bloat indicators (directory listings, obvious conventions, vague instructions)
   3. Stale references (file paths that don't exist, commands that aren't in package.json)
   4. Contradictions between files
   5. Progressive disclosure opportunities (content that should be in separate files)
   6. Missing scope-specific files

   Build a structured assessment with specific line numbers and content for each issue.
   ```

3. **Phase 2 — Replace inline bash (current lines 58-81) with**:

   ```markdown
   ### Phase 2: Codebase Comparison

   Read `${CLAUDE_SKILL_DIR}/references/codebase-analyzer.md` and follow its codebase analysis instructions. Focus on:

   1. Verifying that tooling commands documented in AGENTS.md files still work
   2. Identifying scopes that have distinct tooling but lack their own AGENTS.md
   3. Detecting new domain areas not covered by existing documentation

   Return ONLY actionable findings.
   ```

4. **Phase 3 — Replace current section (lines 83-105) with**: Copy Phase 3 from `plugins/agents-initializer/skills/improve-agents/SKILL.md:65-99` exactly. Note: Change "Based on both subagent reports" to "Based on both analyses" (no subagent language).
5. **Phase 4 — Add new section**: Copy Phase 4 from `plugins/agents-initializer/skills/improve-agents/SKILL.md:101-107` exactly (includes improve-specific validation section reference)
6. **Phase 5 — Renumber current Phase 4**: Copy Phase 5 from `plugins/agents-initializer/skills/improve-agents/SKILL.md:109-133` exactly
7. **Remove**: `## Improvement Checklist` trailing section (current lines 131-144) — this content is now in `references/validation-criteria.md`

**TARGET LINE COUNT**: ~130 lines (plugin is 134)
**MIRROR**: `plugins/agents-initializer/skills/improve-agents/SKILL.md`
**GOTCHA**: Phase 3 in the plugin says "Based on both subagent reports" — change to "Based on both analyses" for standalone. Do NOT copy "The agent runs on Sonnet" language.
**VALIDATE**:

```bash
wc -l skills/improve-agents/SKILL.md  # Must be < 500 (target ~130)
grep -c "Delegate to" skills/improve-agents/SKILL.md  # Must be 0
grep -c "subagent" skills/improve-agents/SKILL.md  # Must be 0
grep -c "CLAUDE_SKILL_DIR" skills/improve-agents/SKILL.md  # Must be >= 9
grep -c "Phase [1-5]" skills/improve-agents/SKILL.md  # Must be 5
grep -c "validation-criteria" skills/improve-agents/SKILL.md  # Must be >= 1
grep -c "evaluation-criteria" skills/improve-agents/SKILL.md  # Must be >= 1
grep -c "file-evaluator" skills/improve-agents/SKILL.md  # Must be >= 1
```

---

### Task 3: REWRITE `skills/init-claude/SKILL.md`

- **ACTION**: Replace entire Process section with 5-phase reference-based structure
- **READ FIRST**: `plugins/agents-initializer/skills/init-claude/SKILL.md` (pattern to mirror)
- **READ SECOND**: `skills/init-claude/SKILL.md` (current file to rewrite)

**TRANSFORMATION RULES:**

1. **Keep unchanged**: Frontmatter, `# Initialize CLAUDE.md` heading, `## Why This Approach` section (including Claude Code hierarchy explanation), `## Hard Rules` section — identical to plugin
2. **Phase 1 — Replace inline bash (current lines 37-63) with**:

   ```markdown
   ### Phase 1: Codebase Analysis

   Read `${CLAUDE_SKILL_DIR}/references/codebase-analyzer.md` and follow its codebase analysis instructions to analyze the project at the current working directory.

   Focus: Return ONLY non-standard, non-obvious information that would cause Claude to make mistakes if it didn't know them. Be ruthlessly minimal.
   ```

3. **Phase 2 — Replace inline bash (current lines 65-80) with**:

   ```markdown
   ### Phase 2: Scope Detection

   Read `${CLAUDE_SKILL_DIR}/references/scope-detector.md` and follow its scope detection instructions for the project at the current working directory.

   Focus: Only flag scopes with genuinely different tooling or conventions. A simple single-package project should have ZERO additional scopes. Also identify areas that would benefit from path-scoped .claude/rules/ files. Check shared/library packages in monorepos — even utility packages may need their own scope if they have unique constraints (e.g., zero-dependency rules, dual exports, conditional imports).
   ```

4. **Phase 3 — Replace inline templates (current lines 87-179) with**: Copy Phase 3 from `plugins/agents-initializer/skills/init-claude/SKILL.md:53-82` exactly (reads 4 references including `claude-rules-system.md`, reads 4 templates)
5. **Phase 4 — Add new section**: Copy Phase 4 from `plugins/agents-initializer/skills/init-claude/SKILL.md:84-88` exactly (includes CLAUDE.md-specific checks)
6. **Phase 5 — Renumber current Phase 4**: Copy Phase 5 from `plugins/agents-initializer/skills/init-claude/SKILL.md:90-97` exactly (includes `.claude/rules/` directory creation step)
7. **Remove**: `## File Loading Behavior (Claude Code)` table (current lines 181-192) and `## What NOT to Include (Evidence-Based)` table (current lines 194-204) — content is in references

**TARGET LINE COUNT**: ~100 lines (plugin is 97)
**MIRROR**: `plugins/agents-initializer/skills/init-claude/SKILL.md`
**GOTCHA**: init-claude reads 4 references in Phase 3 (not 3 like init-agents) — includes `claude-rules-system.md`. Phase 5 includes step 6: "Create `.claude/rules/` directory if generating rules files."
**VALIDATE**:

```bash
wc -l skills/init-claude/SKILL.md  # Must be < 500 (target ~100)
grep -c "Delegate to" skills/init-claude/SKILL.md  # Must be 0
grep -c "CLAUDE_SKILL_DIR" skills/init-claude/SKILL.md  # Must be >= 10
grep -c "Phase [1-5]" skills/init-claude/SKILL.md  # Must be 5
grep -c "validation-criteria" skills/init-claude/SKILL.md  # Must be >= 1
grep -c "claude-rules-system" skills/init-claude/SKILL.md  # Must be >= 1
```

---

### Task 4: REWRITE `skills/improve-claude/SKILL.md`

- **ACTION**: Replace entire Process section with 5-phase reference-based structure
- **READ FIRST**: `plugins/agents-initializer/skills/improve-claude/SKILL.md` (pattern to mirror)
- **READ SECOND**: `skills/improve-claude/SKILL.md` (current file to rewrite)

**TRANSFORMATION RULES:**

1. **Keep unchanged**: Frontmatter, `# Improve CLAUDE.md` heading, `## Why This Matters` section, `## Hard Rules` section — identical to plugin
2. **Phase 1 — Replace inline bash (current lines 38-66) with**:

   ```markdown
   ### Phase 1: Current State Analysis

   Read `${CLAUDE_SKILL_DIR}/references/evaluation-criteria.md` for the scoring rubric and bloat/staleness indicators.

   Read `${CLAUDE_SKILL_DIR}/references/file-evaluator.md` and follow its evaluation instructions to evaluate all CLAUDE.md files and .claude/rules/ files in the project at the current working directory.

   Check for:

   1. Files over 200 lines
   2. Bloat indicators (directory listings, obvious conventions, vague instructions)
   3. Stale references (file paths that don't exist, commands that aren't in package.json)
   4. Contradictions between files (including between CLAUDE.md and .claude/rules/)
   5. Progressive disclosure opportunities (content that should be in separate files or path-scoped rules)
   6. Missing scope-specific files
   7. Rules files without path-scoping that should have it (wasting tokens on every request)
   8. Content in root CLAUDE.md that only applies to specific file patterns (should be in .claude/rules/)

   Build a structured assessment with specific line numbers and content for each issue.
   ```

3. **Phase 2 — Replace inline bash (current lines 68-93) with**:

   ```markdown
   ### Phase 2: Codebase Comparison

   Read `${CLAUDE_SKILL_DIR}/references/codebase-analyzer.md` and follow its codebase analysis instructions. Focus on:

   1. Verifying that tooling commands documented in CLAUDE.md files still work
   2. Identifying scopes that have distinct tooling but lack their own CLAUDE.md — including library/shared packages in monorepos that have unique constraints (zero-dependency rules, dual exports, conditional imports, server-only markers)
   3. Detecting file patterns that have specific conventions but lack path-scoped .claude/rules/ — check for BOTH convention rules (code style, test patterns) AND domain-critical rules (privacy, security, compliance) that should be path-scoped to sensitive file patterns
   4. Detecting new domain areas not covered by existing documentation

   Return ONLY actionable findings.
   ```

4. **Phase 3 — Replace current section (lines 95-119) with**: Copy Phase 3 from `plugins/agents-initializer/skills/improve-claude/SKILL.md:67-105` exactly. Change "Based on both subagent reports" to "Based on both analyses".
5. **Phase 4 — Add new section**: Copy Phase 4 from `plugins/agents-initializer/skills/improve-claude/SKILL.md:107-111` exactly (includes improve-specific + CLAUDE.md-specific validation checks)
6. **Phase 5 — Renumber current Phase 4**: Copy Phase 5 from `plugins/agents-initializer/skills/improve-claude/SKILL.md:113-148` exactly (includes token impact analysis, path-scoping verification)
7. **Remove**: `## Loading Behavior Reference` table (current lines 151-162) and `## Improvement Checklist` section (current lines 164-181) — content is in references

**TARGET LINE COUNT**: ~150 lines (plugin is 148)
**MIRROR**: `plugins/agents-initializer/skills/improve-claude/SKILL.md`
**GOTCHA**: Phase 3 reads 4 references (includes `claude-rules-system.md`). Phase 4 has the most validation: improve-specific + CLAUDE.md-specific. Phase 5 includes token impact analysis and path-scoping verification — this is unique to improve-claude.
**VALIDATE**:

```bash
wc -l skills/improve-claude/SKILL.md  # Must be < 500 (target ~150)
grep -c "Delegate to" skills/improve-claude/SKILL.md  # Must be 0
grep -c "subagent" skills/improve-claude/SKILL.md  # Must be 0
grep -c "CLAUDE_SKILL_DIR" skills/improve-claude/SKILL.md  # Must be >= 12
grep -c "Phase [1-5]" skills/improve-claude/SKILL.md  # Must be 5
grep -c "validation-criteria" skills/improve-claude/SKILL.md  # Must be >= 1
grep -c "evaluation-criteria" skills/improve-claude/SKILL.md  # Must be >= 1
grep -c "claude-rules-system" skills/improve-claude/SKILL.md  # Must be >= 1
grep -c "file-evaluator" skills/improve-claude/SKILL.md  # Must be >= 1
```

---

## Testing Strategy

### Structural Verification (per task)

| Check | Command | Expected |
|-------|---------|----------|
| Line count | `wc -l skills/*/SKILL.md` | All < 500 (targets: ~80, ~130, ~100, ~150) |
| No agent delegation | `grep -r "Delegate to" skills/*/SKILL.md` | 0 matches |
| No subagent language | `grep -r "subagent" skills/*/SKILL.md` | 0 matches |
| No "agent runs on" | `grep -r "agent runs on" skills/*/SKILL.md` | 0 matches |
| No "Wait for it" | `grep -r "Wait for it to complete" skills/*/SKILL.md` | 0 matches |
| Has reference reads | `grep -r "CLAUDE_SKILL_DIR" skills/*/SKILL.md` | Multiple per file |
| Has 5 phases | `grep -c "^### Phase" skills/*/SKILL.md` | 5 per file |
| Has validation phase | `grep -r "validation-criteria" skills/*/SKILL.md` | At least 1 per file |
| Third-person descriptions | `grep "description:" skills/*/SKILL.md` | No "your project", "you" |

### Feature Parity Checks

| Plugin Feature | Init Skills Check | Improve Skills Check |
|----------------|-------------------|----------------------|
| Reference reads in Phase 3 | `grep -c "CLAUDE_SKILL_DIR/references" skills/init-*/SKILL.md` ≥ 3 | `grep -c "CLAUDE_SKILL_DIR/references" skills/improve-*/SKILL.md` ≥ 4 |
| Template reads in Phase 3 | `grep -c "assets/templates" skills/init-*/SKILL.md` ≥ 2 | `grep -c "assets/templates" skills/improve-*/SKILL.md` ≥ 2 |
| Self-validation Phase 4 | Present in all 4 files | With improve-specific section |
| evaluation-criteria.md | Not used by init skills | Used by improve skills |
| file-evaluator.md | Not used by init skills | Used by improve skills |
| claude-rules-system.md | Used by init-claude | Used by improve-claude |
| codebase-analyzer.md (ref) | Used by init-agents, init-claude | Used by improve-agents, improve-claude |
| scope-detector.md (ref) | Used by init-agents, init-claude | Not used by improve skills |

### Content Comparison (manual verification)

For each of the 4 skills, verify:

- [ ] Preamble (heading, Why section, Hard Rules) is identical between plugin and standalone
- [ ] Phase 3 reference reads match the plugin's Phase 3 reference reads exactly
- [ ] Phase 3 template reads match the plugin's Phase 3 template reads exactly
- [ ] Phase 4 validation instructions match the plugin's Phase 4
- [ ] Phase 5 presentation/writing steps match the plugin's Phase 5
- [ ] No inline bash code blocks remain
- [ ] No inline markdown templates remain
- [ ] No trailing reference tables remain (What NOT to Include, Improvement Checklist, Loading Behavior)

### Edge Cases Checklist

- [ ] init-agents references: no `evaluation-criteria.md`, no `file-evaluator.md`, no `claude-rules-system.md`
- [ ] improve-agents references: no `scope-detector.md`, no `claude-rules-system.md`
- [ ] init-claude references: includes `claude-rules-system.md` in Phase 3
- [ ] improve-claude references: includes `claude-rules-system.md` in Phase 3, most validation checks in Phase 4
- [ ] No standalone SKILL.md references a file that doesn't exist in its `references/` or `assets/templates/` directory
- [ ] Descriptions remain in third person (no regression from Phase 5 compliance)
- [ ] improve-claude Phase 4 mentions BOTH improve-specific AND CLAUDE.md-specific checks

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Check all 4 standalone SKILL.md files exist and are under 500 lines
for f in skills/init-agents/SKILL.md skills/improve-agents/SKILL.md skills/init-claude/SKILL.md skills/improve-claude/SKILL.md; do
  lines=$(wc -l < "$f")
  echo "$f: $lines lines"
  [ "$lines" -lt 500 ] || echo "FAIL: $f exceeds 500 lines"
done

# Check no agent delegation language
grep -rn "Delegate to\|agent with this task\|agent runs on Sonnet\|Wait for it to complete\|subagent" skills/*/SKILL.md && echo "FAIL: Agent delegation language found" || echo "PASS: No delegation language"

# Check all files have 5 phases
for f in skills/*/SKILL.md; do
  phases=$(grep -c "^### Phase" "$f")
  echo "$f: $phases phases"
  [ "$phases" -eq 5 ] || echo "FAIL: Expected 5 phases in $f"
done

# Check all files reference validation-criteria.md
for f in skills/*/SKILL.md; do
  grep -q "validation-criteria" "$f" && echo "PASS: $f has validation" || echo "FAIL: $f missing validation"
done

# Check descriptions are third person
grep "description:" skills/*/SKILL.md | grep -i "your\|you " && echo "FAIL: Non-third-person description" || echo "PASS: All descriptions third person"
```

**EXPECT**: All checks pass, zero failures

### Level 2: REFERENCE_INTEGRITY

```bash
# Verify every ${CLAUDE_SKILL_DIR} reference in SKILL.md points to an existing file
for skill_dir in skills/init-agents skills/improve-agents skills/init-claude skills/improve-claude; do
  grep -oP '\$\{CLAUDE_SKILL_DIR\}/\S+' "$skill_dir/SKILL.md" | sed 's/`//g' | while read ref; do
    local_path=$(echo "$ref" | sed "s|\\\${CLAUDE_SKILL_DIR}|$skill_dir|")
    [ -f "$local_path" ] && echo "OK: $local_path" || echo "FAIL: $local_path does not exist"
  done
done
```

**EXPECT**: All referenced files exist

### Level 3: PARITY_CHECK

```bash
# Compare phase structure between plugin and standalone
for skill in init-agents improve-agents init-claude improve-claude; do
  echo "=== $skill ==="
  echo "Plugin phases:"
  grep "^### Phase" "plugins/agents-initializer/skills/$skill/SKILL.md"
  echo "Standalone phases:"
  grep "^### Phase" "skills/$skill/SKILL.md"
  echo ""
done

# Compare reference reads between plugin and standalone (standalone should have >= plugin)
for skill in init-agents improve-agents init-claude improve-claude; do
  plugin_refs=$(grep -c "CLAUDE_SKILL_DIR/references" "plugins/agents-initializer/skills/$skill/SKILL.md")
  standalone_refs=$(grep -c "CLAUDE_SKILL_DIR/references" "skills/$skill/SKILL.md")
  echo "$skill — plugin refs: $plugin_refs, standalone refs: $standalone_refs"
  [ "$standalone_refs" -ge "$plugin_refs" ] || echo "FAIL: Standalone has fewer refs"
done
```

**EXPECT**: Phase names match. Standalone reference reads >= plugin reference reads (standalone adds codebase-analyzer.md, scope-detector.md, file-evaluator.md).

### Level 4: MANUAL_VALIDATION

After all 4 files are rewritten:

1. Read each standalone SKILL.md end-to-end and verify it makes sense as a self-contained skill
2. Verify each file's preamble (frontmatter through Hard Rules) is byte-for-byte identical to its plugin counterpart (except the description's subagent clause)
3. Verify Phase 3-5 structure closely mirrors the plugin (with no agent delegation language)
4. Verify Phase 1-2 use `${CLAUDE_SKILL_DIR}/references/[converted-agent].md` reads instead of agent delegation
5. Verify no orphaned content (inline bash, inline templates, trailing tables) remains

---

## Acceptance Criteria

- [ ] All 4 standalone SKILL.md files rewritten from 4-phase to 5-phase structure
- [ ] Zero agent delegation language in any standalone SKILL.md
- [ ] All reference reads use `${CLAUDE_SKILL_DIR}/references/` paths to files that exist
- [ ] All template reads use `${CLAUDE_SKILL_DIR}/assets/templates/` paths to files that exist
- [ ] Phase 4 self-validation loop present in all 4 files
- [ ] improve-* skills include improve-specific validation section reference
- [ ] improve-claude includes CLAUDE.md-specific validation checks
- [ ] *-claude skills read `claude-rules-system.md` in Phase 3
- [ ] All SKILL.md files under 500 lines (targets: ~80, ~130, ~100, ~150)
- [ ] All descriptions remain in third person
- [ ] No inline bash code blocks remain
- [ ] No inline markdown templates remain
- [ ] No trailing informational tables remain (moved to references)
- [ ] Level 1-3 validation commands pass

---

## Completion Checklist

- [ ] Task 1 (init-agents) completed and validated
- [ ] Task 2 (improve-agents) completed and validated
- [ ] Task 3 (init-claude) completed and validated
- [ ] Task 4 (improve-claude) completed and validated
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Reference integrity passes
- [ ] Level 3: Parity check passes
- [ ] Level 4: Manual validation passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `.claude/rules/standalone-skills.md` blocks "Never reference agents" | LOW | MED | The rule says "Never reference agents" — the converted docs are reference documents, not agents. Phase 7 will update the rule to explicitly document the reference-based analysis pattern. |
| Standalone analysis quality lower than plugin subagent analysis | MED | MED | Converted reference docs preserve 100% of agent analysis logic. The detection patterns, output formats, and self-verification steps are identical. Quality difference is the model executing inline vs as a subagent. |
| SKILL.md body exceeds 500-line Anthropic limit | LOW | HIGH | Target line counts (80-150) are well under 500. The reference-based approach dramatically shortens SKILL.md by moving content to external files. |
| Missing reference/template file breaks skill | LOW | HIGH | Level 2 validation explicitly checks every `${CLAUDE_SKILL_DIR}` path resolves to an existing file. All files already exist from prior phases. |
| Tool-specific language leaks into standalone skills | MED | LOW | Validation checks grep for "Delegate to", "subagent", "agent runs on", "Wait for it". Converted reference docs use tool-agnostic language ("Use your environment's file reading and search capabilities"). |

---

## Notes

- **No external research needed** — this is a pure markdown skills project with no code dependencies
- **All supporting files pre-exist** — Phases 1-3 and 5b created all reference docs, asset templates, and converted agent references. Phase 6 only touches the 4 SKILL.md orchestration files.
- **Key architectural insight**: The standalone skills achieve parity with plugin skills by using **the same reference documents** but with a different execution mechanism. Plugin says "Delegate to agent"; standalone says "Read reference doc and follow its instructions inline." The analysis logic is identical because it lives in the reference documents, not in the SKILL.md body.
- **Phase 7 dependency**: The `.claude/rules/standalone-skills.md` file currently says "All analysis must be inline — include explicit bash commands for each step." After Phase 6, standalone skills use reference-doc-guided analysis instead of explicit bash blocks. Phase 7 should update this rule to say "Analysis uses reference documents read via ${CLAUDE_SKILL_DIR} — follow instructions inline, no agent delegation."
- **Line count improvements**: Current standalone SKILL.md files range from 143-204 lines (bloated with inline content). After rewrite, they'll range from ~80-150 lines — a significant reduction while adding a validation phase.
- **Parallel execution**: All 4 tasks are independent. They can be executed in parallel in separate worktrees or sequentially in a single session.
