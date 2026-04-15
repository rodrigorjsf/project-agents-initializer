---
name: prp-pr
description: "Create a pull request from current branch with unpushed commits. Auto-detects base branch, validates git state, uses repository PR templates, writes a summary of changes, and pushes if needed. Optionally specify --base <branch>."
---

# Create Pull Request

## Phase 0: DETECT Base Branch

1. Check if user provided `--base <branch>` → use that
2. Auto-detect: `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'`
3. Fallback: `git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}'`
4. Last resort: `main`

Store as `{base-branch}` — use for ALL comparisons.

## Phase 1: VALIDATE

```bash
BRANCH=$(git branch --show-current)
git status --short
git log origin/{base-branch}..HEAD --oneline
```

| State | Action |
|-------|--------|
| On {base-branch} | STOP: Cannot create PR from base branch |
| Uncommitted changes | WARN: Commit or stash first |
| No commits ahead | STOP: Branch up to date with {base-branch} |
| Has commits, clean | PROCEED |

Check for existing PR:
```bash
gh pr list --head $(git branch --show-current) --json number,url
```

## Phase 2: DISCOVER

1. **PR template**: Check `.github/PULL_REQUEST_TEMPLATE.md`, `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`, `docs/pull_request_template.md`
2. **Commits**: `git log origin/{base-branch}..HEAD --pretty=format:"- %s"`
3. **Changed files**: `git diff --stat origin/{base-branch}..HEAD`
4. **Title**: Single commit → use message. Multiple → summarize as `{type}: {description}`

## Phase 3: PUSH

```bash
git push -u origin HEAD
```

If push fails due to rebase, suggest `--force-with-lease` (warn user first).

## Phase 4: CREATE PR

**If template found**: Read and fill each section from commits/changes.

**If no template**: Use default format:

```bash
gh pr create \
  --title "{title}" \
  --base "{base-branch}" \
  --body "{body with summary, changes, files, testing checklist, related issues}"
```

Extract issue references from commits (`Fixes #123`, `Closes #123`, `#123`).

## Phase 5: VERIFY & OUTPUT

```bash
gh pr view --json number,url,title,state
```

```markdown
## Pull Request Created

**PR**: #{number}
**URL**: {url}
**Title**: {title}
**Base**: {base-branch} ← {current-branch}

### Changes
- {N} commits, {M} files changed

### Next Steps
- Wait for CI checks: `gh pr checks`
- Add reviewer: `gh pr edit --add-reviewer @username`
- View in browser: `gh pr view --web`
```

## Edge Cases

- **Diverged branch**: Suggest rebase then `git push --force-with-lease`
- **Multiple templates**: Use default or ask user
- **Draft PR**: Add `--draft` flag to `gh pr create`
