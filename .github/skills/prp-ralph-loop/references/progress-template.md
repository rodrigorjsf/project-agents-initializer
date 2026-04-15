# Progress Log Template

Append this to the state file after each iteration:

```markdown
## Iteration N - YYYY-MM-DDTHH:MM:SSZ

### Completed
- [What was implemented this iteration]
- [Files changed: list them]

### Validation Status
- Type-check: PASS/FAIL (details if failing)
- Lint: PASS/FAIL (details if failing)
- Tests: PASS/FAIL (X/Y passing, details if failing)
- Build: PASS/FAIL (details if failing)

### Learnings
- [Pattern discovered: "this codebase uses X for Y"]
- [Gotcha found: "don't forget to Z when doing W"]
- [Context: "the component X is in directory Y"]

### Next Steps
- [What the next iteration should focus on]
- [Specific files or functions to look at]

---
```

## Codebase Patterns Section

If you discover a **reusable pattern**, add it to `## Codebase Patterns` at the top of the state file. Only general, reusable patterns — not iteration-specific details.

## State File Format

```markdown
---
iteration: 3
max_iterations: 10
plan_path: ".claude/PRPs/plans/add-feature.md"
started_at: "2024-01-12T10:00:00Z"
---

# PRP Ralph Loop State

## Codebase Patterns
[Consolidated learnings that apply across iterations]

## Progress Log
[Iteration entries appended here]
```

## Archive Format

On completion, archive to:
```
.claude/PRPs/ralph-archives/YYYY-MM-DD-feature-name/
├── state.md        # Final state file
├── plan.md         # The executed plan
└── learnings.md    # Implementation report
```
