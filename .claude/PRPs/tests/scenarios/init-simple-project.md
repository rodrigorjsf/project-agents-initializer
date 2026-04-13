# Test Scenario: Init — Simple Single-Scope Project

**Scenario ID**: S1
**Skills Under Test**: `init-agents` (plugin + standalone), `init-claude` (plugin + standalone), `init-cursor` (plugin)
**Phase**: GREEN (Tasks I1–I4)

---

## Project Characteristics

A single-package Python CLI tool with standard tooling:

- **Language**: Python 3.11+
- **Framework**: Click (CLI framework)
- **Testing**: pytest, pytest-cov
- **Linting**: ruff (lint + format)
- **Type checking**: mypy
- **Package manager**: uv + pyproject.toml
- **CI**: GitHub Actions (standard Python workflow)
- **Structure**: Single package (`src/myapp/`), flat layout

### Directory Structure

```
myapp/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── conftest.py
│   └── test_core.py
├── pyproject.toml
├── uv.lock
└── README.md
```

### pyproject.toml (summary)

```toml
[tool.ruff]
line-length = 120

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src"
```

---

## What to Test Against

Present the skill with this description of the project (or navigate to a real test project matching these characteristics) and invoke the skill.

**Prompt to use for RED phase comparison**:
> "Create an AGENTS.md for a Python CLI project. It uses Click, pytest, ruff, mypy, and uv."

**Skill invocation**:

- Plugin: invoke `init-agents` or `init-claude` skill via Claude Code with plugin installed
- Standalone: read `skills/init-agents/SKILL.md` or `skills/init-claude/SKILL.md` and follow instructions

---

## Expected Output

### init-agents

| File | Expected Lines | Key Constraints |
|------|---------------|-----------------|
| `AGENTS.md` (root) | 15–40 | No scoped files; no language tutorials; no directory listing |

Root AGENTS.md should contain:

- Project purpose (1–3 lines)
- Non-standard configuration: `line-length = 120` (ruff override), `strict = true` (mypy), `--cov=src` (coverage always on)
- Command reference: test command if non-standard (standard `pytest` need not be documented)
- Notable patterns: anything non-obvious about the project

Root AGENTS.md should NOT contain:

- How to install pytest, ruff, or mypy
- A directory listing of src/myapp/
- Generic advice ("write clean, readable code")
- Python language rules (PEP 8, import sorting) — these are enforced by ruff
- Default commands like `ruff check .` (standard; should be omitted)

### init-claude

| File | Expected Lines | Key Constraints |
|------|---------------|-----------------|
| `CLAUDE.md` (root) | 15–40 | No scoped files; no rules that belong in `.claude/rules/` |

Root CLAUDE.md should contain:

- Project-specific conventions not inferrable from code
- Non-obvious build commands or flags
- Critical constraints (e.g., must maintain mypy strict compliance)

### init-cursor

| File | Expected Lines | Key Constraints |
|------|---------------|-----------------|
| `AGENTS.md` (root) | 15–40 | Same minimal root constraints as `init-agents` |
| `.cursor/rules/*.mdc` | 0 or small focused set | Only generated if truly justified; must use valid Cursor frontmatter |

`init-cursor` should:

- Generate the same minimal root `AGENTS.md` quality bar as `init-agents`
- Prefer **zero** `.cursor/rules/*.mdc` files for this simple single-scope project unless the analysis finds a truly non-obvious file-pattern rule
- If any `.mdc` file is generated, keep it focused and validate frontmatter with only `description`, `alwaysApply`, and `globs`

---

## Pass Criteria

| Criterion | Threshold | How to Check |
|-----------|-----------|--------------|
| Root file length | 15–40 lines | `wc -l AGENTS.md` |
| Scoped files generated | 0 (none needed) | `ls **/AGENTS.md` — should be 1 |
| No directory listing | 0 tree characters (├, └, │) | `grep -c "├\|└\|│" AGENTS.md` |
| No language tutorials | 0 "install", "first install" phrases | Manual review |
| No generic advice | 0 "write clean", "readable code" phrases | Manual review |
| No default commands documented | pytest, ruff, mypy not in "run X to do Y" form | Manual review |
| Non-standard config captured | line-length 120, strict mypy, --cov=src | Manual review |
| Cursor root file stays minimal | Same 15–40 line target as `init-agents` | `wc -l AGENTS.md` |
| Cursor rules remain restrained | 0 unnecessary `.cursor/rules/*.mdc` files | Manual review |
| Cursor frontmatter valid | Only `description`, `alwaysApply`, `globs` | Manual review |

---

## Baseline Comparison

After RED phase establishes baseline, verify these specific improvements:

| RED failure | GREEN resolution |
|-------------|-----------------|
| Root file >40 lines | Root file 15–40 lines |
| Language-specific rules inlined | No Python rules in root |
| Directory listing included | No tree characters |
| Tutorial-style explanations | No install instructions |
| Default commands documented | pytest/ruff not listed |
| Generic advice | No boilerplate phrases |

---

## Self-Validation Loop Evidence

Watch for (during skill execution):

- Phase 4 (validation) triggering a re-evaluation
- Any mention of "exceeds line limit" or "trimming"
- Phase 5 (refine) producing a shorter output than initial draft

For a simple single-scope project, the loop may not need to iterate (first-pass output likely passes hard limits).
