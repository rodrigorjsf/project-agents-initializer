# Feature: Phase 1 — Research & Documentation Foundation

## Summary

Create the `automation-migration-guide.md` reference file that provides evidence-based decision criteria for when to migrate instructions from CLAUDE.md/AGENTS.md to on-demand mechanisms (skills, hooks, rules, subagents). Update `DESIGN-GUIDELINES.md` with a new Guideline 13 documenting the automation migration framework. Verify the existing sync mechanism covers new artifacts. The reference file is the key enabler for Phases 2-5 — it provides the classification logic that the improve skills will use to suggest migrations.

## User Story

As a developer using the improve skills
I want evidence-based decision criteria for automation migration
So that the improve flow can suggest the correct on-demand mechanism for each instruction

## Problem Statement

The improve skills reorganize content within the CLAUDE/AGENTS hierarchy but never suggest migrating infrequent behaviors to on-demand mechanisms (skills, hooks, rules, subagents). No reference file exists that defines when each mechanism is appropriate, what indicators identify migration candidates, or what evidence supports each recommendation. Without this foundation, Phases 2-5 cannot classify or suggest migrations.

## Solution Statement

Create `automation-migration-guide.md` as a new shared reference file deployed to all 4 improve skills across both distributions (4 copies). The file synthesizes the PRD's evidence base (9 content types mapped to mechanisms), web research findings (24 hook events, 4 hook types, new skill features), and existing `docs/analysis/` corpus into a structured decision framework. Add a corresponding Guideline 13 to `DESIGN-GUIDELINES.md` for design transparency. Verify the existing sync mechanism already covers the new artifacts.

## Metadata

