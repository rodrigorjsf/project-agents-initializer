# Test Scenario: Improve — Decent Existing Configuration

**Scenario ID**: S4
**Skills Under Test**: `improve-agents` (plugin + standalone), `improve-claude` (plugin + standalone)
**Phase**: GREEN (Tasks M5–M8)
**Input Fixtures**: `reasonable-agents-md.md`, `reasonable-claude-md.md`

---

## Scenario Description

A Node.js API project with an existing AGENTS.md / CLAUDE.md that someone wrote thoughtfully ~6 months ago. It's mostly well-structured but has a few minor issues that accumulated over time. This is the hardest improve scenario: skills must identify real improvements without over-modifying a file that's already good.

---

## Input Fixtures

Use fixtures from `.claude/PRPs/tests/fixtures/`:

| Fixture | Lines | Use with |
|---------|-------|---------|
| `reasonable-agents-md.md` | ~60 | `improve-agents` runs |
| `reasonable-claude-md.md` | ~65 | `improve-claude` runs |

### Planted Issues (subtle; must be identified without over-modifying)

`reasonable-agents-md.md` (2–3 issues):

1. **One slightly vague instruction** — e.g., "handle errors appropriately" with no specifics
2. **One default command listed** — e.g., `npm test` documented as a custom command when it's the default
3. **One section that could be a separate file** — a 15-line "Database conventions" section that would be better as a domain doc

`reasonable-claude-md.md` (2–3 issues):

1. **One rule that belongs in `.claude/rules/`** — a formatting rule that's inline in the root file
2. **One slightly stale reference** — a reference to a file that was renamed (e.g., `src/config.js` → `src/config.ts`)
3. **One minor over-specification** — documents TypeScript types that are already enforced by the tsconfig

---

## Skill Invocation

Point the skill at the fixture file, then invoke:

- Plugin: invoke `improve-agents` or `improve-claude` via Claude Code with plugin installed
- Standalone: read skill file and follow instructions

---

## Expected Output

### improve-agents (reasonable fixture)

The skill should make targeted improvements without restructuring the whole file:

| Action | Expected |
|--------|----------|
| Vague instruction | Clarified with specific guidance |
| Default command removed | `npm test` entry removed or noted as default |
| Database section | Extracted to `database-conventions.md` domain doc (if ≥15 lines) |
| Everything else | Preserved exactly as-is |

### improve-claude (reasonable fixture)

| Action | Expected |
|--------|----------|
| Inline rule | Extracted to `.claude/rules/` file |
| Stale reference | Updated to correct filename |
| Over-specification | Removed (tools enforce this) |
| Everything else | Preserved exactly as-is |

---

## Pass Criteria

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Quality score improves or holds | Score ≥ original | Evaluate before and after with template |
| No critical info lost | 0 cases of lost custom commands, unique patterns | Manual review |
| File count increases minimally | At most 1 new domain doc created | Manual count |
| Root file stays concise | Still 15–40 lines after improvement | `wc -l` |
| Planted issues addressed | All 2–3 issues resolved | Manual checklist |
| No over-modification | Non-issue sections unchanged | Diff review |

### Scoring (5-dimension rubric)

| Dimension | Baseline (fixture) | Expected after improve |
|-----------|-------------------|----------------------|
| Conciseness | 7/10 | ≥8/10 |
| Accuracy | 8/10 (minor stale ref) | ≥9/10 |
| Specificity | 7/10 (vague instruction) | ≥9/10 |
| Progressive Disclosure | 7/10 (one extractable section) | ≥8/10 |
| Consistency | 9/10 | ≥9/10 |

---

## Hardest Aspect of This Test

The improve skill must demonstrate **restraint** — recognizing that a mostly-good file needs surgical fixes, not wholesale restructuring. A skill that rewrites the entire file has failed this scenario even if the output is technically valid.

Watch for:

- Skills that over-apply changes (rewriting sections that were fine)
- Skills that miss the subtle issues (only catch obvious violations)
- Skills that introduce new issues while fixing existing ones

**Expected loop behavior**: Loop may not need to iterate if the skill is well-calibrated. Excessive looping on a reasonable file suggests the evaluation criteria are too aggressive.
