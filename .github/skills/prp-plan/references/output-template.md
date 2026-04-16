# Console Output Template

Report to user after plan file is created:

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
