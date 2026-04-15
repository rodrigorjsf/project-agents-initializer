---
name: prp-commit
description: "Atomic commits by logical scope following Conventional Commits 1.0.0. Analyzes all changes, groups them into independent units, and creates one conventional commit per group. Specify a file target or leave blank to commit all changes."
---

# Commit

## Strict Rules

- NEVER use `git add .` or `git add -A` — stage files by explicit path only
- NEVER add `Co-Authored-By` or any AI attribution footer
- One commit per logical scope — never mix unrelated changes
- Commit messages MUST conform to [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

## Phase 1: DISCOVER

```bash
git status
git diff
git diff --cached
```

If nothing to commit, stop.

## Phase 2: GROUP

Analyze all changes (staged + unstaged) and identify **atomic groups** — sets of files that form a single logical unit of work. Consider the affected component/scope, the type of change, and whether the files could be reverted independently.

**If a file target was specified** (e.g. "only agents", "except tests"): filter to matching files before grouping.

| Scenario | Action |
|----------|--------|
| All changes = one logical scope | Proceed to Phase 3 with all files |
| Multiple unrelated scopes | Commit each group separately in sequence |
| File target specified | Apply filter first, then group remainder |

## Phase 3: STAGE & COMMIT (repeat per group)

**Stage explicitly by path:**
```bash
git add path/to/file1 path/to/file2
```

**Verify only intended files are staged:**
```bash
git diff --staged --stat
```

**Write the commit message** following Conventional Commits 1.0.0:

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

### Type (REQUIRED)
MUST be one of:

| Type | When to use |
|------|-------------|
| `feat` | Adds a new feature (→ MINOR semver) |
| `fix` | Patches a bug (→ PATCH semver) |
| `docs` | Documentation only |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Neither a fix nor a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `build` | Build system, dependencies |
| `ci` | CI/CD configuration |
| `chore` | Maintenance tasks not affecting src/test |
| `revert` | Reverts a previous commit |

### Scope (OPTIONAL)
A noun in parentheses describing the codebase section: `feat(parser):`, `fix(api):`.

### Breaking Changes (REQUIRED when applicable)
Two allowed forms — use EITHER or BOTH:
- Append `!` after type/scope: `feat(api)!: remove endpoint`
- Footer token `BREAKING CHANGE: <description>` (one blank line after body)

`BREAKING CHANGE` MUST be uppercase. `BREAKING-CHANGE` is synonymous.

### Description (REQUIRED)
- Immediately follows the `: ` after type/scope
- Imperative present tense: "add", "fix", "remove" — not "added", "fixes"
- No capital first letter, no trailing period
- Max 72 characters

### Body (OPTIONAL)
- One blank line after description
- Explains WHAT and WHY — not HOW
- Free-form, 72-char line wrap

### Footer (OPTIONAL)
- One blank line after body (or description if no body)
- Token format: `Token: value` or `Token #value`
- Token uses `-` instead of spaces: `Reviewed-by:`, `Refs:`, `Fixes:`
- Exception: `BREAKING CHANGE` keeps its space

**Examples:**
```
feat(auth): add OAuth2 login support
```
```
fix(parser): handle null values in JSON input

Closes #42
```
```
feat(api)!: remove deprecated v1 endpoints

BREAKING CHANGE: /v1/users is removed, use /v2/users
```
```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

**Commit:**
```bash
git commit --no-verify -m "<description>" -m "<body>" -m "<footer>"
```

## Phase 4: REPORT

After all groups are committed:

```bash
git status
```

```markdown
**Committed**: N commit(s)
- {hash} {message} ({file_count} files)
- ...

**Remaining**: {uncommitted changes or "none"}

Next: `git push` or run `prp-pr` skill
```

If uncommitted changes remain, show them grouped by logical scope and ask if another commit is needed.
