# Feature: Reference Content Creation (Phase 1)

## Summary

Create 6 authoritative reference documents derived from the existing `docs/` research, then distribute copies to the `references/` subdirectory of each skill that needs them. These references replace the inline citations and general-knowledge reliance currently in SKILL.md files, giving skills evidence-based guidance they can load on-demand during execution.

## User Story

As a developer using the agents-initializer skills
I want skills to have bundled reference documents with evidence-based guidance
So that generated CLAUDE.md/AGENTS.md files are consistently accurate regardless of which AI tool executes the skill

## Problem Statement

All 8 skills contain only a single SKILL.md file with no `references/` directory. They cite research docs by name (e.g., "ETH Zurich paper", "a-guide-to-agents.md") but don't actually load or reference those documents. The executing model must rely on general knowledge to produce correct output, leading to inconsistent results.

## Solution Statement

Author 6 reference files (each under 200 lines) distilled from `docs/` research. Each file provides actionable instructions — not theory — that skills will read during execution. Copies are placed in every skill's `references/` directory following the Agent Skills spec's self-contained skill convention (no symlinks, no shared parent directory).

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY                                    |
| Complexity       | MEDIUM                                            |
| Systems Affected | plugins/agents-initializer/skills/*, skills/*     |
| Dependencies     | None (Phase 1 has no dependencies)                |
| Estimated Tasks  | 14                                                |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════╗
║                           BEFORE STATE                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ┌──────────────┐         ┌──────────────┐      ┌──────────────┐  ║
║   │  Developer   │ ──────► │ /init-agents │ ───► │  AGENTS.md   │  ║
║   │  invokes     │         │  SKILL.md    │      │  generated   │  ║
║   │  skill       │         │  (bare)      │      │              │  ║
║   └──────────────┘         └──────────────┘      └──────────────┘  ║
║                                   │                                 ║
║                            No references/                           ║
║                            directory exists                         ║
║                                                                     ║
║   PAIN_POINT: Skill cites "ETH Zurich paper" and                   ║
║   "a-guide-to-agents.md" by name only — model must rely             ║
║   on general knowledge to apply these findings correctly            ║
║                                                                     ║
║   DATA_FLOW: SKILL.md body → model's general knowledge → output    ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════╗
║                           AFTER STATE                               ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║   ┌──────────────┐         ┌──────────────┐      ┌──────────────┐  ║
║   │  Developer   │ ──────► │ /init-agents │ ───► │  AGENTS.md   │  ║
║   │  invokes     │         │  SKILL.md    │      │  generated   │  ║
║   │  skill       │         │              │      │  (validated) │  ║
║   └──────────────┘         └──────┬───────┘      └──────────────┘  ║
║                                   │                                 ║
║                            reads on-demand                          ║
║                                   ▼                                 ║
║                     ┌─────────────────────────┐                     ║
║                     │     references/          │                    ║
║                     │  ├── progressive-        │                    ║
║                     │  │   disclosure-guide.md │                    ║
║                     │  ├── context-            │                    ║
║                     │  │   optimization.md     │                    ║
║                     │  ├── what-not-to-        │                    ║
║                     │  │   include.md          │                    ║
║                     │  └── validation-         │                    ║
║                     │      criteria.md         │                    ║
║                     └─────────────────────────┘                     ║
║                                                                     ║
║   VALUE_ADD: Skill loads specific, evidence-based reference         ║
║   docs with actionable instructions, citations, and criteria        ║
║                                                                     ║
║   DATA_FLOW: SKILL.md → reads references/ → evidence-informed      ║
║              decisions → validated output                           ║
║                                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `*/references/` | Does not exist | Contains 4-6 reference files per skill | Skills produce more consistent, evidence-based output |
| SKILL.md body | Cites research by name only | Will reference `references/*.md` (in Phase 4/5) | No change yet — Phase 1 creates files only |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `docs/a-guide-to-agents.md` | all (239) | Primary source for progressive-disclosure-guide.md |
| P0 | `docs/a-guide-to-claude.md` | all (225) | Primary source for progressive-disclosure-guide.md (Claude-specific additions) |
| P0 | `docs/research-llm-context-optimization.md` | all (568) | Primary source for context-optimization.md and what-not-to-include.md |
| P0 | `docs/research-claude-code-skills-format.md` | all (505) | Primary source for claude-rules-system.md |
| P0 | `docs/Evaluating-AGENTS-paper.md` | 1-100 | Key findings for validation-criteria.md and what-not-to-include.md |
| P1 | `plugins/agents-initializer/agents/file-evaluator.md` | all (151) | Primary source for evaluation-criteria.md |
| P1 | `plugins/agents-initializer/skills/improve-claude/SKILL.md` | 143-160 | Improvement checklist pattern to mirror in validation-criteria.md |
| P1 | `plugins/agents-initializer/skills/init-agents/SKILL.md` | 106-116 | "What NOT to Include" table pattern to mirror |
| P2 | `docs/research-claude-code-skills-format.md` | 153-186 | Agent Skills spec directory layout — confirms references/ convention |

---

## Patterns to Mirror

**REFERENCE FILE STYLE:**
Each reference file must be:

- Under 200 lines (hard limit from PRD line 380)
- Actionable instructions, not theory summaries
- Structured with tables, checklists, and decision criteria
- Traceable to source docs with inline citations
- Written as instructions the skill can follow, not prose for humans to read

**EXISTING CHECKLIST PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/SKILL.md:143-160
// COPY THIS PATTERN for validation-criteria.md:
## Improvement Checklist

After improvements, every CLAUDE.md and .claude/rules/ file should pass:

- [ ] Under 200 lines
- [ ] No directory/file structure listings
- [ ] No standard language conventions
...
```

**EXISTING EVIDENCE TABLE PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/skills/init-agents/SKILL.md:106-116
// COPY THIS PATTERN for what-not-to-include.md:
## What NOT to Include (Evidence-Based)

| Content | Why to Exclude | Source |
|---------|----------------|--------|
| Directory structure | "Not effective at providing repository overview" | ETH Zurich paper |
...
```

**EXISTING QUALITY SCORING PATTERN:**

```markdown
// SOURCE: plugins/agents-initializer/agents/file-evaluator.md:132-141
// COPY THIS PATTERN for evaluation-criteria.md:
### Quality Score
| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Conciseness | 3 | 342 lines, 70%+ over limit |
...
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/init-agents/references/progressive-disclosure-guide.md` | CREATE | Shared reference — file hierarchy design |
| `plugins/agents-initializer/skills/init-agents/references/context-optimization.md` | CREATE | Shared reference — token budgets, attention |
| `plugins/agents-initializer/skills/init-agents/references/what-not-to-include.md` | CREATE | Shared reference — evidence table |
| `plugins/agents-initializer/skills/init-agents/references/validation-criteria.md` | CREATE | Shared reference — quality checklist |
| `plugins/agents-initializer/skills/improve-agents/references/progressive-disclosure-guide.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-agents/references/context-optimization.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-agents/references/what-not-to-include.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-agents/references/validation-criteria.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-agents/references/evaluation-criteria.md` | CREATE | Improve-only — scoring rubric |
| `plugins/agents-initializer/skills/init-claude/references/progressive-disclosure-guide.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/init-claude/references/context-optimization.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/init-claude/references/what-not-to-include.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/init-claude/references/validation-criteria.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/init-claude/references/claude-rules-system.md` | CREATE | Claude-only — .claude/rules/ conventions |
| `plugins/agents-initializer/skills/improve-claude/references/progressive-disclosure-guide.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-claude/references/context-optimization.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-claude/references/validation-criteria.md` | CREATE | Copy of shared reference |
| `plugins/agents-initializer/skills/improve-claude/references/evaluation-criteria.md` | CREATE | Copy — improve-only |
| `plugins/agents-initializer/skills/improve-claude/references/claude-rules-system.md` | CREATE | Copy — Claude-only |
| `skills/init-agents/references/progressive-disclosure-guide.md` | CREATE | Standalone copy |
| `skills/init-agents/references/context-optimization.md` | CREATE | Standalone copy |
| `skills/init-agents/references/what-not-to-include.md` | CREATE | Standalone copy |
| `skills/init-agents/references/validation-criteria.md` | CREATE | Standalone copy |
| `skills/improve-agents/references/progressive-disclosure-guide.md` | CREATE | Standalone copy |
| `skills/improve-agents/references/context-optimization.md` | CREATE | Standalone copy |
| `skills/improve-agents/references/what-not-to-include.md` | CREATE | Standalone copy |
| `skills/improve-agents/references/validation-criteria.md` | CREATE | Standalone copy |
| `skills/improve-agents/references/evaluation-criteria.md` | CREATE | Standalone copy |
| `skills/init-claude/references/progressive-disclosure-guide.md` | CREATE | Standalone copy |
| `skills/init-claude/references/context-optimization.md` | CREATE | Standalone copy |
| `skills/init-claude/references/what-not-to-include.md` | CREATE | Standalone copy |
| `skills/init-claude/references/validation-criteria.md` | CREATE | Standalone copy |
| `skills/init-claude/references/claude-rules-system.md` | CREATE | Standalone copy |
| `skills/improve-claude/references/progressive-disclosure-guide.md` | CREATE | Standalone copy |
| `skills/improve-claude/references/context-optimization.md` | CREATE | Standalone copy |
| `skills/improve-claude/references/what-not-to-include.md` | CREATE | Standalone copy |
| `skills/improve-claude/references/validation-criteria.md` | CREATE | Standalone copy |
| `skills/improve-claude/references/evaluation-criteria.md` | CREATE | Standalone copy |
| `skills/improve-claude/references/claude-rules-system.md` | CREATE | Standalone copy |

**Total: 40 files (6 unique authored × distribution across 8 skills)**

---

## NOT Building (Scope Limits)

- **SKILL.md rewrites** — Phase 4/5 will update SKILL.md files to reference these documents
- **Asset templates** — Phase 2 creates `assets/templates/` files separately
- **Agent-to-reference conversions** — Phase 3 converts agent files to standalone references
- **Rules updates** — Phase 6 updates `.claude/rules/` to enforce new conventions
- **Validation testing** — Phase 7 runs cross-distribution validation

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `references/` directories for all 8 skills

- **ACTION**: Create empty `references/` directories
- **IMPLEMENT**:

  ```bash
  mkdir -p plugins/agents-initializer/skills/init-agents/references
  mkdir -p plugins/agents-initializer/skills/improve-agents/references
  mkdir -p plugins/agents-initializer/skills/init-claude/references
  mkdir -p plugins/agents-initializer/skills/improve-claude/references
  mkdir -p skills/init-agents/references
  mkdir -p skills/improve-agents/references
  mkdir -p skills/init-claude/references
  mkdir -p skills/improve-claude/references
  ```

- **VALIDATE**: `ls -d plugins/agents-initializer/skills/*/references skills/*/references` — should list 8 directories

### Task 2: AUTHOR `progressive-disclosure-guide.md`

- **ACTION**: Create the progressive disclosure reference file
- **PRIMARY SOURCES**:
  - `docs/a-guide-to-agents.md` — ball-of-mud pattern (lines 34-43), instruction budget (~150-200, lines 45-58), minimum content (lines 75-81), progressive disclosure patterns (lines 110-163), monorepo hierarchy (lines 164-193), decision table (lines 228-233)
  - `docs/a-guide-to-claude.md` — identical structure, same key content (95% overlap)
  - `docs/research-llm-context-optimization.md` — section 3 progressive disclosure (lines 138-208), section 5 hierarchical config (lines 257-305)
- **IMPLEMENT**: Distill into actionable reference with these sections:
  1. **File Hierarchy Decision Table** — when to use root vs separate file vs nested doc vs rule (merge the two guides' tables at lines 228-233)
  2. **Root File Requirements** — the absolute minimum: one-sentence desc, package manager, build commands (from guides lines 75-81)
  3. **Monorepo What-Goes-Where** — root vs package level content (from guides lines 170-193)
  4. **Progressive Disclosure Patterns** — move language rules to separate files, nest docs, use skills (from guides lines 110-163)
  5. **CLAUDE.md-Specific Hierarchy** — subdirectory CLAUDE.md, .claude/rules/ path-scoping, loading behavior table (from research lines 182-208, 257-305)
  6. **AGENTS.md-Specific Notes** — AGENTS.md is an open standard; symlink tip; no .claude/rules/ equivalent
  7. **Anti-Patterns** — ball-of-mud feedback loop, auto-generated file trap (from guides lines 34-43)
- **LINE BUDGET**: ≤ 180 lines
- **GOTCHA**: Content must be written as instructions for the skill to follow ("Generate X", "Check for Y"), not as theory for humans to read
- **VALIDATE**: `wc -l progressive-disclosure-guide.md` — must be ≤ 200

### Task 3: AUTHOR `context-optimization.md`

- **ACTION**: Create the context optimization reference file
- **PRIMARY SOURCE**: `docs/research-llm-context-optimization.md` (568 lines → distill to ≤ 180)
- **IMPLEMENT**: Distill into actionable reference with these sections:
  1. **Hard Limits** — 200 lines per file (section 2.2, lines 86-101), ~150-200 instructions (section 2.1, lines 73-85), zero contradictions (section 4.3, lines 232-236)
  2. **The Attention Budget** — context is finite with diminishing returns (section 1.1, lines 14-31); n² attention constraint; context rot definition
  3. **Lost in the Middle** — critical instructions at start/end of files, not buried in middle (section 1.2, lines 33-43)
  4. **Quality Over Quantity Checklist** — include/exclude table (section 2.3, lines 113-121); instruction specificity goldilocks (section 2.4, lines 123-134)
  5. **Context Poisoning Vectors** — stale documentation (section 4.4, lines 237-243), contradictions (section 4.3), over-specification (section 4.5, lines 245-253), failed approach accumulation (section 4.1, lines 213-224)
  6. **JIT Documentation Patterns** — implementation patterns table (section 7.2, lines 451-461); hybrid pre-loaded + on-demand (section 3.2, lines 156-167)
  7. **Key Citations** — compact citations list from sources index (lines 540-557) for traceability
- **LINE BUDGET**: ≤ 180 lines
- **GOTCHA**: Extract the quantitative claims with their exact quotes and sources — skills need to cite these when presenting output to users
- **VALIDATE**: `wc -l context-optimization.md` — must be ≤ 200

### Task 4: AUTHOR `what-not-to-include.md`

- **ACTION**: Create the evidence table of content to exclude
- **PRIMARY SOURCES**:
  - `plugins/agents-initializer/skills/init-agents/SKILL.md:106-116` — existing 6-row table to expand
  - `docs/research-llm-context-optimization.md` — section 2.3 include/exclude table (lines 113-121)
  - `docs/Evaluating-AGENTS-paper.md` — abstract findings: "context files do not provide effective overviews", "unnecessary requirements make tasks harder"
  - `docs/plans/2026-03-22-agents-initializer-plugin-design.md` — evidence table (lines 26-37) with 10 source/finding/impact rows
- **IMPLEMENT**: Create a definitive evidence table with these sections:
  1. **Exclusion Evidence Table** — expanded from existing 6-row table to ~12 rows, each with: Content Type | Why to Exclude | Evidence Quote | Source Citation
  2. **The Instruction Test** — "Would removing this cause the agent to make mistakes? If no, cut it." (from Anthropic Best Practices)
  3. **Common Traps** — auto-generated files trap, ball-of-mud growth, comprehensive-over-restrained mindset
  4. **What TO Include Instead** — the positive side: one-sentence desc, non-standard tooling, non-obvious conventions, progressive disclosure pointers
- **LINE BUDGET**: ≤ 150 lines
- **GOTCHA**: The existing "What NOT to Include" tables in SKILL.md files cite source names — the reference must provide the actual quotes and citations that back each exclusion
- **VALIDATE**: `wc -l what-not-to-include.md` — must be ≤ 200

### Task 5: AUTHOR `validation-criteria.md`

- **ACTION**: Create the self-validation quality checklist
- **PRIMARY SOURCES**:
  - `plugins/agents-initializer/skills/improve-claude/SKILL.md:143-160` — most complete checklist (13 items)
  - `plugins/agents-initializer/skills/improve-agents/SKILL.md:108-122` — AGENTS.md checklist (10 items)
  - `plugins/agents-initializer/agents/file-evaluator.md:23-59` — hard limits table, bloat indicators table, staleness indicators table, progressive disclosure assessment
  - PRD lines 289-311 — hard limits, quality checks, information preservation criteria
- **IMPLEMENT**: Create with these sections:
  1. **Hard Limits** (auto-fail if violated):
     - Root file: 15-40 lines
     - Scope files: 10-30 lines
     - Any file: ≤ 200 lines
     - Zero language-specific rules in root file
     - Zero stale file path references
     - Zero contradictions between files
  2. **Quality Checks** (must all pass):
     - Every instruction is actionable (not vague like "write clean code")
     - Package manager specified if non-standard
     - Build/test commands included if non-standard
     - Progressive disclosure: domain docs referenced, not inlined
     - No information that tools can enforce (linting rules, formatting)
     - No duplication across files in the hierarchy
     - No directory/file structure listings
     - No standard language conventions the model already knows
  3. **Information Preservation Checks** (improve skills only):
     - Critical project information preserved (domain concepts, security notes, compliance requirements)
     - Custom commands/scripts referenced in original file are retained
     - Existing progressive disclosure structure not flattened
  4. **Structural Checks**:
     - One scope per file
     - Progressive disclosure pointers where appropriate
     - CLAUDE.md-specific: .claude/rules/ files have path-scoping when applicable
     - CLAUDE.md-specific: minimal content in always-loaded locations
  5. **Validation Loop Instructions**:
     - For EACH generated file, evaluate against ALL criteria above
     - If ANY criterion fails: identify failure, fix, re-evaluate
     - Maximum 3 iterations — if still failing, present issues to user
     - Only proceed when ALL criteria pass for ALL files
- **LINE BUDGET**: ≤ 150 lines
- **GOTCHA**: Must be usable by both init skills (no "information preservation" section needed) and improve skills (full checklist). Use conditional sections: "If this is an IMPROVE operation, also check..."
- **VALIDATE**: `wc -l validation-criteria.md` — must be ≤ 200

### Task 6: AUTHOR `evaluation-criteria.md`

- **ACTION**: Create the scoring rubric for evaluating existing files (improve skills only)
- **PRIMARY SOURCES**:
  - `plugins/agents-initializer/agents/file-evaluator.md` — entire file (151 lines): hard limits (lines 23-28), bloat indicators (lines 30-41), staleness indicators (lines 43-50), progressive disclosure assessment (lines 52-59), quality score template (lines 132-141)
  - `docs/research-llm-context-optimization.md` — include/exclude table (lines 113-121), instruction specificity (lines 123-134)
  - `docs/plans/2026-03-22-agents-initializer-plugin-design.md` — evidence table (lines 26-37)
- **IMPLEMENT**: Create with these sections:
  1. **Hard Limits Table** — ≤200 lines, ≤150-200 instructions, 0 contradictions (from file-evaluator.md:23-28 with source citations)
  2. **Bloat Indicators Table** — 6 types with "Why It's Bloat" and source citations (from file-evaluator.md:30-41)
  3. **Staleness Indicators Table** — 4 types with detection methods (from file-evaluator.md:43-50)
  4. **Progressive Disclosure Assessment** — 4 questions with Good/Bad columns (from file-evaluator.md:52-59)
  5. **Instruction Specificity** — goldilocks examples: ✅ specific vs ❌ vague (from research lines 131-134)
  6. **Quality Score Rubric** — 5 dimensions (Conciseness, Accuracy, Specificity, Progressive Disclosure, Consistency) with scoring guidelines (from file-evaluator.md:132-141)
  7. **Evaluation Output Template** — the exact format the skill should produce when reporting findings (from file-evaluator.md:89-141)
- **LINE BUDGET**: ≤ 180 lines
- **GOTCHA**: This file is used by improve-agents and improve-claude only (not init skills). It provides the ASSESSMENT rubric (what's wrong with existing files), while validation-criteria.md provides the GENERATION checklist (what the output must satisfy).
- **VALIDATE**: `wc -l evaluation-criteria.md` — must be ≤ 200

### Task 7: AUTHOR `claude-rules-system.md`

- **ACTION**: Create the .claude/rules/ conventions reference (Claude skills only)
- **PRIMARY SOURCES**:
  - `docs/research-claude-code-skills-format.md` — skill directory layout (lines 153-186), plugin structure (lines 207-264)
  - `docs/research-llm-context-optimization.md` — path-specific rules (section 3.4, lines 181-196), rules system (section 5.2, lines 284-305), loading behavior (section 3.5, lines 198-208)
  - `plugins/agents-initializer/skills/init-claude/SKILL.md:104-136` — .claude/rules/ generation instructions
  - `plugins/agents-initializer/skills/improve-claude/SKILL.md:128-141` — loading behavior reference table
- **IMPLEMENT**: Create with these sections:
  1. **Loading Behavior Table** — when each config location loads and its token impact (from init-claude SKILL.md:151-164)
  2. **Path-Scoping Syntax** — YAML frontmatter `paths:` field with glob patterns (from research lines 186-196)
  3. **When to Create Rules Files** — two categories: convention rules + domain-critical rules (from init-claude SKILL.md:118-136)
  4. **When NOT to Create Rules Files** — project-wide goes in root CLAUDE.md, scope-wide in subdirectory CLAUDE.md, obvious patterns omitted (from init-claude SKILL.md:133-136)
  5. **Rules Directory Structure** — `.claude/rules/` layout with examples (from research section 5.2, lines 290-299)
  6. **Rules vs CLAUDE.md Decision Table** — when to use root CLAUDE.md vs subdirectory CLAUDE.md vs .claude/rules/ vs domain files
  7. **CLAUDE.md Hierarchy** — 5-level scope with priority order (from research section 5.1, lines 259-282)
  8. **Maximize On-Demand Loading** — priority is moving content from always-consumed to on-demand locations
- **LINE BUDGET**: ≤ 180 lines
- **GOTCHA**: This reference is Claude Code-specific by design. It's used by init-claude and improve-claude only. AGENTS.md skills don't need it because AGENTS.md has no `.claude/rules/` equivalent.
- **VALIDATE**: `wc -l claude-rules-system.md` — must be ≤ 200

### Task 8: DISTRIBUTE to plugin `init-agents/references/`

- **ACTION**: Copy the 4 shared references to plugin init-agents skill
- **FILES TO COPY**:
  - `progressive-disclosure-guide.md`
  - `context-optimization.md`
  - `what-not-to-include.md`
  - `validation-criteria.md`
- **DESTINATION**: `plugins/agents-initializer/skills/init-agents/references/`
- **VALIDATE**: `ls plugins/agents-initializer/skills/init-agents/references/` — should list 4 files

### Task 9: DISTRIBUTE to plugin `improve-agents/references/`

- **ACTION**: Copy 5 references (4 shared + evaluation-criteria)
- **FILES TO COPY**: 4 shared + `evaluation-criteria.md`
- **DESTINATION**: `plugins/agents-initializer/skills/improve-agents/references/`
- **VALIDATE**: `ls plugins/agents-initializer/skills/improve-agents/references/` — should list 5 files

### Task 10: DISTRIBUTE to plugin `init-claude/references/`

- **ACTION**: Copy 5 references (4 shared + claude-rules-system)
- **FILES TO COPY**: 4 shared + `claude-rules-system.md`
- **DESTINATION**: `plugins/agents-initializer/skills/init-claude/references/`
- **VALIDATE**: `ls plugins/agents-initializer/skills/init-claude/references/` — should list 5 files

### Task 11: DISTRIBUTE to plugin `improve-claude/references/`

- **ACTION**: Copy 6 references (4 shared + evaluation-criteria + claude-rules-system)
- **FILES TO COPY**: 4 shared + `evaluation-criteria.md` + `claude-rules-system.md`
- **DESTINATION**: `plugins/agents-initializer/skills/improve-claude/references/`
- **VALIDATE**: `ls plugins/agents-initializer/skills/improve-claude/references/` — should list 6 files

### Task 12: DISTRIBUTE to standalone `init-agents/references/` and `init-claude/references/`

- **ACTION**: Copy references to standalone init skills
- **FILES**: init-agents gets 4 shared; init-claude gets 4 shared + claude-rules-system
- **DESTINATIONS**: `skills/init-agents/references/` and `skills/init-claude/references/`
- **VALIDATE**: `ls skills/init-agents/references/ skills/init-claude/references/` — should list 4 and 5 files respectively

### Task 13: DISTRIBUTE to standalone `improve-agents/references/` and `improve-claude/references/`

- **ACTION**: Copy references to standalone improve skills
- **FILES**: improve-agents gets 4 shared + evaluation-criteria; improve-claude gets 4 shared + evaluation-criteria + claude-rules-system
- **DESTINATIONS**: `skills/improve-agents/references/` and `skills/improve-claude/references/`
- **VALIDATE**: `ls skills/improve-agents/references/ skills/improve-claude/references/` — should list 5 and 6 files respectively

### Task 14: VERIFY all 40 files and line counts

- **ACTION**: Run final verification across all 8 skills
- **IMPLEMENT**:

  ```bash
  # Count files per skill
  for dir in plugins/agents-initializer/skills/*/references skills/*/references; do
    echo "$dir: $(ls "$dir" | wc -l) files"
  done

  # Verify all files are under 200 lines
  find plugins/agents-initializer/skills/*/references skills/*/references -name "*.md" | while read f; do
    lines=$(wc -l < "$f")
    if [ "$lines" -gt 200 ]; then echo "OVER LIMIT: $f ($lines lines)"; fi
  done

  # Verify identical copies match
  for ref in progressive-disclosure-guide.md context-optimization.md what-not-to-include.md validation-criteria.md; do
    md5sum plugins/agents-initializer/skills/init-agents/references/$ref skills/init-agents/references/$ref
  done
  ```

- **EXPECTED**: All files under 200 lines; matching checksums for shared references; correct file counts per skill

---

## Testing Strategy

### Verification Checks

| Check | Method | Validates |
| ----- | ------ | --------- |
| File count per skill | `ls references/ \| wc -l` | Correct distribution |
| Line count per file | `wc -l references/*.md` | Under 200-line limit |
| Shared file identity | `md5sum` across copies | No accidental drift |
| Source traceability | Manual scan for citations | Every claim cites a source |
| Actionable language | Manual scan for imperatives | Instructions not theory |

### Edge Cases Checklist

- [ ] No file exceeds 200 lines
- [ ] Every exclusion in what-not-to-include.md has a source citation
- [ ] validation-criteria.md conditional sections clearly marked for init vs improve
- [ ] claude-rules-system.md only present in claude skills (not agents skills)
- [ ] evaluation-criteria.md only present in improve skills (not init skills)
- [ ] All shared references are byte-identical across copies

---

## Validation Commands

### Level 1: FILE_EXISTENCE

```bash
# Verify all 40 reference files exist
expected_count=40
actual_count=$(find plugins/agents-initializer/skills/*/references skills/*/references -name "*.md" 2>/dev/null | wc -l)
echo "Expected: $expected_count, Found: $actual_count"
[ "$actual_count" -eq "$expected_count" ] && echo "PASS" || echo "FAIL"
```

**EXPECT**: 40 files found, PASS

### Level 2: LINE_LIMITS

```bash
# All files must be ≤ 200 lines
find plugins/agents-initializer/skills/*/references skills/*/references -name "*.md" | while read f; do
  lines=$(wc -l < "$f")
  [ "$lines" -gt 200 ] && echo "FAIL: $f ($lines lines)"
done
echo "Line limit check complete"
```

**EXPECT**: No FAIL output

### Level 3: DISTRIBUTION_CORRECTNESS

```bash
# Verify per-skill file counts
echo "init-agents (plugin): $(ls plugins/agents-initializer/skills/init-agents/references/ | wc -l) (expect 4)"
echo "improve-agents (plugin): $(ls plugins/agents-initializer/skills/improve-agents/references/ | wc -l) (expect 5)"
echo "init-claude (plugin): $(ls plugins/agents-initializer/skills/init-claude/references/ | wc -l) (expect 5)"
echo "improve-claude (plugin): $(ls plugins/agents-initializer/skills/improve-claude/references/ | wc -l) (expect 6)"
echo "init-agents (standalone): $(ls skills/init-agents/references/ | wc -l) (expect 4)"
echo "improve-agents (standalone): $(ls skills/improve-agents/references/ | wc -l) (expect 5)"
echo "init-claude (standalone): $(ls skills/init-claude/references/ | wc -l) (expect 5)"
echo "improve-claude (standalone): $(ls skills/improve-claude/references/ | wc -l) (expect 6)"
```

**EXPECT**: Counts match expectations (4, 5, 5, 6, 4, 5, 5, 6)

### Level 4: CONTENT_INTEGRITY

```bash
# Verify shared files are identical across all copies
for ref in progressive-disclosure-guide.md context-optimization.md what-not-to-include.md validation-criteria.md; do
  hashes=$(find plugins/agents-initializer/skills/*/references skills/*/references -name "$ref" -exec md5sum {} + | awk '{print $1}' | sort -u | wc -l)
  [ "$hashes" -eq 1 ] && echo "PASS: $ref (all copies identical)" || echo "FAIL: $ref ($hashes different versions)"
done
```

**EXPECT**: All PASS (1 unique hash per shared reference)

---

## Acceptance Criteria

- [ ] 6 unique reference files authored, each ≤ 200 lines
- [ ] 40 total reference files distributed across 8 skills
- [ ] Distribution matches: init-agents=4, improve-agents=5, init-claude=5, improve-claude=6 (×2 distributions)
- [ ] Shared references are byte-identical across all copies
- [ ] Every reference file contains actionable instructions (not theory)
- [ ] Every claim/exclusion cites its source document
- [ ] claude-rules-system.md only in claude skills
- [ ] evaluation-criteria.md only in improve skills
- [ ] validation-criteria.md has conditional sections for init vs improve usage

---

## Completion Checklist

- [ ] All tasks completed in dependency order (Tasks 1-7 author, Tasks 8-13 distribute, Task 14 verify)
- [ ] Each task validated immediately after completion
- [ ] Level 1: File existence check passes (40 files)
- [ ] Level 2: Line limit check passes (all ≤ 200)
- [ ] Level 3: Distribution correctness passes (correct counts)
- [ ] Level 4: Content integrity passes (identical shared copies)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Reference files exceed 200-line budget | Medium | HIGH | Write in passes: first draft → cut ruthlessly → verify. Budget each section. |
| Content becomes theory instead of instructions | Medium | HIGH | Review each file asking: "Can the skill execute this directly?" Rewrite passive voice → imperative. |
| Source attribution gaps | Low | Medium | Cross-reference every table row against source docs during authoring. |
| Shared files drift between copies | Low | Medium | Author once, copy programmatically (cp command), verify with md5sum. Never edit copies individually. |
| 200-line budget forces important content out | Medium | Medium | Prioritize by impact: hard limits first, then decision tables, then citations. Move deep theory to a "further reading" pointer. |

---

## Notes

- **Authoring strategy**: Write each of the 6 reference files in a temporary location first (e.g., `/tmp/refs/`), then copy to all target directories. This prevents drift and ensures all copies are identical.
- **Phase 1 creates files only** — it does NOT modify any SKILL.md. The SKILL.md files will be updated in Phase 4 (plugin) and Phase 5 (standalone) to reference these documents.
- **Standalone skills will also receive converted agent refs in Phase 3** — `codebase-analyzer.md`, `scope-detector.md`, `file-evaluator.md` are NOT part of Phase 1. Phase 3 handles the agent-to-reference conversion.
- **The 6 reference files in this phase are "knowledge references"** (research-derived guidance). Phase 3's references are "process references" (analysis instructions). Different purposes, same `references/` directory.
