# Test Scenario: Improve — Bloated Existing Configuration

**Scenario ID**: S3
**Skills Under Test**: `improve-agents` (plugin + standalone), `improve-claude` (plugin + standalone)
**Phase**: GREEN (Tasks M1–M4)
**Input Fixtures**: `bloated-agents-md.md`, `bloated-claude-md.md`

---

## Scenario Description

A multi-language project (Python + Go services) whose AGENTS.md / CLAUDE.md grew organically over 18 months into a 200+ line monolith. The file has accumulated:

- Inline Python and Go rules that should be in separate files
- A directory listing showing the project structure
- Stale file paths referencing modules that were renamed
- Contradictions (conflicting indentation rules)
- Linting rules that tools enforce automatically
- Tutorial-style explanations for basic operations
- Generic boilerplate advice

---

## Input Fixtures

Use fixtures from `.claude/PRPs/tests/fixtures/`:

| Fixture | Lines | Use with |
|---------|-------|---------|
| `bloated-agents-md.md` | ~220 | `improve-agents` runs |
| `bloated-claude-md.md` | ~230 | `improve-claude` runs |

### Planted Violations (all must be caught and fixed)

`bloated-agents-md.md` contains:

1. **Inline Python rules** — pytest conventions, import sorting style, type hints style
2. **Inline Go rules** — error handling patterns, naming conventions, package structure
3. **Directory listing** — ASCII tree with ├──, └──, │ characters
4. **Stale file paths** — at least 2 references marked `[STALE]` in fixture
5. **Contradiction** — "always use tabs" and "use 2-space indent" in the same file
6. **Auto-enforced linting rules** — "max line length 80" (enforced by ruff/golangci-lint)
7. **Tutorial-style** — "To run tests, first install pytest by running..."
8. **Generic advice** — "write clean, readable code"

`bloated-claude-md.md` additionally contains:

1. **Inline `.claude/rules/` content** — rules that should be in separate rule files
2. **@import references to non-existent files** — `@nonexistent-module.md`

---

## Skill Invocation

Point the skill at the fixture file (copy it to a test project as AGENTS.md or CLAUDE.md), then invoke:

- Plugin: invoke `improve-agents` or `improve-claude` via Claude Code with plugin installed
- Standalone: read skill file and follow instructions

---

## Expected Output

### improve-agents (bloated fixture)

| File | Expected Lines | Description |
|------|---------------|-------------|
| `AGENTS.md` (root) | 15–40 | Restructured root, violations removed |
| `python-conventions.md` (domain doc) | 10–40 | Extracted Python rules |
| `go-conventions.md` (domain doc) | 10–40 | Extracted Go rules |

Or alternatively, violations removed without extraction if content is truly auto-enforced by tools.

### improve-claude (bloated fixture)

| File | Expected Lines | Description |
|------|---------------|-------------|
| `CLAUDE.md` (root) | 15–40 | Restructured root |
| `.claude/rules/[extracted-rules].md` | 5–30 | Extracted rule files |

---

## Pass Criteria

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Root file length | ≤40 lines (ideally 15–40) | `wc -l AGENTS.md` |
| Directory listing removed | 0 tree characters | `grep -c "├\|└\|│" AGENTS.md` |
| Python rules extracted | Not inline in root | `grep -c "pytest\|import sort" AGENTS.md` → 0 |
| Go rules extracted | Not inline in root | `grep -c "error handling\|naming conv" AGENTS.md` → 0 |
| Stale paths removed | 0 stale references | `grep -c "STALE\|nonexistent" AGENTS.md` → 0 |
| Contradiction resolved | One consistent style | Manual review |
| Auto-enforced rules removed | Line length, linting rules gone | Manual review |
| Tutorial text removed | No "first install", "first run" | `grep -i "first install" AGENTS.md` → 0 |
| Generic advice removed | No "write clean", "readable code" | Manual review |
| Critical info preserved | Custom commands, unique patterns kept | Manual review |

### Scoring (5-dimension rubric from evaluation-criteria.md)

Evaluate on 1–10 scale:

| Dimension | Baseline (fixture) | Expected after improve |
|-----------|-------------------|----------------------|
| Conciseness | 2/10 (220+ lines) | ≥8/10 |
| Accuracy | 4/10 (stale paths, contradictions) | ≥9/10 |
| Specificity | 3/10 (generic advice) | ≥8/10 |
| Progressive Disclosure | 1/10 (monolithic) | ≥7/10 |
| Consistency | 3/10 (contradictions) | ≥9/10 |

---

## Self-Validation Loop Evidence

This scenario is a primary trigger for self-validation loop iterations:

- Bloated improve is the hardest task — initial restructuring may produce output with new violations
- Watch for Phase 4 loop catching intermediate violations during restructuring
- All 10 planted violation types must be caught by the evaluator

**Expected loop behavior**: Multiple validation iterations likely during restructuring.