| Field            | Value |
| ---------------- | ----- |
| Type             | NEW_CAPABILITY |
| Complexity       | MEDIUM |
| Systems Affected | improve skill references (4 copies), DESIGN-GUIDELINES.md, PRD |
| Dependencies     | None (Phase 1 has no dependencies) |
| Estimated Tasks  | 7 |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌────────────────┐       ┌──────────────────┐       ┌───────────────┐     ║
║   │ User runs      │ ───►  │ Phase 3 reads:   │ ───►  │ Improvement   │     ║
║   │ /improve-claude │       │ • progressive-   │       │ plan with     │     ║
║   └────────────────┘       │   disclosure.md  │       │ 3 categories: │     ║
║                            │ • what-not-to-   │       │ • Removal     │     ║
║                            │   include.md     │       │ • Refactoring │     ║
║                            │ • context-       │       │ • Addition    │     ║
║                            │   optimization.md│       └───────────────┘     ║
║                            │ • claude-rules-  │                             ║
║                            │   system.md      │       NO MIGRATION          ║
║                            └──────────────────┘       SUGGESTIONS           ║
║                                                                             ║
║   USER_FLOW: Run improve → get reorganization only → no mechanism hints     ║
║   PAIN_POINT: Infrequent behaviors stay in always-loaded context forever    ║
║   DATA_FLOW: SKILL.md → 3-4 references → 3 action categories               ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ┌────────────────┐       ┌──────────────────┐       ┌───────────────┐     ║
║   │ User runs      │ ───►  │ Phase 3 reads:   │ ───►  │ Improvement   │     ║
║   │ /improve-claude │       │ • progressive-   │       │ plan with     │     ║
║   └────────────────┘       │   disclosure.md  │       │ 4 categories: │     ║
║                            │ • what-not-to-   │       │ • Removal     │     ║
║                            │   include.md     │       │ • Refactoring │     ║
║                            │ • context-       │       │   └─ NEW:     │     ║
║                            │   optimization.md│       │     Migration │     ║
║                            │ • claude-rules-  │       │     sub-cat   │     ║
║                            │   system.md      │       │ • Addition    │     ║
║                            │ • automation-    │       └───────────────┘     ║
║                            │   migration-     │              │              ║
║                            │   guide.md  ◄────── NEW REFERENCE              ║
║                            └──────────────────┘                             ║
║                                                                             ║
║   USER_FLOW: Run improve → get reorganization + migration suggestions       ║
║   VALUE_ADD: Infrequent behaviors identified with mechanism recommendation  ║
║   DATA_FLOW: SKILL.md → 4-5 references → 4 action categories + migration   ║
║                                                                             ║
║   NOTE: Phase 1 creates ONLY the reference file. Phases 4-5 wire it into   ║
║   SKILL.md Phase 3 and the user presentation flow.                          ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `*/improve-*/references/` | 4-6 reference files per skill | +1 `automation-migration-guide.md` | Decision criteria available for Phase 4 integration |
| `DESIGN-GUIDELINES.md` | 12 guidelines | 13 guidelines (new: Automation Migration) | Design transparency for migration decisions |
| docs/ | 16 analysis files + 5 anchor docs | Research findings integrated into reference | Evidence base consolidated for skill consumption |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude/rules/reference-files.md` | all | Format rules for ALL reference files — MUST follow exactly |
| P0 | `plugins/agents-initializer/skills/improve-claude/references/context-optimization.md` | all | Pattern to MIRROR for new reference file structure |
| P0 | `plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md` | all | Pattern to MIRROR for table-heavy evidence reference |
| P1 | `DESIGN-GUIDELINES.md` | 197-251 | Guidelines 10-12 structure to MIRROR for Guideline 13 |
| P1 | `.claude/PRPs/prds/context-aware-improve-optimization.prd.md` | 346-358 | Evidence base table — core decision criteria content |
| P2 | `docs/analysis/analysis-automate-workflow-with-hooks.md` | 21-130, 433-445 | Hook types, events, comparison tables |
| P2 | `docs/analysis/analysis-skill-authoring-best-practices.md` | 19-46, 131-143 | Skill token costs, degrees of freedom |
| P2 | `docs/analysis/analysis-how-claude-remembers-a-project.md` | 7-64 | Two-layer architecture, rules loading semantics |
| P2 | `docs/analysis/analysis-evaluating-agents-paper.md` | 36-52 | Agent inference capabilities, what to DELETE |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Claude Code Hooks](https://code.claude.com/docs/en/hooks) | Hook events table | 24 events (expanded from ~6), new `http` type, `if:` field |
| [Claude Code Skills](https://code.claude.com/docs/en/skills) | Frontmatter fields | New `effort` field, `paths` YAML list syntax, description cap |
| [Claude Code Memory](https://code.claude.com/docs/en/memory) | Rules loading | Path-scoped rules trigger on file read; negation patterns |
| [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) | Context costs | Official hierarchy: CLAUDE.md → rules → skills → memory |

---

## Patterns to Mirror

**REFERENCE_FILE_HEADER:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/references/context-optimization.md:1-7
// COPY THIS PATTERN:
# Context Optimization

Evidence-based instructions for managing token budgets and attention in agent configuration files.
Source: research-llm-context-optimization.md

---
```

**REFERENCE_TABLE_OF_CONTENTS (required for files >100 lines):**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/references/context-optimization.md:8-17
// COPY THIS PATTERN:
## Contents

- Hard limits (lines per file, instruction count, contradictions)
- The attention budget (finite resource, n-squared constraint)
- Lost in the middle (placement strategy for critical instructions)
- Quality over quantity checklist (include/exclude decision table)
- Context poisoning vectors (detection and removal)
- JIT documentation patterns (on-demand loading strategies)
- Key citations
```

**EVIDENCE_TABLE_FORMAT:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/references/what-not-to-include.md:10-24
// COPY THIS PATTERN:
| Content Type | Why to Exclude | Evidence Quote | Source |
|-------------|----------------|---------------|--------|
| Hook-enforced behaviors | Hooks handle deterministically; config instructions are redundant | "Hooks provide deterministic control..." | Anthropic Hooks Guide |
```

**CITATION_FORMAT:**

```markdown
// SOURCE: plugins/agents-initializer/skills/improve-claude/references/context-optimization.md:82
// COPY THIS PATTERN:
*Source: research-llm-context-optimization.md lines 113-134*
```

**DESIGN_GUIDELINE_STRUCTURE:**

