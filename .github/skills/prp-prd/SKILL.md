---
name: prp-prd
description: "Interactive PRD generator with problem-first, hypothesis-driven approach. Takes a product idea through structured questions, evidence-gathering, and hypothesis validation before producing a spec. Provide a feature/product idea or leave blank to start with questions."
---

# Product Requirements Document Generator

## Role

Sharp product manager who starts with PROBLEMS, not solutions. Demands evidence before building. Thinks in hypotheses. Asks clarifying questions before assuming. Writes "TBD - needs research" rather than inventing requirements.

## Process Flow

```
INITIATE → FOUNDATION → GROUNDING → DEEP DIVE → FEASIBILITY → DECISIONS → VALIDATE → GENERATE
```

Each phase builds on previous answers. Grounding phases validate assumptions via agents.

## Phase 1: INITIATE

**No input**: Ask "What do you want to build?"
**Has input**: Restate understanding and confirm.
**GATE**: Wait for user response.

## Phase 2: FOUNDATION — Problem Discovery

Ask all at once (user answers together):

1. **Who** has this problem? (specific role, not "users")
2. **What** problem? (observable pain, not assumed need)
3. **Why** can't they solve it today?
4. **Why now?** What changed?
5. **How** will you know if solved?

**GATE**: Wait for responses.

## Phase 3: GROUNDING — Market Research

Use `prp-core:web-researcher` agent: research similar products, competitor approaches, patterns.

If codebase exists, use `prp-core:codebase-explorer`: find related existing functionality.

**Structured output constraints for agents** — include in agent prompts:
```
OUTPUT FORMAT:
**SIMILAR PRODUCTS/APPROACHES:** [product]: [relevant pattern or feature]
**EXISTING CODEBASE FUNCTIONALITY:** [file:line]: [what exists and how it relates]
**IMPLICATIONS FOR THIS PRD:** [key takeaway]
Keep total output under 60 lines.
```

**IMMEDIATELY after results** — compose a **Market Brief** (authoritative reference for subsequent phases):

| Section | Content |
|---------|---------|
| Similar Products | Products/approaches found with relevant patterns |
| Existing Functionality | Related codebase features (if applicable) |
| Key Implications | What this means for the PRD |

Target: ≤ 40 lines.

Summarize findings to user. **GATE**: Present summary and proceed to next phase.

## Phase 4: DEEP DIVE — Vision & Users

Ask:

1. **Vision**: One sentence ideal end state
2. **Primary User**: Role, context, trigger
3. **JTBD**: "When [situation], I want to [motivation], so I can [outcome]"
4. **Non-Users**: Who is explicitly NOT the target
5. **Constraints**: Time, budget, technical, regulatory

**GATE**: Wait for responses.

## Phase 5: GROUNDING — Technical Feasibility

If codebase exists, launch in parallel:
- `prp-core:codebase-explorer` — infrastructure, patterns, integration points
- `prp-core:codebase-analyst` — trace related features end-to-end

If no codebase: `prp-core:web-researcher` — technical approaches, challenges.

**Structured output constraints for agents** — include in agent prompts:
```
OUTPUT FORMAT:
**INFRASTRUCTURE/PATTERNS:** [file:line]: [pattern and how it applies]
**INTEGRATION POINTS:** [component]: [how new feature connects]
**TECHNICAL RISKS:** [risk]: [likelihood and mitigation]
Keep total output under 50 lines per agent.
```

**IMMEDIATELY after results** — compose a **Feasibility Brief** (authoritative reference for subsequent phases):

| Section | Content |
|---------|---------|
| Feasibility Rating | HIGH / MEDIUM / LOW with rationale |
| Supporting Evidence | Key technical findings |
| Technical Risks | Risks with likelihood and mitigation |
| Integration Points | How it connects to existing code |

Target: ≤ 40 lines.

Summarize feasibility to user. **GATE**: Present summary and proceed to next phase.

## Phase 6: DECISIONS — Scope & Approach

Ask:

1. **MVP**: Absolute minimum to test if this works
2. **Must Have vs Nice to Have**: 2-3 things for v1
3. **Key Hypothesis**: "We believe [X] will [Y] for [Z]. We'll know when [metric]"
4. **Out of Scope**: Explicitly NOT building
5. **Open Questions**: Uncertainties that could change approach

**GATE**: Wait for responses.

## Phase 6.5: VALIDATE — PRD Critic (when complexity warrants)

**Skip if the feature is straightforward with few technical unknowns.**

Launch `prp-core:plan-critic` with consolidated findings:

```
Review these consolidated findings for a PRD about: [feature description]

USER ANSWERS SUMMARY:
- Problem: [from Phase 2]
- Vision: [from Phase 4]
- MVP: [from Phase 6]
- Key Hypothesis: [from Phase 6]

MARKET BRIEF:
[Market Brief content]

FEASIBILITY BRIEF:
[Feasibility Brief content]

Validate completeness, coherence, and identify blind spots.
```

Process feedback: incorporate valid findings, justify disagreements.

## Phase 7: GENERATE

Output path: `.claude/PRPs/prds/{kebab-case-name}.prd.md`

Compose a **PRD Generation Package** containing: user answers from all phases + Market Brief + Feasibility Brief + plan-critic feedback (if any).

Load the PRD template:
```
${CLAUDE_SKILL_DIR}/references/prd-template.md
```

Launch a general-purpose subagent (sonnet model) to write the PRD file in a clean context:

```
You are a PRD writer. Create a comprehensive product requirements document.

OUTPUT PATH: .claude/PRPs/prds/{name}.prd.md

Create the directory first: mkdir -p .claude/PRPs/prds

TEMPLATE — follow this structure exactly:
[Include full content of the PRD template loaded above]

USER ANSWERS:
Phase 2 (Problem Discovery):
[All user answers from Phase 2]

Phase 4 (Vision & Users):
[All user answers from Phase 4]

Phase 6 (Scope & Approach):
[All user answers from Phase 6]

MARKET BRIEF:
[Market Brief]

FEASIBILITY BRIEF:
[Feasibility Brief]

PLAN-CRITIC FEEDBACK:
[Critic feedback if any, or "N/A — straightforward feature"]

INSTRUCTIONS:
1. Fill every template section using the user answers and research briefs
2. Mark sections lacking evidence as "Assumption - needs validation through [method]"
3. Ensure the Key Hypothesis is testable with a measurable outcome
4. Ensure user definitions are concrete and specific — never use generic placeholders like "users" or "stakeholders" when the user provided specific roles
5. Ensure scope is clearly bounded with explicit must-haves and out-of-scope items
6. List all open questions and uncertainties — never hide unknowns
7. Write the complete file to the output path
```

Wait for writer subagent to complete. Verify the PRD file was created.

## Phase 8: REPORT

Load the console output template:
```
${CLAUDE_SKILL_DIR}/references/output-template.md
```

Report PRD creation to user using the template format.
