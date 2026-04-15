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

**Formulate user story:**

```
As a <user type>
I want to <action/goal>
So that <benefit/value>
```

**GATE**: If requirements are AMBIGUOUS → STOP and ASK user for clarification.

**CHECKPOINT:**
- [ ] Problem statement is specific and testable
- [ ] User story follows correct format
- [ ] Complexity assessed with rationale

---

## Phase 2: EXPLORE — Codebase Intelligence

**Directory Discovery** (run these first to understand project structure):
```bash
ls -la
ls -la */ 2>/dev/null | head -50
```

Do NOT assume `src/` exists — discover the actual structure (could be `app/`, `lib/`, `packages/`, `cmd/`, root-level files, etc.).

Load the full exploration protocol with agent prompts:
```
${CLAUDE_SKILL_DIR}/references/exploration-protocol.md
```

**CRITICAL: Launch `prp-core:codebase-explorer` and `prp-core:codebase-analyst` in parallel.**

Merge results into a unified discovery table (see exploration protocol for format).

**CHECKPOINT:**
- [ ] Both agents launched in parallel and completed
- [ ] At least 3 similar implementations found with file:line refs
- [ ] Code snippets are ACTUAL (copy-pasted, not invented)
- [ ] Integration points mapped with data flow traces
- [ ] Dependencies cataloged with versions

---

## Phase 3: RESEARCH — External Documentation

**ONLY AFTER Phase 2 is complete.**

Use `prp-core:web-researcher` agent (see exploration protocol for prompt). Match documentation versions to project's package.json/config.

Format findings with direct links, key insights, gotchas, and version constraints.

**CHECKPOINT:**
- [ ] Documentation versions match project config
- [ ] URLs include specific section anchors
- [ ] Gotchas documented with mitigation strategies

---

## Phase 4: DESIGN — UX Transformation

Create ASCII diagrams showing user experience BEFORE and AFTER states including:
- User flow steps
- Pain points (before) / Value adds (after)
- Data flow through the system

Document interaction changes in a table: Location | Before | After | User Impact.

**CHECKPOINT:**
- [ ] Before state accurately reflects current system
- [ ] After state shows ALL new capabilities
- [ ] Data flows are traceable; user value is explicit

---

## Phase 5: ARCHITECT — Strategic Design

For complex features, use `prp-core:codebase-analyst` to trace architecture at integration points (see exploration protocol for prompt and analysis framework).

Analyze: architecture fit, execution order, failure modes, performance, security, maintainability.

Document: chosen approach with rationale, rejected alternatives with reasons, explicit scope limits (NOT_BUILDING).

**CHECKPOINT:**
- [ ] Approach aligns with existing architecture
- [ ] Dependencies ordered correctly
- [ ] Edge cases identified with mitigations
- [ ] Scope boundaries explicit and justified

---

## Phase 6: GENERATE — Implementation Plan File

**Output path**: `.claude/PRPs/plans/{kebab-case-feature-name}.plan.md`

```bash
mkdir -p .claude/PRPs/plans
```

Load the full plan template:
```
${CLAUDE_SKILL_DIR}/references/plan-template.md
```

Fill the template with all findings from Phases 1-5. Every pattern reference must include actual code snippets. Every task must have an executable validation command. Replace all placeholder commands with actual project commands.

### If input was from PRD file:

Update the PRD: change phase Status from `pending` to `in-progress`, add plan file path to PRP Plan column.

---

## Output

Report to user:

```
## Plan Created

**File**: `.claude/PRPs/plans/{feature-name}.plan.md`

{If from PRD: source PRD path, phase number, PRD update confirmation}
{If parallel phases available: note opportunity with worktree command}

**Summary**: {2-3 sentence overview}
**Complexity**: {LOW/MEDIUM/HIGH} - {rationale}

**Scope**:
- {N} files to CREATE
- {M} files to UPDATE
- {K} total tasks

**Key Patterns Discovered**:
- {Pattern 1 with file:line}
- {Pattern 2 with file:line}

**External Research**: {key docs with versions}

**UX Transformation**:
- BEFORE: {one-line current state}
- AFTER: {one-line new state}

**Risks**: {primary risk and mitigation}

**Confidence Score**: {1-10}/10 for one-pass implementation success
- {Rationale}

**Next Step**: To execute, run the `prp-implement` skill with `.claude/PRPs/plans/{feature-name}.plan.md`
```

---

## Verification Checklist

Before saving the plan, verify:

**Context completeness:**
- [ ] All patterns documented with file:line references
- [ ] External docs versioned to match project config
- [ ] Integration points mapped with specific file paths
- [ ] Gotchas captured with mitigation strategies

**Implementation readiness:**
- [ ] Tasks ordered by dependency (executable top-to-bottom)
- [ ] Each task is atomic and independently testable
- [ ] No placeholders — all content is specific and actionable
- [ ] Pattern references include actual code snippets

**Pattern faithfulness:**
- [ ] Every new file mirrors existing codebase style exactly
- [ ] No unnecessary abstractions introduced
- [ ] Naming follows discovered conventions

**Validation coverage:**
- [ ] Every task has executable validation command
- [ ] Edge cases enumerated with test plans

**NO_PRIOR_KNOWLEDGE_TEST**: Could an agent unfamiliar with this codebase implement using ONLY the plan?

---

## Success Criteria

- **CONTEXT_COMPLETE**: All patterns, gotchas, integration points documented from actual codebase
- **IMPLEMENTATION_READY**: Tasks executable top-to-bottom without questions
- **PATTERN_FAITHFUL**: Every new file mirrors existing codebase style exactly
- **VALIDATION_DEFINED**: Every task has executable verification command
- **UX_DOCUMENTED**: Before/After transformation is visually clear
- **ONE_PASS_TARGET**: Confidence score 8+ indicates high likelihood of first-attempt success