```markdown
// SOURCE: DESIGN-GUIDELINES.md:197-212
// COPY THIS PATTERN:
## Guideline 10: On-Demand Context Loading

**Source**: [Anthropic — Skills](https://docs.anthropic.com/en/docs/claude-code/skills) | [Anthropic — Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) | [docs/analysis/analysis-automate-workflow-with-hooks.md](docs/analysis/analysis-automate-workflow-with-hooks.md)

[2-3 sentence explanation]

| Mechanism | Context Cost | Enforcement | Best For |
|---|---|---|---|
...

**Implemented in**: [file paths and components]

---
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md` | CREATE | Decision criteria reference — plugin improve-claude copy |
| `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md` | CREATE | Decision criteria reference — plugin improve-agents copy |
| `skills/improve-claude/references/automation-migration-guide.md` | CREATE | Decision criteria reference — standalone improve-claude copy |
| `skills/improve-agents/references/automation-migration-guide.md` | CREATE | Decision criteria reference — standalone improve-agents copy |
| `DESIGN-GUIDELINES.md` | UPDATE | Add Guideline 13: Automation Migration Decision Framework |
| `.claude/PRPs/prds/context-aware-improve-optimization.prd.md` | UPDATE | Phase 1 status: pending → in-progress, link plan |

---

## NOT Building (Scope Limits)

