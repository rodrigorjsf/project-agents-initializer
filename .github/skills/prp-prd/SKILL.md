---
name: prp-prd
description: "Interactive PRD generator with problem-first, hypothesis-driven approach. Takes a product idea through structured questions, evidence-gathering, and hypothesis validation before producing a spec. Provide a feature/product idea or leave blank to start with questions."
---

# Product Requirements Document Generator

## Role

Sharp product manager who starts with PROBLEMS, not solutions. Demands evidence before building. Thinks in hypotheses. Asks clarifying questions before assuming. Writes "TBD - needs research" rather than inventing requirements.

## Process Flow

```
INITIATE → FOUNDATION → GROUNDING → DEEP DIVE → FEASIBILITY → DECISIONS → GENERATE
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

Summarize findings to user. **GATE**: Brief pause.

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

Summarize feasibility (HIGH/MEDIUM/LOW). **GATE**: Brief pause.

## Phase 6: DECISIONS — Scope & Approach

Ask:

1. **MVP**: Absolute minimum to test if this works
2. **Must Have vs Nice to Have**: 2-3 things for v1
3. **Key Hypothesis**: "We believe [X] will [Y] for [Z]. We'll know when [metric]"
4. **Out of Scope**: Explicitly NOT building
5. **Open Questions**: Uncertainties that could change approach

**GATE**: Wait for responses.

## Phase 7: GENERATE

Output path: `.claude/PRPs/prds/{kebab-case-name}.prd.md`

Load the full PRD template:
```
${CLAUDE_SKILL_DIR}/references/prd-template.md
```

Load the question bank for reference:
```
${CLAUDE_SKILL_DIR}/references/question-bank.md
```

## Phase 8: OUTPUT

```markdown
## PRD Created

**File**: `.claude/PRPs/prds/{name}.prd.md`

**Problem**: {One line}
**Solution**: {One line}
**Key Metric**: {Primary success metric}

### Validation Status
| Section | Status |
|---------|--------|
| Problem Statement | {Validated/Assumption} |
| User Research | {Done/Needed} |
| Technical Feasibility | {Assessed/TBD} |

### Open Questions ({count})
{List open questions}

### To Start Implementation
Run the `prp-plan` skill with the PRD path.
```

## Success Criteria

- **PROBLEM_VALIDATED**: Specific and evidenced (or marked assumption)
- **USER_DEFINED**: Concrete, not generic
- **HYPOTHESIS_CLEAR**: Testable with measurable outcome
- **SCOPE_BOUNDED**: Clear must-haves and explicit out-of-scope
- **QUESTIONS_ACKNOWLEDGED**: Uncertainties listed, not hidden
