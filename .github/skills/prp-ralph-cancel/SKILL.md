---
name: prp-ralph-cancel
description: "Cancel an active PRP Ralph autonomous loop. Removes the state file and reports what iteration was reached. Work in progress is preserved in modified files and git commits."
---

# Cancel PRP Ralph Loop

## Steps

1. **Check if loop is active**

   ```bash
   test -f .claude/prp-ralph.state.md && echo "ACTIVE" || echo "NOT_FOUND"
   ```

2. **If NOT_FOUND**: Report "No active Ralph loop found."

3. **If ACTIVE**:

   a. Read the state file to get current iteration:

   ```bash
   head -20 .claude/prp-ralph.state.md
   ```

   b. Extract iteration number from the YAML frontmatter

   c. Remove the state file:

   ```bash
   rm .claude/prp-ralph.state.md
   ```

   d. Report:

   ```markdown
   ## Ralph Loop Cancelled

   **Was at**: Iteration {N}
   **Plan**: {plan_path}

   The loop has been stopped. Your work so far is preserved in:
   - Modified files (check `git status`)
   - Git commits (if any were made)

   To resume later, run the `prp-ralph` skill with the same plan path.
   Or continue manually with the `prp-implement` skill.
   ```
