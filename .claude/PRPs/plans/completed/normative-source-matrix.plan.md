# Feature: Normative Source Matrix

## Summary

Create the authoritative normative source matrix that maps every repository scope and artifact type to its correct documentation sources, precedence model, forbidden sources, and contamination boundaries. This single document becomes the foundation for all subsequent compliance phases — every validator resolves its source bundle from this matrix without guessing.

## User Story

As a compliance validator (human or automated)
I want to look up any (scope × artifact type) and immediately know which sources are authoritative, which are supporting, and which are forbidden
So that every audit produces consistent, traceable findings against the correct normative base

## Problem Statement

The repository ships 4 distributions with different artifact rules, but the mapping from "which artifact am I reviewing?" to "which docs are authoritative?" is scattered across 9 rule files, 9 instruction files, plugin CLAUDE.md files, and implicit conventions. A validator must assemble this knowledge from 20+ files every time — leading to inconsistent scope decisions and contamination risk.

## Solution Statement

Create `docs/compliance/normative-source-matrix.md` — a single authority model document with: scope registry (5 scopes including repository-global), source catalog with stable IDs, precedence model, per-scope artifact matrices, contamination rules, named source bundles, and explicitly excluded sources.

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | docs/, compliance program (PRD #56 Phase 1) |
| Dependencies | None (Phase 1 has no deps) |
| Estimated Tasks | 3 |
| Source PRD | `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` |
| Source Issue | [#56](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56) |
| PRD Phase | 1 of 10 — Normative Source Matrix |

---

## UX Design

### Before State

```
Validator wants to audit plugins/cursor-initializer/agents/codebase-analyzer.md

  ┌─ Where are the rules? ─────────────────────────────────┐
  │                                                         │
  │  .claude/rules/cursor-agent-files.md  ← knows this     │
  │  .github/instructions/agent-definitions.instructions.md │
  │  docs/cursor/subagents/subagents-guide.md  ← maybe?    │
  │  docs/shared/skill-authoring-best-practices.md ← ??    │
  │  docs/claude-code/subagents/...  ← WRONG SCOPE!        │
  │  DESIGN-GUIDELINES.md  ← which parts apply?            │
  │                                                         │
  │  Result: Validator must assemble from 20+ files         │
  │          Risk of loading wrong-scope sources            │
  └─────────────────────────────────────────────────────────┘
```

### After State

```
Validator wants to audit plugins/cursor-initializer/agents/codebase-analyzer.md

  ┌─ Look up: scope=cursor-initializer, artifact=agent ────┐
  │                                                         │
  │  normative-source-matrix.md                             │
  │  ├─ Primary: CURSOR-SUBAGENTS, CURSOR-PLUGIN           │
  │  ├─ Secondary: SHARED-SKILLS-STD, GENERAL-SUBAGENTS    │
  │  ├─ Project: rule:cursor-agent-files,                   │
  │  │           instr:agent-definitions                    │
  │  ├─ Forbidden: CLAUDE-SUBAGENTS, CLAUDE-HOOKS           │
  │  └─ Bundle: "cursor-agent-bundle"                       │
  │                                                         │
  │  Result: Deterministic source resolution in one lookup  │
  └─────────────────────────────────────────────────────────┘
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Compliance audit start | Validator manually assembles source list from scattered files | Validator looks up scope × artifact in matrix | Eliminates guesswork, prevents wrong-scope loading |
| Quality gate execution | Gate may load incorrect sources for scope | Gate resolves named bundle from matrix | Consistent source bundles across runs |
| New artifact review | Reviewer unsure which docs apply | Matrix provides definitive answer | Faster, more accurate reviews |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `DESIGN-GUIDELINES.md` | 1-70 | Structure pattern with source citations and traceability |
| P0 | `.claude/rules/plugin-skills.md` | all | Claude plugin skill constraints |
| P0 | `.claude/rules/cursor-plugin-skills.md` | all | Cursor plugin skill constraints |
| P0 | `.claude/rules/standalone-skills.md` | all | Standalone skill constraints |
| P0 | `.claude/rules/agent-files.md` | all | Claude agent constraints |
| P0 | `.claude/rules/cursor-agent-files.md` | all | Cursor agent constraints |
| P0 | `.claude/rules/reference-files.md` | all | Cross-distribution reference constraints |
| P1 | `.github/instructions/skill-files.instructions.md` | all | Contamination boundaries for skills |
| P1 | `.github/instructions/agent-definitions.instructions.md` | all | Contamination boundaries for agents |
| P1 | `.github/instructions/template-files.instructions.md` | all | Distribution-aware template rules |
| P1 | `plugins/agents-initializer/CLAUDE.md` | all | Plugin-specific conventions |
| P1 | `plugins/cursor-initializer/CLAUDE.md` | all | Cursor-specific conventions |
| P1 | `plugins/agent-customizer/CLAUDE.md` | all | Agent-customizer conventions |

---

## Patterns to Mirror

**DOCUMENT_STRUCTURE (tables with source citations):**
```markdown
<!-- SOURCE: DESIGN-GUIDELINES.md:8-18 -->
<!-- COPY THIS PATTERN: table with evidence, then "In practice" + "Implemented in" -->

| Configuration                    | Success Impact | Cost Impact |
| -------------------------------- | -------------- | ----------- |
| No config file                   | Baseline       | Baseline    |
| LLM-generated comprehensive file | **-3%**        | **+20%**    |

**In practice**: Every generated instruction must pass the test...
**Implemented in**: All 4 init skills...
```

**RULE_FILE_STRUCTURE (path-scoped assertions):**
```markdown
<!-- SOURCE: .claude/rules/cursor-agent-files.md:1-12 -->
<!-- COPY THIS PATTERN: YAML frontmatter + bullet list of constraints -->
---
paths:
  - "plugins/cursor-initializer/agents/*.md"
---
# Cursor Agent File Conventions
- YAML frontmatter required: `name`, `description`, `model`, `readonly`
- `model: inherit` — Cursor agents inherit model from parent context
```

**DOCS_ANALYSIS_STRUCTURE (status + source + scope header):**
```markdown
<!-- SOURCE: docs/analysis/analysis-evaluating-agents-paper.md:1-6 -->
<!-- COPY THIS PATTERN: metadata header with status, source, scope -->
# Analysis: Evaluating AGENTS.md
> **Status**: Current
> **Source document**: [Gloaguen et al. ...]
> **Analysis date**: 2026-02-01
> **Scope**: Rigorous evaluation of...
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `docs/compliance/normative-source-matrix.md` | CREATE | The authoritative matrix — foundation for all compliance phases |

---

## NOT Building (Scope Limits)

- Per-distribution matrix splits — single document is the authority; splits create drift risk
- Automated validator code — Phase 3 defines the validator protocol; this phase only defines the source model
- Source file content audits — Phase 4-6 handle artifact-by-artifact audits; this phase defines WHICH sources, not WHETHER artifacts comply
- RAG routing changes — Phase 8 handles RAG hardening; this phase is the input model for that work

---

## Step-by-Step Tasks

### Task 1: CREATE `docs/compliance/normative-source-matrix.md`

- **ACTION**: Create the full normative source matrix document
- **IMPLEMENT**: The document must contain these sections in order:
  1. **Purpose and Precedence Model** — define the 4-tier precedence: (1) platform-specific docs, (2) shared/open standards, (3) project design guidance + general-LLM, (4) analysis docs as supporting only
  2. **Scope Registry** — enumerate 5 scopes: `agents-initializer` (Claude plugin), `agent-customizer` (Claude plugin), `cursor-initializer` (Cursor plugin), `standalone` (portable skills), `repository-global` (governance artifacts)
  3. **Normative Source Catalog** — assign stable IDs to every source category: `CLAUDE-HOOKS`, `CLAUDE-PLUGINS`, `CLAUDE-SKILLS`, `CLAUDE-SUBAGENTS`, `CLAUDE-MEMORY`, `CLAUDE-PROMPTING`, `CURSOR-RULES`, `CURSOR-SKILLS`, `CURSOR-SUBAGENTS`, `CURSOR-HOOKS`, `CURSOR-PLUGIN`, `CURSOR-TOOLS`, `SHARED-SKILLS-STD`, `SHARED-AUTHORING`, `GENERAL-AGENTS-PAPER`, `GENERAL-CONTEXT`, `GENERAL-SUBAGENTS`, `GENERAL-PROMPTING`, `GENERAL-WORKFLOWS`, `PROJECT-DESIGN-GUIDELINES`, plus rules (`rule:*`) and instructions (`instr:*`)
  4. **Artifact Type Registry** — enumerate all artifact types: SKILL.md, agent-definition, reference-file, template-file, plugin-manifest, CLAUDE.md/AGENTS.md, README, rule-file, instruction-file
  5. **Normative Matrix** — one table per scope, each row = artifact type, columns = primary sources, secondary sources, project rules, forbidden sources
  6. **Contamination Rules** — explicit Claude↔Cursor isolation rules, plugin↔standalone isolation rules, init↔improve lifecycle rules, output target rules
  7. **Named Source Bundles** — define loadable bundles: `claude-plugin-bundle`, `cursor-plugin-bundle`, `standalone-bundle`, `agent-customizer-bundle`, `governance-bundle`
  8. **Excluded Sources** — explicitly list what is NEVER normative: `docs/plans/`, completed PRPs/PRDs, ad hoc reports, next-steps.md
- **MIRROR**: `DESIGN-GUIDELINES.md:1-18` — use table-based structure with source citations
- **GOTCHA**: Use stable source IDs as primary keys, not raw file paths (paths go stale per `documentation.instructions.md:30-35`). Map IDs → canonical paths in the catalog section only.
- **GOTCHA**: Analysis docs (`docs/analysis/`) are supporting/interpretive, never sole authority — mark them as Tier 4 explicitly.
- **GOTCHA**: `.claude/rules/` and `.github/instructions/` are project normative sources (not just "docs") — include them in the catalog under project rules category.
- **VALIDATE**: `grep -c "^|" docs/compliance/normative-source-matrix.md` should show extensive table coverage; `grep -c "FORBIDDEN\|forbidden" docs/compliance/normative-source-matrix.md` should show forbidden markers in every scope table

### Task 2: Validate matrix completeness

- **ACTION**: Cross-check the matrix against the actual repository
- **IMPLEMENT**: Verify:
  - Every artifact found via `find plugins skills -name "SKILL.md" -o -name "*.md" -path "*/agents/*"` has a matching matrix row
  - Every docs/ file is categorized in the source catalog
  - No source appears in both "primary" and "forbidden" for the same scope
  - Every `.claude/rules/` file is referenced as a project rule in at least one scope
  - Every `.github/instructions/` file is referenced in at least one scope
  - The 5 scopes cover all directories: `plugins/agents-initializer/`, `plugins/cursor-initializer/`, `plugins/agent-customizer/`, `skills/`, and root governance files
- **MIRROR**: N/A (validation, not creation)
- **VALIDATE**: All checks pass with no gaps

### Task 3: Update PRD and commit

- **ACTION**: Update PRD Phase 1 status from `pending` to `complete`, add plan path
- **IMPLEMENT**: Edit `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` Implementation Phases table row for Phase 1
- **MIRROR**: Existing PRD table format
- **VALIDATE**: `grep "complete" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` shows Phase 1

---

## Testing Strategy

### Completeness Tests

| Check | Method | Validates |
|-------|--------|-----------|
| Scope coverage | Count scopes in matrix = 5 | All distributions + governance covered |
| Artifact type coverage | Count unique artifact types per scope ≥ 5 | No artifact type missed |
| Source catalog completeness | Every docs/ subdirectory has IDs | No source uncategorized |
| Contamination rules | Claude↔Cursor + plugin↔standalone + init↔improve all present | All isolation boundaries defined |
| Bundle definitions | 5 named bundles defined | Validators can load by name |
| Forbidden sources | Every scope has at least 1 forbidden entry | No scope allows everything |

### Edge Cases Checklist

- [ ] Repository-global artifacts (rules, instructions, root CLAUDE.md) — covered by governance scope
- [ ] Shared references that exist in multiple distributions — covered by parity notes
- [ ] Cross-cutting docs (DESIGN-GUIDELINES.md) — classified at correct precedence tier
- [ ] Analysis docs — marked as supporting/interpretive only, never sole authority
- [ ] Historical artifacts (completed plans, old PRDs) — explicitly excluded

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
# Verify document exists and has substantial content
test -f docs/compliance/normative-source-matrix.md && wc -l docs/compliance/normative-source-matrix.md
```

**EXPECT**: File exists, 100+ lines

### Level 2: STRUCTURAL_VALIDATION

```bash
# Verify all required sections exist
grep -c "## Purpose\|## Scope Registry\|## Normative Source Catalog\|## Artifact Type\|## Normative Matrix\|## Contamination\|## Named Source Bundles\|## Excluded" docs/compliance/normative-source-matrix.md
```

**EXPECT**: 8 section headers found

### Level 3: CONTENT_VALIDATION

```bash
# Verify all 5 scopes have matrix tables
grep -c "agents-initializer\|cursor-initializer\|agent-customizer\|standalone\|repository-global" docs/compliance/normative-source-matrix.md
```

**EXPECT**: Multiple matches for each scope

### Level 6: MANUAL_VALIDATION

- Pick 3 random artifacts from different distributions
- Look up each in the matrix
- Confirm the primary/forbidden sources match what `.claude/rules/` and `.github/instructions/` define
- Confirm no contradictions

---

## Acceptance Criteria

- [ ] `docs/compliance/normative-source-matrix.md` exists with all 8 required sections
- [ ] 5 scopes defined (agents-initializer, cursor-initializer, agent-customizer, standalone, repository-global)
- [ ] Every artifact type mapped per scope with primary, secondary, project, and forbidden sources
- [ ] Precedence model explicitly defined (4 tiers)
- [ ] Contamination boundaries match existing rules (Claude↔Cursor, plugin↔standalone, init↔improve)
- [ ] 5 named source bundles defined and enumerable
- [ ] Historical/planning artifacts explicitly excluded
- [ ] No contradiction with existing `.claude/rules/` or `.github/instructions/` content
- [ ] PRD Phase 1 updated to `complete`

---

## Completion Checklist

- [ ] Task 1 completed: matrix document created
- [ ] Task 2 completed: completeness validated
- [ ] Task 3 completed: PRD updated
- [ ] Level 1: File exists with substantial content
- [ ] Level 2: All 8 sections present
- [ ] Level 3: All 5 scopes have matrix entries
- [ ] Level 6: Manual spot-check confirms accuracy
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Matrix becomes stale as docs evolve | MEDIUM | HIGH | Use stable source IDs, not raw paths; paths only in catalog section |
| Matrix too long for practical use | LOW | MEDIUM | Use tables, not prose; keep main matrix compact |
| Missing edge cases in contamination rules | LOW | HIGH | Cross-reference every `.claude/rules/` boundary explicitly |
| Disagreement between matrix and existing rules | LOW | HIGH | Task 2 validates consistency; fix rules if matrix reveals gaps |

---

## Notes

- This is Phase 1 of a 10-phase compliance program (PRD #56)
- The matrix is a reference document for human validators and future automated gates
- Rubber-duck critique identified key improvements: add precedence model, repository-global scope, stable source IDs, and explicitly forbidden historical artifacts
- The matrix does NOT audit artifacts — it defines the authority model that Phases 4-6 audit against
- Analysis docs are intentionally Tier 4 (supporting only) — they accelerate understanding but are never sole authority for artifact compliance
