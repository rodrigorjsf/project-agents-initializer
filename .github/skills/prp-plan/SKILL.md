---
name: prp-plan
description: "Create a comprehensive feature implementation plan with deep codebase analysis and research. Provide a feature description in natural language or a path to a PRD file. Explores the codebase first, researches gaps, and produces a battle-tested plan that enables one-pass implementation success without writing any code."
---

# Feature Implementation Plan

**Core Principle**: PLAN ONLY — no code written. Create a context-rich document that enables one-pass implementation success.

**Execution Order**: CODEBASE FIRST, RESEARCH SECOND. Solutions must fit existing patterns before introducing new ones.

---

## Phase 0: DETECT — Input Type Resolution

| Input Pattern | Type | Action |
|---------------|------|--------|
| Ends with `.prd.md` | PRD file | Parse PRD, select next pending phase |
| Ends with `.md` and contains "Implementation Phases" | PRD file | Parse PRD, select next pending phase |
| File path that exists | Document | Read and extract feature description |
| Free-form text | Description | Use directly as feature input |
| Empty/blank | Conversation | Use conversation context as input |

### If PRD File Detected:

1. Read the PRD file
2. Parse Implementation Phases table — find rows with `Status: pending`
3. Check dependencies — only select phases whose dependencies are `complete`
4. Select next actionable phase (first pending with all deps complete)
5. Extract phase context: PHASE, GOAL, SCOPE, SUCCESS SIGNAL, PRD CONTEXT
6. Report selection to user (note parallel opportunities if applicable)

### If Free-form or Conversation Context:

Proceed directly to Phase 1 with the input as feature description.

**CHECKPOINT:**
- [ ] Input type determined
- [ ] If PRD: next phase selected and dependencies verified
- [ ] Feature description ready for Phase 1

---

## Phase 1: PARSE — Feature Understanding

**Extract from input:**

- Core problem being solved
- User value and business impact
- Feature type: NEW_CAPABILITY | ENHANCEMENT | REFACTOR | BUG_FIX
- Complexity: LOW | MEDIUM | HIGH
- Affected systems list

**GATE**: If requirements are AMBIGUOUS → STOP and ASK user for clarification.

**CHECKPOINT:**
- [ ] Problem statement is specific and testable
- [ ] Complexity assessed with rationale

---

## Phase 2: EXPLORE — Codebase Intelligence

Load the full exploration protocol with agent prompts:
```
${CLAUDE_SKILL_DIR}/references/exploration-protocol.md
```

Launch subagents in parallel using `subagent_type="prp-core:codebase-explorer"` and `subagent_type="prp-core:codebase-analyst"` (see protocol for prompts and output format).

**IMMEDIATELY after merging results** — compose a **Discovery Brief** (authoritative reference for all subsequent phases):

| Section | Content |
|---------|---------|
| Key Locations | Table of file:line refs by category (naming, errors, logging, tests, types, config) |
| Mirrorable Snippets | Top 3 actual code patterns to follow (≤ 5 lines each) |
| Integration Points | Entry points + data flow summary |
| Dependencies | Libraries and versions in use |
| Test Patterns | Test framework, structure, assertion style |

Target: ≤ 50 lines. This brief replaces raw agent output for all subsequent phases.

**CHECKPOINT:**
- [ ] Both agents launched in parallel and completed
- [ ] Discovery Brief composed with ≥ 3 mirrorable snippets
- [ ] Code snippets are ACTUAL (copy-pasted, not invented)

---

## Phase 3: RESEARCH — External Documentation

**ONLY AFTER Phase 2 is complete.**

Use `prp-core:web-researcher` agent (see exploration protocol for prompt and output format). Match documentation versions to project config.

**IMMEDIATELY after results** — compose a **Research Brief** (authoritative reference for subsequent phases):

| Section | Content |
|---------|---------|
| Key Docs | Direct links with version-specific anchors |
| Critical Insights | What affects implementation decisions |
| Gotchas | Pitfalls with mitigation strategies |
| Version Constraints | Library compatibility notes |

Target: ≤ 30 lines.

