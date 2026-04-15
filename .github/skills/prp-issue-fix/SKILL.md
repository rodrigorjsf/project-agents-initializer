---
name: prp-issue-fix
description: "Implement a fix from a prp-issue-investigate artifact. Provide an issue number or artifact path, optionally with --base <branch> to set the target branch. Loads the investigation plan, makes code changes, runs validation, creates a PR linked to the issue, runs self-review, and archives the artifact."
---

# Implement Issue Fix

## Mission

Execute the implementation plan from the `prp-issue-investigate` skill:

1. Load and validate the investigation artifact
2. Ensure git state is correct
3. Implement the changes exactly as specified
4. Run validation
5. Create PR linked to issue
6. Run self-review and post findings
7. Archive the artifact

**Golden Rule**: Follow the artifact. If something seems wrong, validate it first — don't silently deviate.

---

## Phase 0: DETECT — Base Branch

Load the base branch detection protocol:
```
${CLAUDE_SKILL_DIR}/references/fix-protocol.md
```

Determine base branch from: input `--base` flag → `git symbolic-ref refs/remotes/origin/HEAD` → `git remote show origin` → fallback `main`.

Store as `{base-branch}` — use for ALL branch operations and PR creation.

---

## Phase 1: LOAD — Get the Artifact

**If input is a number** (`123`, `#123`):
```bash
ls .claude/PRPs/issues/issue-{number}.md
```

**If input is a path:** Use directly.

Parse artifact to extract: issue number/title, type, files to modify (with lines), implementation steps, validation commands, test cases.

**If artifact not found:**
```
❌ Artifact not found at .claude/PRPs/issues/issue-{number}.md

Run the prp-issue-investigate skill first to create the implementation plan.
```

**CHECKPOINT:**
- [ ] Artifact found and loaded
- [ ] Key sections parsed (files, steps, validation)
- [ ] Issue number extracted

---

## Phase 2: VALIDATE — Sanity Check

For each file in the artifact, read actual current code and compare to what the artifact expects.

See fix protocol reference for drift detection format and handling.

Confirm the proposed fix actually addresses the root cause. If plan seems fundamentally wrong → STOP and suggest re-investigation.

**CHECKPOINT:**
- [ ] Artifact matches current codebase state
- [ ] Approach still makes sense
- [ ] No blocking issues identified

---

## Phase 3: GIT-CHECK — Ensure Correct State

```bash
git branch --show-current
git rev-parse --show-toplevel
git worktree list
git status --porcelain
git fetch origin
```

Follow the git state decision tree from the fix protocol reference to determine whether to create a new branch, use existing, or stop.

Sync with base branch:
```bash
git pull --rebase origin {base-branch} 2>/dev/null || git pull origin {base-branch}
```

**CHECKPOINT:**
- [ ] Git state is clean and correct
- [ ] On appropriate branch (created or existing)
- [ ] Up to date with {base-branch}

---

## Phase 4: IMPLEMENT — Make Changes

Execute each step from the artifact's Implementation Plan in order:

1. **Read** the target file
2. **Make the change** exactly as specified
3. **Verify types compile** after each change

Follow implementation rules from the fix protocol: match code style, copy patterns from artifact, add tests as specified, don't refactor unrelated code or add unplanned improvements.

Track any deviations with rationale.

**CHECKPOINT:**
- [ ] All artifact steps executed
- [ ] Types compile after each change
- [ ] Tests added as specified
- [ ] Deviations documented (if any)

---

## Phase 5: VERIFY — Run Validation

Execute each command from the artifact's Validation section. All must pass before proceeding.

If failures: analyze → fix → re-run → note additional fixes in PR description.

Execute manual verification steps if specified in artifact.

**CHECKPOINT:**
- [ ] Type check passes
- [ ] Tests pass
- [ ] Lint passes
- [ ] Manual verification complete (if applicable)

---

## Phase 6: COMMIT — Save Changes

```bash
git add {list of changed files}  # Prefer specific files over git add -A
git status
```

Load commit message and PR templates:
```
${CLAUDE_SKILL_DIR}/references/report-template.md
```

Commit using the format from the report template. Message must reference the issue number with `Fixes #{number}`.

---

## Phase 7: PR — Create Pull Request

```bash
git push -u origin HEAD  # Use --force-with-lease if rebased
```

Create PR using `gh pr create --base "{base-branch}"` with the PR body template from the report template reference. PR must include `Fixes #{number}` to link the issue.

```bash
PR_URL=$(gh pr view --json url -q '.url')
PR_NUMBER=$(gh pr view --json number -q '.number')
```

**CHECKPOINT:**
- [ ] Changes pushed to remote
- [ ] PR created and linked to issue

---

## Phase 8: REVIEW — Self Code Review

Use Task tool with `subagent_type="prp-core:code-reviewer"`:

```
Review the changes in this PR for issue #{number}.

Focus on:
1. Does the fix address the root cause from the investigation?
2. Code quality - matches codebase patterns?
3. Test coverage - are the new tests sufficient?
4. Edge cases - are they handled?
5. Security - any concerns?
6. Potential bugs - anything that could break?

Review only the diff, not the entire codebase.
```

Post review to PR using the self-review comment template from the report template reference.

**CHECKPOINT:**
- [ ] Code review completed
- [ ] Review posted to PR

---

## Phase 9: ARCHIVE — Clean Up

```bash
mkdir -p .claude/PRPs/issues/completed
mv .claude/PRPs/issues/issue-{number}.md .claude/PRPs/issues/completed/
git add .claude/PRPs/issues/
git commit -m "Archive investigation for issue #{number}"
git push
```

---

## Phase 10: REPORT — Output to User

Display the user report (format in report-template.md reference) including:
- Issue number, branch name, PR number/URL
- Changes made table
- Validation results
- Self-review summary
- Archived artifact path
- Next steps: human review and merge

---

## Success Criteria

- **PLAN_EXECUTED**: All artifact steps completed
- **VALIDATION_PASSED**: All checks green
- **PR_CREATED**: PR exists and linked to issue
- **REVIEW_POSTED**: Self-review comment on PR
- **ARTIFACT_ARCHIVED**: Moved to completed folder
- **AUDIT_TRAIL**: Full history in git and GitHub