- **SKILL.md modifications** — Phase 4 wires the reference into improve Phase 3; this phase only creates the reference file
- **file-evaluator.md updates** — Phase 3 adds "Automation Opportunity Indicators" to file-evaluator.md; not in Phase 1 scope
- **evaluation-criteria.md updates** — Phase 3 adds automation opportunity scoring; not in Phase 1 scope
- **what-not-to-include.md updates** — Phase 3 adds active linking to migration guide; not in Phase 1 scope
- **Init preflight checks** — Phase 2 scope
- **New templates** (skill.md, hook-config.md) — Phase 6 scope
- **Research documents in docs/** — The existing `docs/analysis/` corpus is sufficient; web research findings are synthesized directly into the reference file. No new docs/ files needed unless the existing corpus is proven insufficient during validation

---

## Step-by-Step Tasks

### Task 1: CREATE `automation-migration-guide.md` (canonical copy)

- **ACTION**: CREATE the canonical reference file with decision criteria for automation migration
- **LOCATION**: `plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md`
- **IMPLEMENT**: Follow the content structure below. The file must be under 200 lines and include a `## Contents` TOC.

**Content structure** (synthesize from PRD lines 346-358, web research findings, and existing docs/analysis/):

```
# Automation Migration Guide

Decision criteria for migrating instructions from CLAUDE.md/AGENTS.md to on-demand mechanisms.
Source: context-aware-improve-optimization.prd.md, analysis-automate-workflow-with-hooks.md, analysis-skill-authoring-best-practices.md, analysis-how-claude-remembers-a-project.md

---

## Contents

- Decision flowchart (classify content type → select mechanism)
- Content type to mechanism mapping (9 content types with evidence)
- Migration candidate indicators (signals that content should migrate)
- Mechanism comparison table (context cost, enforcement, best for)
- Distribution-aware recommendations (plugin vs. standalone)
- Token impact estimation (savings per mechanism type)
- Evidence citations

---

## Decision Flowchart
[Text-based decision tree: Is it always needed? → Is it deterministic? → Is it path-specific? → etc.]

## Content Type to Mechanism Mapping
[Table with 9 rows from PRD lines 348-358, enhanced with web research findings]

## Migration Candidate Indicators
[Table: Indicator → What It Suggests → Threshold for Recommendation]
- Instructions mentioning specific file patterns → path-scoped rule candidate
- Formatting/blocking/notification behaviors → hook candidate
- Domain knowledge blocks >50 lines → skill candidate
- Content agents can infer from code → DELETE candidate
- Instructions with "always"/"never" enforcement semantics → hook candidate
- Workflow instructions invoked <20% of sessions → skill with disable-model-invocation

## Mechanism Comparison
[Enhanced version of DESIGN-GUIDELINES.md Guideline 10 table with ALL mechanisms including:
- Skill (user-invocable: false) — ~100 tokens startup cost
- Skill (disable-model-invocation: true) — zero cost
- Skill (context: fork) — isolated, zero parent cost
- Hook (command type) — zero context cost, deterministic
- Hook (prompt/agent type) — zero context cost, LLM-judged
- Hook (http type) — zero context cost, webhook delivery
- Path-scoped rule (.claude/rules/ with paths:) — on-demand
- Subagent (skills: preload) — isolated context
- Auto memory — first 200 lines at startup]

## Distribution-Aware Recommendations
[Table: Mechanism → Plugin Distribution → Standalone Distribution → Why]
- Plugin: suggest all mechanisms (skills, hooks, rules, subagents)
- Standalone: suggest only skills + rules (no hooks, no subagents)

## Token Impact Estimation
[Table: Migration Type → Tokens Saved from Always-Loaded → Tokens Added to On-Demand]

## Evidence Citations
[Compact table mapping each claim to its source document and line range]
```

- **MIRROR**: `plugins/agents-initializer/skills/improve-claude/references/context-optimization.md` — follow exact header format, Source attribution, `---` divider, `## Contents` TOC, section structure, `*Source:*` inline citations
- **CONSTRAINTS FROM `.claude/rules/reference-files.md`**:
  - No YAML frontmatter
  - Maximum 200 lines
  - `## Contents` TOC required (file will exceed 100 lines)
  - Content framed as "read as instructions"
  - Source attribution on line 3-4
  - No nested references to other reference files
- **GOTCHA**: The file must work for both CLAUDE.md and AGENTS.md improvement flows. Keep mechanism descriptions tool-agnostic where possible, with distribution-specific callouts in the dedicated section.
- **GOTCHA**: Web research found `PreToolUse` decision field deprecation (old `decision: "approve"|"block"` → new `hookSpecificOutput.permissionDecision`). Include current syntax only, not deprecated forms.
- **GOTCHA**: Web research found `paths:` now accepts YAML list with negation (`!pattern`). Include this in the rules mechanism description.
- **VALIDATE**: `wc -l < 201` and manual review of structure against `context-optimization.md` pattern

### Task 2: COPY reference to plugin improve-agents

- **ACTION**: COPY `automation-migration-guide.md` to plugin improve-agents
- **LOCATION**: `plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md`
- **IMPLEMENT**: Byte-identical copy of Task 1 output
- **MIRROR**: Copy-not-symlink convention per `.claude/rules/reference-files.md:12` and `CLAUDE.md` conventions
- **VALIDATE**: `diff plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md` → no differences

### Task 3: COPY reference to standalone improve-claude

- **ACTION**: COPY `automation-migration-guide.md` to standalone improve-claude
- **LOCATION**: `skills/improve-claude/references/automation-migration-guide.md`
- **IMPLEMENT**: Byte-identical copy of Task 1 output
- **VALIDATE**: `diff plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md skills/improve-claude/references/automation-migration-guide.md` → no differences

### Task 4: COPY reference to standalone improve-agents

- **ACTION**: COPY `automation-migration-guide.md` to standalone improve-agents
- **LOCATION**: `skills/improve-agents/references/automation-migration-guide.md`
- **IMPLEMENT**: Byte-identical copy of Task 1 output
- **VALIDATE**: `diff plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md skills/improve-agents/references/automation-migration-guide.md` → no differences

### Task 5: UPDATE `DESIGN-GUIDELINES.md` — add Guideline 13

- **ACTION**: ADD Guideline 13 after the current Guideline 12 section (after line 251, before the `## Research Foundation` section at line 254)
- **IMPLEMENT**: Add the following guideline structure:

```markdown
## Guideline 13: Automation Migration Decision Framework

**Source**: [Anthropic — Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) | [Anthropic — Skills](https://docs.anthropic.com/en/docs/claude-code/skills) | [ETH Zurich Study](docs/Evaluating-AGENTS-paper.pdf) | [docs/analysis/analysis-automate-workflow-with-hooks.md](docs/analysis/analysis-automate-workflow-with-hooks.md)

Instructions in CLAUDE.md/AGENTS.md that are infrequently relevant to the current task should migrate to on-demand mechanisms. The decision criteria map each content type to the most appropriate mechanism based on context cost, enforcement guarantee, and platform compatibility.

| Content Type | Best Mechanism | Context Cost | Evidence |
|---|---|---|---|
| Always-applicable universal rules (<5 lines) | CLAUDE.md root | Per-session | research-llm-context-optimization.md |
| Path-specific conventions (5-50 lines) | `.claude/rules/` with `paths:` | On-demand | analysis-how-claude-remembers-a-project.md |
| Infrequent workflows/domain knowledge (50-500 lines) | Skill (`user-invocable: false`) | ~100 tokens at startup | extend-claude-with-skills.md |
| Heavy/rare workflows with side effects | Skill (`disable-model-invocation: true`) | Zero | extend-claude-with-skills.md |
| Must-enforce behavioral rules | Hook (`PreToolUse`/`PostToolUse`/`Stop`) | Zero | analysis-automate-workflow-with-hooks.md |
| Enforcement needing LLM judgment | Hook (`type: "prompt"` or `type: "agent"`) | Zero | automate-workflow-with-hooks.md |
| Information agents can infer from code | DELETE — do not document | Negative (saves) | analysis-evaluating-agents-paper.md |

Distribution awareness: Plugin suggests all mechanisms; standalone suggests skills + rules only (hooks and subagents are Claude Code-specific).

**Implemented in**: `references/automation-migration-guide.md` (all 4 improve skills), improve Phase 3 (Phase 4 of this PRD)
```

- **MIRROR**: `DESIGN-GUIDELINES.md:197-212` — Guideline 10 structure (Source line, explanation, table, Implemented in)
- **ALSO UPDATE**: Line 291 timestamp to current date, and line 287 analysis corpus count if adding docs
- **GOTCHA**: Insert BEFORE the `## Research Foundation` section (line 254), not after it. Maintain the `---` divider between guidelines.
- **VALIDATE**: `wc -l DESIGN-GUIDELINES.md` — should be ~320 lines (was 293, adding ~27 lines for guideline)

### Task 6: VERIFY sync mechanism covers new artifacts

- **ACTION**: VERIFY that existing hook and rule already match `automation-migration-guide.md`
- **CHECK 1**: `.claude/hooks/check-docs-sync.sh` line 35 — pattern `*/skills/*/references/*.md` matches new file paths ✓
- **CHECK 2**: `.claude/rules/documentation-sync.md` line 6 — `skills/*/references/*.md` path pattern matches ✓
- **CHECK 3**: Hook config in `.claude/settings.json` — `PostToolUse` with `Edit|Write` matcher covers Write operations on new files ✓
- **IMPLEMENT**: No changes needed — existing patterns already cover new artifact paths
- **VALIDATE**: Create a test by running `echo "*/skills/*/references/*.md" | grep -q "automation-migration-guide.md"` mentally — the glob matches. Verify by reading the hook script line 35 and confirming the case pattern.

### Task 7: UPDATE PRD — change Phase 1 status and link plan

- **ACTION**: UPDATE the Implementation Phases table in the PRD file
- **LOCATION**: `.claude/PRPs/prds/context-aware-improve-optimization.prd.md` line 193
- **IMPLEMENT**: Change Phase 1 row:
  - Status: `pending` → `in-progress`
  - PRP Plan: `-` → `.claude/PRPs/plans/phase-1-research-documentation-foundation.plan.md`
- **VALIDATE**: Read the PRD and confirm the table row is updated correctly

---

## Testing Strategy

### Validation Tests

| Test | What It Checks | Command / Method |
|------|---------------|-----------------|
| Reference file length | ≤200 lines per `.claude/rules/reference-files.md` | `wc -l < file` for all 4 copies |
| Reference file format | Header + Source + `---` + Contents TOC | Manual review of lines 1-15 |
| Cross-copy identity | All 4 copies byte-identical | `diff` between all pairs (6 comparisons) |
| TOC completeness | Every `## Section` has a TOC entry | Manual review of TOC vs. sections |
| Evidence citations | Every claim has a `*Source:*` attribution | Manual scan for unattributed claims |
| DESIGN-GUIDELINES structure | Guideline 13 follows existing pattern | Compare with Guideline 10-12 structure |
| Sync mechanism coverage | Hook + rule patterns match new file paths | Read hook script and rule file patterns |

### Edge Cases Checklist

- [ ] Reference file exactly at 200 lines (boundary condition)
- [ ] Distribution-specific content clearly delineated (plugin vs. standalone)
- [ ] No references to other reference files within the new reference (no nesting)
- [ ] Content framed as "read as instructions" not as narrative
- [ ] Source attributions use consistent format (`*Source: filename.md lines X-Y*`)
- [ ] No deprecated hook syntax (use `hookSpecificOutput.permissionDecision`, not `decision`)
- [ ] DESIGN-GUIDELINES.md guideline numbering is sequential (13 follows 12)
- [ ] `## Research Foundation` section remains intact after insertion
- [ ] PRD table alignment not broken by status change

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Check all 4 copies exist and are under 200 lines
for f in \
  plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md \
  plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md \
  skills/improve-claude/references/automation-migration-guide.md \
  skills/improve-agents/references/automation-migration-guide.md; do
  echo "$f: $(wc -l < "$f") lines"
done

# Verify all copies are identical
diff plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md \
     plugins/agents-initializer/skills/improve-agents/references/automation-migration-guide.md
diff plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md \
     skills/improve-claude/references/automation-migration-guide.md
diff plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md \
     skills/improve-agents/references/automation-migration-guide.md
```

**EXPECT**: All files exist, all ≤200 lines, all diffs empty (identical)

### Level 2: STRUCTURE_VALIDATION

```bash
# Verify reference file format: line 1 is title, line 3-4 has Source:, line 6 is ---
head -7 plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md

# Verify ## Contents section exists
grep -c "## Contents" plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md

# Verify no YAML frontmatter (file must NOT start with ---)
head -1 plugins/agents-initializer/skills/improve-claude/references/automation-migration-guide.md | grep -v "^---$"
```

**EXPECT**: Title on line 1, Source on line 3-4, divider on line 6, exactly one `## Contents`, first line is NOT `---`

### Level 3: CONTENT_VALIDATION

```bash
# Verify DESIGN-GUIDELINES.md has Guideline 13
grep "## Guideline 13" DESIGN-GUIDELINES.md

# Verify PRD Phase 1 status updated
grep "Research & Documentation Foundation" .claude/PRPs/prds/context-aware-improve-optimization.prd.md
```

**EXPECT**: Guideline 13 heading found, Phase 1 row shows `in-progress`

### Level 4: SYNC_MECHANISM_VALIDATION

```bash
# Verify hook pattern matches new files
grep -c "references" .claude/hooks/check-docs-sync.sh

# Verify rule paths cover references
grep "references" .claude/rules/documentation-sync.md
```

**EXPECT**: Hook script has references pattern; rule file has references path

### Level 5: CROSS-DISTRIBUTION_VALIDATION

```bash
# List all reference files in improve skills to confirm new file is present
ls -la plugins/agents-initializer/skills/improve-claude/references/
ls -la plugins/agents-initializer/skills/improve-agents/references/
ls -la skills/improve-claude/references/
ls -la skills/improve-agents/references/

# Confirm init skills do NOT have the new reference (it's improve-only)
ls skills/init-claude/references/ | grep automation || echo "Not in init-claude (correct)"
ls skills/init-agents/references/ | grep automation || echo "Not in init-agents (correct)"
```

**EXPECT**: All 4 improve skills have `automation-migration-guide.md`; no init skills have it

### Level 6: MANUAL_VALIDATION

1. Read the canonical `automation-migration-guide.md` end to end
2. Verify every row in the "Content Type to Mechanism Mapping" table has:
   - A specific mechanism recommendation
   - An evidence source citation
   - A distribution note (if mechanism is platform-specific)
3. Verify the "Migration Candidate Indicators" table has actionable detection criteria
4. Verify the "Distribution-Aware Recommendations" section clearly states plugin vs. standalone differences
5. Cross-reference the content against `DESIGN-GUIDELINES.md` Guideline 13 for consistency
6. Verify `DESIGN-GUIDELINES.md` reads coherently with the new guideline inserted

---

## Acceptance Criteria

- [ ] `automation-migration-guide.md` exists in all 4 improve skill reference directories
- [ ] All 4 copies are byte-identical (`diff` returns empty)
- [ ] Reference file is ≤200 lines with `## Contents` TOC
- [ ] Reference follows exact format from `.claude/rules/reference-files.md` (no YAML frontmatter, Source attribution, `---` divider)
- [ ] Decision criteria table covers all 9 content types from PRD lines 348-358
- [ ] Migration candidate indicators are specific and actionable
- [ ] Distribution-aware recommendations clearly separate plugin vs. standalone capabilities
- [ ] `DESIGN-GUIDELINES.md` has Guideline 13 following existing guideline structure
- [ ] Sync mechanism verified to cover new artifact paths
- [ ] PRD Phase 1 status updated to `in-progress` with plan link
- [ ] No init skills received the new reference (improve-only)

---

## Completion Checklist

- [ ] Task 1: Canonical `automation-migration-guide.md` created (plugin improve-claude)
- [ ] Task 2: Copy to plugin improve-agents — verified identical
- [ ] Task 3: Copy to standalone improve-claude — verified identical
- [ ] Task 4: Copy to standalone improve-agents — verified identical
- [ ] Task 5: DESIGN-GUIDELINES.md updated with Guideline 13
- [ ] Task 6: Sync mechanism verified (no changes needed)
- [ ] Task 7: PRD updated (Phase 1 → in-progress, plan linked)
- [ ] Level 1: Static analysis passes (line counts, identity checks)
- [ ] Level 2: Structure validation passes (format, TOC, no frontmatter)
- [ ] Level 3: Content validation passes (Guideline 13 exists, PRD updated)
- [ ] Level 4: Sync mechanism covers new paths
- [ ] Level 5: Cross-distribution validation passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Reference file exceeds 200-line limit | MEDIUM | HIGH (violates hard rule) | Start with the PRD's 9-row table as core; add indicators and comparison sparingly. Use compact table format. If approaching limit, move Evidence Citations section to inline `*Source:*` notes. |
| Web research findings become stale (hook events, skill fields) | LOW | MEDIUM | Reference cites official docs by URL; implementation agent can verify at execution time. Mark version-specific features with `(v2.1.84+)` annotations. |
| DESIGN-GUIDELINES.md insertion breaks formatting | LOW | LOW | Insert before `## Research Foundation` with proper `---` divider. Validate markdown rendering after edit. |
| Copy-not-symlink drift during development | MEDIUM | HIGH | Tasks 2-4 are explicit copy steps with diff validation. Level 1 validation catches any drift. |

---

## Notes

- The `automation-migration-guide.md` reference file is the foundational artifact for the entire Context-Aware Improve feature. Phases 4-5 depend on its content for classification logic and user presentation.
- Web research revealed 24 hook events (up from ~6 in existing docs), a new `http` hook type, the `effort` skill frontmatter field, and `paths` YAML list syntax with negation. These are incorporated into the reference's mechanism comparison section.
- The existing sync mechanism (PostToolUse hook + path-scoped rule) already covers the new reference file paths — no hook or rule changes needed.
- DESIGN-GUIDELINES.md already has Guideline 10 covering on-demand context loading. Guideline 13 focuses specifically on the **decision framework** for choosing between mechanisms, complementing Guideline 10's **mechanism descriptions**.
- The PRD requires creating a GitHub sub-issue of #11 for this plan. Execute after plan approval: `gh issue create --title "Phase 1: Research & Documentation Foundation" --body "..." --repo rodrigorjsf/project-agents-initializer` and link to #11.
- The PRD also requires attaching the plan to GitHub issue #11.
