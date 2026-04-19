# Feature: Regression Prevention Workflow (PRD Phase 9)

## Summary

Close all Phase 9 compliance gaps by auditing 20 assigned artifacts, adding a cursor-initializer
quality gate skill, creating a repository-global validation protocol, adding drift detection to
the agents-initializer and standalone quality gates, and layering in a regression prevention
workflow document, rule, and instruction file. All work is additive — no existing artifact is
deleted; only the two existing quality gate SKILL.md files require surgical updates.

## User Story

As a repository maintainer
I want automated quality gates and documented workflows for every scope
So that compliance drift cannot silently re-enter the repository after the Phase 4–8 corrections

## Problem Statement

After Phases 4–8 corrected all open compliance violations, there is no systematic mechanism to
prevent regression. Three structural gaps remain: (1) cursor-initializer has no quality gate —
all coverage is manual; (2) repository-global artifacts have no validation protocol; (3) the two
existing quality gates lack drift detection for agents-initializer and standalone reference
files. Without Phase 9, the next codebase change can silently break conventions that took
significant effort to establish.

## Solution Statement

Create a cursor-initializer quality gate skill (3-phase, mirrors quality-gate pattern), a
repository-global validation protocol document, drift manifests for agents-initializer and
standalone, and a regression prevention workflow document that ties all gates together with a
change-type matrix and manual fallback. Layer in a compliance maintenance rule and instruction
file to auto-load the workflow doc in the right contexts. Update both existing quality gate
SKILL.md files with a mandatory regression checkpoint step and Phase 3 drift detection (for
quality-gate). Perform all 20 Phase 9-assigned artifact audits using the CF-NNN finding model —
document any violations found.

## Metadata