**CHECKPOINT:**
- [ ] Research Brief composed
- [ ] Documentation versions match project config

---

## Phase 4: DESIGN — UX Transformation

Create ASCII diagrams showing user experience BEFORE and AFTER states including user flow steps, pain points, and data flow.

**IMMEDIATELY after design** — compose a **UX Brief** (authoritative reference for subsequent phases):

| Section | Content |
|---------|---------|
| Before | Current user experience summary |
| After | New capabilities and value adds |
| Interaction Changes | Location → Before → After → User Impact |

Target: ≤ 30 lines.

**CHECKPOINT:**
- [ ] UX Brief composed
- [ ] Before state reflects current system
- [ ] After state shows ALL new capabilities

---

## Phase 5: ARCHITECT — Strategic Design

For complex features, use `prp-core:codebase-analyst` to trace architecture at integration points (see exploration protocol for prompt and output format).

Analyze: architecture fit, execution order, failure modes, performance, security, maintainability.

**IMMEDIATELY after analysis** — compose an **Architecture Brief** (authoritative reference for generation):

| Section | Content |
|---------|---------|
| Approach | Chosen approach with rationale |
| Rejected Alternatives | Options with rejection reasons |
| Scope Limits | NOT_BUILDING items with justification |
| Failure Modes | Edge cases with mitigations |
| Execution Order | Dependency sequence |

Target: ≤ 30 lines.

**CHECKPOINT:**
- [ ] Architecture Brief composed
- [ ] Approach aligns with existing architecture
- [ ] Scope boundaries explicit and justified

---

## Phase 5.5: VALIDATE — Plan Critic (MEDIUM/HIGH complexity only)

**Skip this phase if complexity is LOW.**

Launch `prp-core:plan-critic` with all phase briefs:

```
Review these consolidated findings for a plan about: [feature description]

DISCOVERY BRIEF:
[Discovery Brief content]

RESEARCH BRIEF:
[Research Brief content]

UX BRIEF:
[UX Brief content]

ARCHITECTURE BRIEF:
[Architecture Brief content]

Validate completeness, coherence, and identify blind spots.
```

Process feedback: incorporate valid findings into the relevant briefs, briefly justify any disagreements.

Make sure to execute `prp-verification-before-completion` skill for every claim you make in the briefs and critic feedback. No evidence = no claim.

---

## Phase 6: GENERATE — Implementation Plan File

**Output path**: `.claude/PRPs/plans/{kebab-case-feature-name}.plan.md`

Compose a **Plan Generation Package** containing all phase briefs and plan-critic feedback (if any).

Launch a general-purpose subagent (sonnet model) to write the plan file in a clean context:

```
You are a plan writer. Create a comprehensive implementation plan file.

OUTPUT PATH: .claude/PRPs/plans/{feature-name}.plan.md

Create the directory first: mkdir -p .claude/PRPs/plans

TEMPLATE — follow this structure exactly:
[Include full content of: ${CLAUDE_SKILL_DIR}/references/plan-template.md]

DISCOVERY BRIEF:
[Discovery Brief]

RESEARCH BRIEF:
[Research Brief]

UX BRIEF:
[UX Brief]

ARCHITECTURE BRIEF:
[Architecture Brief]

PLAN-CRITIC FEEDBACK:
[Critic feedback if any, or "N/A — LOW complexity"]

VERIFICATION — check every item before saving:
[Include full content of: ${CLAUDE_SKILL_DIR}/references/verification-checklist.md]

INSTRUCTIONS:
1. Fill every template section using findings from the briefs
2. Every pattern reference must include actual code snippets from the Discovery Brief
3. Every task must have an executable validation command
4. Replace all placeholder commands with actual project commands discovered in the briefs
5. Run the verification checklist — fix any failing items before saving
6. Write the complete file to the output path
```

Wait for writer subagent to complete. Verify the plan file was created.

### If input was from PRD file:

Update the PRD: change phase Status from `pending` to `in-progress`, add plan file path to PRP Plan column.

---

## Phase 7: REPORT

Load the console output template:
```
${CLAUDE_SKILL_DIR}/references/output-template.md
```

Report plan creation to user using the template format.
