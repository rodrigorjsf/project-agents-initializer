# Fix Protocol

## Base Branch Detection

Determine the base branch (used for branching, syncing, and PR creation):

1. **Check input**: If input contains `--base <branch>`, extract that value and remove the flag
2. **Auto-detect from remote**:
   ```bash
   git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
   ```
3. **Fallback**:
   ```bash
   git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}'
   ```
4. **Last resort**: `main`

Store as `{base-branch}` — never hardcode `main` or `master`.

---

## Git State Decision Tree

```
┌─ IN WORKTREE?
│  └─ YES → Use it (assume it's for this work)
│           Log: "Using worktree at {path}"
│
├─ ON {base-branch}?
│  └─ Q: Working directory clean?
│     ├─ YES → Create branch: fix/issue-{number}-{slug}
│     │        git checkout -b fix/issue-{number}-{slug}
│     └─ NO  → Warn user:
│              "Working directory has uncommitted changes.
│               Please commit or stash before proceeding."
│              STOP
│
├─ ON FEATURE/FIX BRANCH?
│  └─ Use it (assume it's for this work)
│     If branch name doesn't contain issue number:
│       Warn: "Branch '{name}' may not be for issue #{number}"
│
└─ DIRTY STATE?
   └─ Warn and suggest: git stash or git commit
      STOP
```

---

## Implementation Rules

**DO:**

- Follow artifact steps in order
- Match existing code style exactly
- Copy patterns from "Patterns to Follow" section
- Add tests as specified

**DON'T:**

- Refactor unrelated code
- Add "improvements" not in the plan
- Change formatting of untouched lines
- Deviate from the artifact without noting it

### File Operations

**UPDATE files:** Read current content → find exact lines → make specified change → preserve surrounding code.

**CREATE files:** Use patterns from artifact → follow existing file structure conventions → include all specified content.

**Test files:** Add test cases as specified → follow existing test patterns → ensure tests actually test the fix.

### Tracking Deviations

If you must deviate from the artifact, note what changed and why. Include in PR description.

---

## Plan Accuracy Verification

For each file mentioned in the artifact:

- Read the actual current code
- Compare to what artifact expects
- Check if the "current code" snippets match reality

**If significant drift detected:**

```
⚠️ Code has changed since investigation:

File: src/x.ts:45
- Artifact expected: {snippet}
- Actual code: {different snippet}

Options:
1. Re-run the prp-issue-investigate skill to get fresh analysis
2. Proceed carefully with manual adjustments
```

**If plan seems fundamentally wrong:** STOP, explain what's wrong, suggest re-investigation.

---

## Edge Case Handling

### Artifact is outdated
- Warn user about drift
- Suggest re-running the `prp-issue-investigate` skill
- Can proceed with caution if changes are minor

### Tests fail after implementation
- Debug the failure
- Fix the code (not the test, unless test is wrong)
- Re-run validation
- Note the additional fix in PR

### Merge conflicts during rebase
- Resolve conflicts
- Re-run full validation
- Note conflict resolution in PR

### PR creation fails
- Check if PR already exists for branch
- Check for permission issues
- Provide manual gh command

### Already on a branch with changes
- Use the existing branch
- Warn if branch name doesn't match issue
- Don't create a new branch

### In a worktree
- Use it as-is
- Assume it was created for this purpose
- Log that worktree is being used