| Field            | Value                                                                                        |
| ---------------- | -------------------------------------------------------------------------------------------- |
| Type             | ENHANCEMENT                                                                                  |
| Complexity       | HIGH                                                                                         |
| Systems Affected | quality-gate skills, compliance docs, rules, instructions, drift manifests, audit artifacts  |
| Dependencies     | Phases 4–8 complete (all `complete`)                                                         |
| Estimated Tasks  | 18                                                                                           |
| Parent PRD       | `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`                   |
| Parent Issue     | [#56](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/56)                    |
| Plan Issue       | [#71](https://github.com/rodrigorjsf/agent-engineering-toolkit/issues/71)                    |

---

## UX Design

### Before State

```
Change is made to a cursor-initializer artifact
        ↓
No quality gate exists → compliance drift silently enters
        ↓
Repository-global artifacts (rules, hooks, instructions) also have no gate
        ↓
agents-initializer and standalone quality gates run but skip reference file drift detection
        ↓
Regressions accumulate between manual audit cycles
```

### After State

```
Change is made to any artifact in any scope
        ↓
Implementer consults regression-prevention-workflow.md → selects change type → follows checklist
        ↓
Runs scope-appropriate quality gate:
  cursor-initializer →  cursor-initializer-quality-gate  (NEW)
  agents-initializer →  quality-gate (updated: +drift, +regression checkpoint)
  agent-customizer   →  agent-customizer-quality-gate    (+regression checkpoint)
  repository-global  →  repository-global-validation-protocol.md (NEW manual protocol)
        ↓
All 4 scopes have gate coverage; drift reported before merge
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| cursor-initializer scope | Manual audit only | `cursor-initializer-quality-gate` skill | Automated compliance check available |
| repository-global scope | No protocol | `repository-global-validation-protocol.md` | Documented manual checklist |
| quality-gate skill | 3 phases (inspect, parity, scenarios) | 4 phases (+drift detection) | agents-initializer/standalone ref drift caught |
| Both QG SKILL.md files | No regression checkpoint | Mandatory Phase N+1 step | Workflow doc consulted automatically |
| Compliance rules | No rule for maintenance paths | `compliance-maintenance.md` rule | Correct convention files auto-loaded |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude/skills/quality-gate/SKILL.md` | all (119) | MIRROR exactly for cursor-initializer QG |
| P0 | `.claude/skills/agent-customizer-quality-gate/SKILL.md` | all (132) | MIRROR drift phase pattern |
| P0 | `plugins/agent-customizer/docs-drift-manifest.md` | all | MIRROR format for new drift manifests |
| P0 | `docs/compliance/finding-model-and-validator-protocol.md` | 1-130 | CF-NNN format + 7-step validator protocol |
| P1 | `docs/compliance/artifact-audit-manifest.md` | 450-500, 630-680 | Phase 9 artifact list + gap map |
| P1 | `docs/compliance/normative-source-matrix.md` | all | Authoritative sources per scope |
| P1 | `.claude/skills/quality-gate/agents/artifact-inspector.md` | all | Mirror prompt structure for new QG agents |
| P1 | `.claude/skills/quality-gate/agents/parity-checker.md` | all | Mirror for cursor QG parity agent |
| P1 | `.claude/skills/quality-gate/references/quality-gate-criteria.md` | all | Mirror for cursor QG criteria reference |
| P2 | `.claude/rules/rag-routing.md` | 9-14 | Mirror format for compliance-maintenance rule |
| P2 | `.github/instructions/prp-artifacts.instructions.md` | all | Mirror format for compliance-prevention instruction |

---

## Patterns to Mirror

**RULE_FILE_FORMAT:**
```yaml
# SOURCE: .claude/rules/rag-mcp-server.md:1-8
# COPY THIS PATTERN:
---
paths:
  - ".mcp.json"
  - "rag/server.py"
---
# Section Title
- Direct imperative assertion
- Another assertion
```

**QUALITY_GATE_SKILL_PHASE:**
```markdown
# SOURCE: .claude/skills/quality-gate/SKILL.md:28-38
# COPY THIS PATTERN:
## Phase 1: Static Artifact Inspection

Read `.claude/skills/quality-gate/agents/artifact-inspector.md`. Skip the YAML frontmatter
block (between the first and second `---` delimiters). Pass the remaining content as the task
to a general-purpose agent via the Task tool.

**Wait for completion.** Collect structured output as `artifact_report`, which contains:
- Compliance matrix per category
- Violation list: file path, rule violated, rule source, severity, evidence
```

**DRIFT_MANIFEST_FORMAT:**
```markdown
# SOURCE: plugins/agent-customizer/docs-drift-manifest.md (table rows)
# COPY THIS PATTERN:
| Reference File | Source Docs | Status |
|---|---|---|
| `path/to/reference.md` | `docs/source-doc.md:10-45` | baseline |
```

**AGENT_DEFINITION_FRONTMATTER:**
```yaml
# SOURCE: .claude/skills/quality-gate/agents/artifact-inspector.md:1-6
# COPY THIS PATTERN:
---
name: artifact-inspector
description: "..."
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 20
---
```

**INSTRUCTIONS_FILE_FORMAT:**
```yaml
# SOURCE: .github/instructions/prp-artifacts.instructions.md:1-5
# COPY THIS PATTERN:
---
applyTo: "glob/pattern/**/*.md"
---
# Title

## Section
- Review guard as direct assertion
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `docs/compliance/regression-prevention-workflow.md` | CREATE | Central workflow doc: change type matrix, scope-gate map, manual fallback |
| `.claude/rules/compliance-maintenance.md` | CREATE | Auto-loads compliance conventions for docs/compliance, quality-gate, wiki paths |
| `.github/instructions/compliance-prevention.instructions.md` | CREATE | Review guards for compliance artifact changes |
| `.claude/skills/cursor-initializer-quality-gate/SKILL.md` | CREATE | Quality gate for cursor-initializer scope (gap closure) |
| `.claude/skills/cursor-initializer-quality-gate/agents/artifact-inspector.md` | CREATE | Static inspection agent for cursor-initializer artifacts |
| `.claude/skills/cursor-initializer-quality-gate/agents/parity-checker.md` | CREATE | Parity checker for cursor-initializer shared references |
| `.claude/skills/cursor-initializer-quality-gate/agents/scenario-evaluator.md` | CREATE | Red-green scenario evaluator for cursor-initializer |
| `.claude/skills/cursor-initializer-quality-gate/references/quality-gate-criteria.md` | CREATE | Expected results checklist + report template for cursor QG |
| `docs/compliance/repository-global-validation-protocol.md` | CREATE | Manual validation checklist for repository-global scope |
| `plugins/agents-initializer/docs-drift-manifest.md` | CREATE | Drift manifest for agents-initializer reference files |
| `skills/docs-drift-manifest.md` | CREATE | Drift manifest for standalone reference files |
| `.claude/skills/quality-gate/SKILL.md` | UPDATE | Add Phase 3: Docs Drift + mandatory regression checkpoint |
| `.claude/skills/agent-customizer-quality-gate/SKILL.md` | UPDATE | Add mandatory regression checkpoint step |
| `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | UPDATE | Phase 9 status: pending → in-progress; add plan path |

---

## NOT Building (Scope Limits)

- **Automation hooks for compliance checks** — the regression-prevention-workflow.md is a manual
  protocol document; automated enforcement is Phase 10 scope
- **Cursor-initializer drift checker agent** — cursor plugin has no docs-drift-manifest yet
  (manifests require verified source attributions; creating them is a separate research task)
- **New test scenarios for cursor scope** — scenarios exist for agents-initializer + standalone;
  adding cursor scenarios would require a dedicated scenario authoring pass (Phase 10 scope)
- **Fixing violations found during audits** — Phase 9 DOCUMENTS findings as CF-NNN; correction
  is Phase 10 scope
- **Expanding quality-gate SKILL.md beyond drift addition** — no structural refactor; only
  Phase 3 insertion and regression checkpoint addition

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

---

### Group A: Artifact Audits (20 Phase 9-assigned artifacts)

#### Task A1: Audit `.claude/rules/rag-mcp-server.md` and `.claude/rules/rag-storage-and-search.md`

- **ACTION**: Validate both rule files against `i:rl` validator criteria
- **IMPLEMENT**: Check: (1) YAML `paths:` frontmatter present; (2) direct assertions only, no prose; (3) path patterns match actual file locations; (4) no duplicate content with CLAUDE.md. Use `docs/compliance/finding-model-and-validator-protocol.md` 7-step protocol. Document each violation as CF-NNN finding.
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:50-90` — CF-NNN format with 15 fields
- **GOTCHA**: `rag-mcp-server.md` has paths `[".mcp.json","rag/server.py","rag/cli.py"]` — verify these exist with `ls`; `rag-storage-and-search.md` has 6 paths — verify all exist
- **VALIDATE**: `ls .claude/rules/rag-mcp-server.md .claude/rules/rag-storage-and-search.md && grep -c "^paths:" .claude/rules/rag-mcp-server.md .claude/rules/rag-storage-and-search.md`

#### Task A2: Audit `.github/instructions/prp-artifacts.instructions.md`

- **ACTION**: Validate against `i:inst` validator criteria
- **IMPLEMENT**: Check: (1) YAML `applyTo:` frontmatter present; (2) glob pattern is specific; (3) review guard format (direct assertions, not prose); (4) no standard conventions already inferrable from code. Document violations as CF-NNN.
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:95-111` — 7-step validator protocol
- **GOTCHA**: `applyTo:` value is `"**/*.prd.md,**/*.plan.md,.claude/PRPs/**/*.md"` — verify this pattern actually matches the files it claims to guard
- **VALIDATE**: `grep "applyTo:" .github/instructions/prp-artifacts.instructions.md`

#### Task A3: Audit hooks — `check-docs-sync.sh` and `check-rag-reindex.sh`

- **ACTION**: Validate both hook scripts against `i:hk` validator criteria
- **IMPLEMENT**: Check: (1) exit code semantics correct (PostToolUse hooks must exit 0 — exit 2 has no effect on non-blocking hooks); (2) tool_name filtering present; (3) no side effects beyond notification/logging; (4) stdin parsing via `jq` correct. Document violations as CF-NNN.
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md:50-90` — finding model
- **GOTCHA**: `check-docs-sync.sh` exit comment at line 60 explicitly notes exit 2 is ineffective for PostToolUse — this is intentional documentation; do not flag as a violation
- **VALIDATE**: `bash -n .claude/hooks/check-docs-sync.sh && bash -n .claude/hooks/check-rag-reindex.sh` (syntax check only)

#### Task A4: Audit both quality-gate skill families

Audit all artifacts in `.claude/skills/quality-gate/` AND `.claude/skills/agent-customizer-quality-gate/`:

- **ACTION**: Validate SKILL.md files against `i:sk` criteria; agent files against `i:ag` criteria; quality-gate-criteria.md against `i:rf` criteria
- **IMPLEMENT**:
  - SKILL.md checks: YAML frontmatter valid; body <500 lines; phase-based workflow; delegates to named agents (not inline bash); self-validation phase references criteria file
  - Agent checks: YAML frontmatter with `name`, `description`, `tools`, `model`, `maxTurns`; `model: sonnet`; tools restricted to Read/Grep/Glob/Bash; `maxTurns: 20`
  - Reference check: quality-gate-criteria.md ≤200 lines; >100 lines → `## Contents` TOC present; source attribution present
  - Document violations as CF-NNN
- **MIRROR**: `.claude/rules/agent-files.md` — agent constraint rules; `.claude/rules/reference-files.md` — reference file rules
- **GOTCHA**: `quality-gate/agents/parity-checker.md` is 236 lines (exceeds 200-line limit for reference files) — but this is an AGENT file, not a reference file; apply agent rules not reference rules
- **VALIDATE**: `wc -l .claude/skills/quality-gate/SKILL.md .claude/skills/agent-customizer-quality-gate/SKILL.md .claude/skills/quality-gate/agents/*.md .claude/skills/agent-customizer-quality-gate/agents/*.md .claude/skills/quality-gate/references/quality-gate-criteria.md`

#### Task A5: Audit dev-skills — `receiving-code-review` and `update-review-instructions`

- **ACTION**: Validate both dev-skill SKILL.md files and `update-review-instructions` references against `i:sk` criteria
- **IMPLEMENT**: Check: (1) YAML frontmatter valid (`name` ≤64 chars, `description` ≤1024 chars); (2) body <500 lines; (3) phase-based workflow present; (4) references files load from correct relative path convention; (5) for `update-review-instructions` — references directory exists and ≤200 lines each. Document violations as CF-NNN.
- **MIRROR**: `.github/instructions/skill-files.instructions.md` — SKILL.md validation criteria
- **GOTCHA**: `receiving-code-review` has no `references/` dir — this skill is inline; check if this violates convention (standalone dev-skills may be inline)
- **VALIDATE**: `wc -l .claude/skills/receiving-code-review/SKILL.md .claude/skills/update-review-instructions/SKILL.md && ls .claude/skills/update-review-instructions/references/`

---

### Group B: Cursor-Initializer Quality Gate (new skill)

#### Task B1: CREATE `.claude/skills/cursor-initializer-quality-gate/SKILL.md`

- **ACTION**: Create the cursor-initializer quality gate meta-skill
- **IMPLEMENT**: Mirror `.claude/skills/quality-gate/SKILL.md` structure exactly, adapted for cursor-initializer scope:
  - YAML frontmatter: `name: cursor-initializer-quality-gate`, `description` describing cursor-initializer scope
  - Scope header: covers `plugins/cursor-initializer/` — SKILL.md files, agent files, references, templates
  - Convention sources: `.claude/rules/cursor-plugin-skills.md`, `plugins/cursor-initializer/CLAUDE.md`
  - Phase 1: Static Artifact Inspection → delegate to `cursor-initializer-quality-gate/agents/artifact-inspector.md`
  - Phase 2: Cross-Distribution Parity → delegate to `cursor-initializer-quality-gate/agents/parity-checker.md`
  - Phase 3: Red-Green Test Evaluation → delegate to `cursor-initializer-quality-gate/agents/scenario-evaluator.md` with scenarios from `.claude/PRPs/tests/scenarios/`
  - Phase 4: Findings Synthesis → compute Quality Gate Dashboard (same format as quality-gate)
  - Phase 5: Findings Report → write to `.specs/reports/cursor-initializer-quality-gate-[YYYY-MM-DD]-findings.md`
  - Add regression checkpoint final step: "Before concluding, read `docs/compliance/regression-prevention-workflow.md` Section 'Post-Gate Actions' and confirm all post-gate actions are complete."
  - Routing guidance: `search_docs("compliance routing cursor-initializer")`
  - Test scenarios: use scenarios that have cursor or improve scope (`.claude/PRPs/tests/scenarios/`)
- **MIRROR**: `.claude/skills/quality-gate/SKILL.md` — copy phase structure exactly; adapt scope headers
- **GOTCHA**: Do NOT include Phase 3: Docs Drift — cursor-initializer has no drift manifest yet; omit that phase entirely; 4 phases only (inspect, parity, scenarios, synthesis/report)
- **VALIDATE**: `wc -l .claude/skills/cursor-initializer-quality-gate/SKILL.md` (must be <500)

#### Task B2: CREATE cursor-initializer-quality-gate agents and criteria reference

- **ACTION**: Create 3 agent definition files + 1 reference file
- **IMPLEMENT**:
  - `agents/artifact-inspector.md`: Mirror `.claude/skills/quality-gate/agents/artifact-inspector.md` exactly; adapt convention sources (`.claude/rules/cursor-plugin-skills.md`, `plugins/cursor-initializer/CLAUDE.md`), artifact paths (`plugins/cursor-initializer/skills/*/SKILL.md`, `plugins/cursor-initializer/agents/*.md`), and checklist items for cursor-specific rules (Cursor agent frontmatter: `model: inherit`, `readonly: true`, no `tools`/`maxTurns`; SKILL.md cursor patterns)
  - `agents/parity-checker.md`: Mirror `.claude/skills/quality-gate/agents/parity-checker.md`; adapt for cursor-initializer shared reference copies between `init-cursor/` and `improve-cursor/` skill directories
  - `agents/scenario-evaluator.md`: Mirror `.claude/skills/quality-gate/agents/scenario-evaluator.md`; adapt skill paths to `plugins/cursor-initializer/skills/`
  - `references/quality-gate-criteria.md`: Mirror `.claude/skills/quality-gate/references/quality-gate-criteria.md`; replace plugin-skill checks with cursor-specific checks (P5/P6/P7 become cursor delegation checks; agent checks become `model: inherit`/`readonly: true` checks); include `## Contents` TOC if >100 lines
- **MIRROR**: `.claude/skills/quality-gate/agents/artifact-inspector.md` — full structure; `.claude/rules/cursor-plugin-skills.md` — cursor-specific rules to check
- **GOTCHA**: Cursor agents use `model: inherit` and `readonly: true` — NOT `model: sonnet`/`maxTurns`; the cursor agent inspector must check these different fields. Do not copy Claude-agent checks blindly.
- **VALIDATE**: `ls .claude/skills/cursor-initializer-quality-gate/agents/ && ls .claude/skills/cursor-initializer-quality-gate/references/ && wc -l .claude/skills/cursor-initializer-quality-gate/references/quality-gate-criteria.md`

---

### Group C: Repository-Global Validation Protocol

#### Task C1: CREATE `docs/compliance/repository-global-validation-protocol.md`

- **ACTION**: Create a structured manual validation protocol for repository-global artifacts
- **IMPLEMENT**: Document the validation protocol for repository-global scope artifacts:
  - **Scope**: `.claude/rules/` (non-plugin-specific), `.claude/hooks/`, `.github/instructions/`, root `CLAUDE.md`, `DESIGN-GUIDELINES.md`, `README.md`, `rag/` Python source, `.mcp.json`, `rag.config.yaml`
  - **Convention source bundle**: `governance-bundle` (from `docs/compliance/normative-source-matrix.md`)
  - **Validation checklist** (table format): Artifact type | Convention source | Check | How to verify
  - Include check items for: rules (paths frontmatter, direct assertions, no prose), instructions (`applyTo` frontmatter, character limit, no standard conventions), hooks (exit code semantics, tool filtering, no blocking side effects), CLAUDE.md (15-40 lines, no domain-specific rules), root READMEs (section order, cost warning block, line budget)
  - **Manual fallback protocol**: "When no automated gate is available, run this checklist manually before merging any change to repository-global artifacts"
  - **Findings process**: Any violation found → document as CF-NNN finding using `docs/compliance/finding-model-and-validator-protocol.md` format
  - File must have `## Contents` TOC (will exceed 100 lines)
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md` — structural pattern; `docs/compliance/normative-source-matrix.md` — scope and bundle reference
- **GOTCHA**: Keep ≤200 lines; use tables for density; do not reproduce the finding model in full — reference it by path
- **VALIDATE**: `wc -l docs/compliance/repository-global-validation-protocol.md && grep "## Contents" docs/compliance/repository-global-validation-protocol.md`

---

### Group D: Drift Detection

#### Task D1: CREATE `plugins/agents-initializer/docs-drift-manifest.md`

- **ACTION**: Create drift manifest for agents-initializer reference files
- **IMPLEMENT**: Mirror `plugins/agent-customizer/docs-drift-manifest.md` format exactly:
  - Title block and description of purpose
  - Table: `Reference File | Source Docs | Status`
  - Populate table by reading each reference file in `plugins/agents-initializer/skills/*/references/*.md` and extracting the `Source:` line at the top of each file
  - Source docs must include line ranges where determinable (grep the source doc for content matches if needed)
  - Status: `baseline` for all initial entries
  - Files to include: all reference files across `init-claude/`, `init-agents/`, `improve-claude/`, `improve-agents/` — approximately 16 files total
  - Read the `Source:` field from each reference file to populate the Source Docs column
- **MIRROR**: `plugins/agent-customizer/docs-drift-manifest.md` — exact table format
- **GOTCHA**: Source paths in reference files are relative names without directory (e.g., `research-context-engineering-comprehensive.md`) — resolve to full `docs/` paths using `find docs -name "research-context-engineering-comprehensive.md"`; if not found, note as `[path-tbd]` in the manifest
- **VALIDATE**: `wc -l plugins/agents-initializer/docs-drift-manifest.md && grep -c "baseline" plugins/agents-initializer/docs-drift-manifest.md`

#### Task D2: CREATE `skills/docs-drift-manifest.md`

- **ACTION**: Create drift manifest for standalone distribution reference files
- **IMPLEMENT**: Mirror `plugins/agents-initializer/docs-drift-manifest.md` just created; populate from `skills/*/references/*.md` `Source:` lines
  - Standalone skills: `init-agents/`, `init-claude/`, `improve-agents/`, `improve-claude/`, `create-hook/`, `create-rule/`, `create-skill/`, `create-subagent/` — approximately 32 reference files
  - Follow same resolution approach for source paths
  - Status: `baseline` for all entries
- **MIRROR**: `plugins/agents-initializer/docs-drift-manifest.md` — just created; same format
- **GOTCHA**: Standalone has more skills than agents-initializer; expect ~32 rows; table may approach 100-line threshold → add `## Contents` TOC if >100 lines
- **VALIDATE**: `wc -l skills/docs-drift-manifest.md && grep -c "baseline" skills/docs-drift-manifest.md`

#### Task D3: UPDATE `.claude/skills/quality-gate/SKILL.md` — add Phase 3: Docs Drift

- **ACTION**: Insert Phase 3 Docs Drift between current Phase 2 (Parity) and current Phase 3 (Red-Green Tests, which becomes Phase 4); update phase numbers throughout; add regression checkpoint
- **IMPLEMENT**:
  - After Phase 2 section, insert new Phase 3 block:
    ```
    ## Phase 3: Docs Drift Detection

    Check for docs drift against both manifest files:
    - `plugins/agents-initializer/docs-drift-manifest.md`
    - `skills/docs-drift-manifest.md`

    For each manifest, read the manifest file, then verify that cited source docs exist at the
    referenced line ranges and that reference file content still aligns with source. Document
    any drift as findings in `drift_report`.

    **Manual drift check**: For each row in the manifest, run:
    `grep -n "" <source-doc-path> | sed -n '<start>,<end>p'` and compare against the
    reference file content that cites it.

    **Wait for completion.** Collect structured output as `drift_report`.
    ```
  - Renumber Phase 3 → Phase 4 (Red-Green Tests), Phase 4 → Phase 5 (Synthesis), Phase 5 → Phase 6 (Report)
  - At very end of SKILL.md, add regression checkpoint step:
    ```
    ## Regression Checkpoint

    After completing all phases, read `docs/compliance/regression-prevention-workflow.md`
    Section "Post-Gate Actions". Confirm all post-gate actions are complete before declaring
    the quality gate run finished.
    ```
  - Preserve all existing content exactly; only insert new sections
- **MIRROR**: `.claude/skills/agent-customizer-quality-gate/SKILL.md:55-70` — Phase 3 Docs Drift delegation pattern
- **GOTCHA**: quality-gate/SKILL.md currently ends with Phase 5 (Findings Report); after update it should end with Phase 6 + Regression Checkpoint. Verify final line count stays <500.
- **VALIDATE**: `wc -l .claude/skills/quality-gate/SKILL.md && grep -c "^## Phase" .claude/skills/quality-gate/SKILL.md` (should be 6 phases)

---

### Group E: Regression Prevention Layer

#### Task E1: CREATE `docs/compliance/regression-prevention-workflow.md`

- **ACTION**: Create the central regression prevention workflow document
- **IMPLEMENT**: Structure:
  - `## Contents` TOC (file will exceed 100 lines)
  - `## Purpose` — one paragraph: explains this doc ties together all quality gates as a repeatable regression prevention system
  - `## Change Type Matrix` — table: Change Type | Affected Scope | Required Gate | Manual Fallback
    - Content changes to plugin artifacts → cursor/agents/agent-customizer scope → run matching quality gate
    - Changes to standalone skills → standalone scope → run quality-gate
    - Changes to compliance docs / rules / instructions → repository-global → run repository-global-validation-protocol.md
    - New shared reference copy → parity check required → quality gate parity phase
    - Drift manifest update → re-run drift detection phase
  - `## Scope-to-Gate Map` — table: Scope | Quality Gate Skill | Fallback Protocol
    - agents-initializer → `quality-gate` | manual per `repository-global-validation-protocol.md` §rules
    - agent-customizer → `agent-customizer-quality-gate` | same
    - cursor-initializer → `cursor-initializer-quality-gate` | same
    - standalone → `quality-gate` | same
    - repository-global → none (automated) | `repository-global-validation-protocol.md`
  - `## Checkpoint Protocol` — numbered steps: 1. Identify change type using matrix; 2. Select gate(s) from scope-to-gate map; 3. Run gate(s); 4. Document any findings as CF-NNN; 5. Do not merge until all findings are REVALIDATED or CLOSED
  - `## Manual Fallback` — when to use: automated gate unavailable, repository-global scope, urgent fix. Protocol: run the applicable checklist from `repository-global-validation-protocol.md`; document any violations found as CF-NNN
  - `## Post-Gate Actions` — short checklist referenced by regression checkpoint in quality gate skills: confirm drift manifests up to date; confirm parity across shared copies; confirm no new CF-NNN findings left OPEN
- **MIRROR**: `docs/compliance/finding-model-and-validator-protocol.md` — tone and structure style
- **GOTCHA**: Must stay ≤200 lines; use tables and short bullets for density; `## Contents` TOC required
- **VALIDATE**: `wc -l docs/compliance/regression-prevention-workflow.md && grep "## Contents" docs/compliance/regression-prevention-workflow.md`

#### Task E2: CREATE `.claude/rules/compliance-maintenance.md`

- **ACTION**: Create path-scoped rule enforcing compliance workflow consultation
- **IMPLEMENT**:
  ```yaml
  ---
  paths:
    - "docs/compliance/**/*.md"
    - ".claude/skills/quality-gate/**"
    - ".claude/skills/agent-customizer-quality-gate/**"
    - ".claude/skills/cursor-initializer-quality-gate/**"
    - "wiki/knowledge/compliance*.md"
    - "wiki/knowledge/finding-model*.md"
  ---
  # Compliance Maintenance

  - Before modifying any compliance artifact, consult `docs/compliance/normative-source-matrix.md` to identify the scope and authoritative source bundle.
  - When a quality gate run produces CF-NNN findings, document them using `docs/compliance/finding-model-and-validator-protocol.md` before proposing corrections.
  - After modifying a quality gate skill or agent, re-run the regression checkpoint defined in `docs/compliance/regression-prevention-workflow.md`.
  - Drift manifests (`**/docs-drift-manifest.md`) must be updated when any cited source doc is modified.
  ```
- **MIRROR**: `.claude/rules/rag-mcp-server.md` — frontmatter pattern; `.claude/rules/rag-routing.md` — direct assertion style
- **GOTCHA**: Path globs must be specific; `**` alone is too broad; each path entry must target a real directory pattern
- **VALIDATE**: `grep -c "^paths:" .claude/rules/compliance-maintenance.md && head -12 .claude/rules/compliance-maintenance.md`

#### Task E3: CREATE `.github/instructions/compliance-prevention.instructions.md`

- **ACTION**: Create Copilot review instruction file for compliance artifact changes
- **IMPLEMENT**:
  ```yaml
  ---
  applyTo: "docs/compliance/**/*.md,.claude/skills/*quality-gate*/**,wiki/knowledge/compliance*.md"
  ---
  # Compliance Prevention Review Guidelines

  ## Finding Model
  - Every violation claim must reference a CF-NNN finding number and cite the violated rule source.
  - Finding status must be one of: OPEN, IN-PROGRESS, CORRECTED, REVALIDATED, CLOSED.

  ## Quality Gate Skills
  - SKILL.md files must delegate analysis to named agents — no inline bash scanning.
  - Every quality gate SKILL.md must end with the Regression Checkpoint step referencing `docs/compliance/regression-prevention-workflow.md`.
  - Agent files must use `model: sonnet`, `maxTurns: 20`, read-only tools only.

  ## Drift Manifests
  - Every row in a drift manifest must reference a real source doc path and valid line range.
  - Status column must be `baseline` until a drift checker run updates it.

  ## Compliance Docs
  - Files over 100 lines must have a `## Contents` TOC.
  - No compliance doc may exceed 200 lines.
  ```
- **MIRROR**: `.github/instructions/prp-artifacts.instructions.md` — frontmatter + section format
- **GOTCHA**: Character limit for Copilot review instructions is 4,000 chars; keep content concise; avoid long prose
- **VALIDATE**: `wc -c .github/instructions/compliance-prevention.instructions.md` (must be <4000)

#### Task E4: UPDATE `.claude/skills/agent-customizer-quality-gate/SKILL.md` — add regression checkpoint

- **ACTION**: Append a Regression Checkpoint section at the end of the file
- **IMPLEMENT**: After Phase 5 (Findings Report) section, append:
  ```
  ## Regression Checkpoint

  After completing all phases, read `docs/compliance/regression-prevention-workflow.md`
  Section "Post-Gate Actions". Confirm all post-gate actions are complete before declaring
  the quality gate run finished.
  ```
- **MIRROR**: Same regression checkpoint text added to quality-gate/SKILL.md in Task D3 — must be identical wording
- **GOTCHA**: agent-customizer-quality-gate/SKILL.md is currently 132 lines; adding ~8 lines brings it to ~140; well under 500-line limit. Do NOT renumber phases — agent-customizer QG is NOT adding a drift phase (it already has one).
- **VALIDATE**: `wc -l .claude/skills/agent-customizer-quality-gate/SKILL.md && tail -10 .claude/skills/agent-customizer-quality-gate/SKILL.md`

---

### Group F: PRD Update

#### Task F1: UPDATE PRD Phase 9 row

- **ACTION**: Update Phase 9 row in the Implementation Phases table
- **IMPLEMENT**: In `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`, find the Phase 9 row. Change `Status: pending` → `in-progress`. Add plan path in the PRP Plan column: `.claude/PRPs/plans/regression-prevention-workflow.plan.md`
- **MIRROR**: Other in-progress phase rows in the same table
- **GOTCHA**: Preserve exact table formatting (pipe-aligned markdown table); do not change any other rows
- **VALIDATE**: `grep "Phase 9" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md`

---

## Testing Strategy

| Check | Validates |
|-------|-----------|
| `wc -l` on all new files | No file exceeds 200 lines; SKILL.md <500 |
| `grep "^paths:" .claude/rules/compliance-maintenance.md` | Rule has path-scoped frontmatter |
| `grep "applyTo:" .github/instructions/compliance-prevention.instructions.md` | Instruction has frontmatter |
| `wc -c .github/instructions/compliance-prevention.instructions.md` | <4000 chars (Copilot limit) |
| `ls .claude/skills/cursor-initializer-quality-gate/agents/` | 3 agent files created |
| `ls .claude/skills/cursor-initializer-quality-gate/references/` | criteria reference created |
| `grep -c "baseline" plugins/agents-initializer/docs-drift-manifest.md` | All rows have status |
| `grep -c "baseline" skills/docs-drift-manifest.md` | All rows have status |
| `grep "## Phase" .claude/skills/quality-gate/SKILL.md` | 6 phases present after update |
| `grep "Regression Checkpoint" .claude/skills/agent-customizer-quality-gate/SKILL.md` | Checkpoint added |
| `grep "in-progress" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` | PRD updated |

---

## Validation Commands

```bash
# Verify all new files exist
ls docs/compliance/regression-prevention-workflow.md \
   docs/compliance/repository-global-validation-protocol.md \
   .claude/rules/compliance-maintenance.md \
   .github/instructions/compliance-prevention.instructions.md \
   .claude/skills/cursor-initializer-quality-gate/SKILL.md \
   plugins/agents-initializer/docs-drift-manifest.md \
   skills/docs-drift-manifest.md

# Verify line counts (all must pass)
wc -l docs/compliance/regression-prevention-workflow.md \
       docs/compliance/repository-global-validation-protocol.md \
       .claude/skills/cursor-initializer-quality-gate/SKILL.md \
       plugins/agents-initializer/docs-drift-manifest.md \
       skills/docs-drift-manifest.md

# Verify quality gate SKILL.md phase count
grep "^## Phase" .claude/skills/quality-gate/SKILL.md | wc -l
# Expected: 6

# Verify regression checkpoints present in both QG skills
grep -l "Regression Checkpoint" \
  .claude/skills/quality-gate/SKILL.md \
  .claude/skills/agent-customizer-quality-gate/SKILL.md \
  .claude/skills/cursor-initializer-quality-gate/SKILL.md

# Verify frontmatter in rule and instruction files
grep "^paths:" .claude/rules/compliance-maintenance.md
grep "^applyTo:" .github/instructions/compliance-prevention.instructions.md

# Verify instruction file is under 4000 chars
wc -c .github/instructions/compliance-prevention.instructions.md

# Verify PRD updated
grep -A2 "Phase 9" .claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md
```

---

## Acceptance Criteria

- [ ] All 20 Phase 9-assigned artifacts audited; violations documented as CF-NNN findings
- [ ] `cursor-initializer-quality-gate` skill created with 3 agents + criteria reference
- [ ] `repository-global-validation-protocol.md` created and covers all repository-global artifact types
- [ ] Drift manifests created for both `plugins/agents-initializer/` and `skills/`
- [ ] `quality-gate/SKILL.md` updated: Phase 3 Docs Drift inserted + regression checkpoint added
- [ ] `agent-customizer-quality-gate/SKILL.md` updated: regression checkpoint added
- [ ] `docs/compliance/regression-prevention-workflow.md` covers change type matrix, scope-gate map, checkpoint protocol, manual fallback, post-gate actions
- [ ] `.claude/rules/compliance-maintenance.md` has valid `paths:` frontmatter and direct assertions only
- [ ] `.github/instructions/compliance-prevention.instructions.md` has `applyTo:` frontmatter and is <4000 chars
- [ ] PRD Phase 9 row updated to `in-progress` with plan path
- [ ] No new file exceeds 200 lines; no SKILL.md exceeds 500 lines
- [ ] All validation commands pass with exit 0

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| Source paths in drift manifests unresolvable | MED | MED | Use `[path-tbd]` placeholder; leave note; resolve in Phase 10 |
| quality-gate/SKILL.md update breaks phase numbering | LOW | HIGH | Read entire file before editing; verify phase count after update |
| cursor-initializer QG criteria file exceeds 200 lines | MED | MED | Use dense table format; omit explanatory prose; add TOC if >100 |
| compliance-prevention.instructions.md exceeds 4000 chars | LOW | MED | Keep bullet lists, avoid prose; `wc -c` gate in validation |
| Artifact audit finds no violations | LOW | LOW | Valid outcome; document as "no findings" per validator protocol |
| Audit finds violations requiring immediate fix (CRITICAL) | LOW | HIGH | Document as CF-NNN per protocol; do NOT fix in Phase 9; escalate to Phase 10 planning |

---

## Notes

**Execution order**: Group A audits can be done in any order among themselves. Group B (cursor QG)
must precede Tasks D3 and E4 (which reference the cursor QG in regression checkpoints). Group E1
(regression-prevention-workflow.md) must be created before E2/E3/E4 since they reference it.
Task D3 depends on D1+D2 (drift manifests must exist before updating quality-gate to reference
them). Task F1 (PRD update) should be last.

**Audit finding storage**: CF-NNN findings discovered during Group A should be appended to the
existing finding register or documented in-line in this plan's execution notes. Phase 10 will
triage and assign corrections.

**Cursor quality gate scenarios**: The cursor-initializer QG Phase 3 (Red-Green Tests) should
use the improve scenarios from `.claude/PRPs/tests/scenarios/` — specifically
`improve-reasonable-artifact.md` and `improve-bloated-artifact.md` which cover the improve-cursor
skill family. Init scenarios (`init-simple-project.md`, `init-complex-monorepo.md`) also apply
to `init-cursor`.

**Drift manifest source resolution**: The `Source:` field in reference files uses bare filenames
(e.g., `research-context-engineering-comprehensive.md`). Resolve via:
`find docs -name "research-context-engineering-comprehensive.md" -type f`
If not found in `docs/`, check `wiki/knowledge/` and `.claude/` paths.
