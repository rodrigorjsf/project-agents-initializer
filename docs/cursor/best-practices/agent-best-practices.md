# Agent Best Practices

**Source:** [cursor.com/blog/agent-best-practices](https://cursor.com/blog/agent-best-practices)

Official Cursor guide covering techniques for working effectively with Cursor's agent. Extracted from the Cursor blog.

## Understanding Agent Harnesses

An agent harness is built on three components:

1. **Instructions**: The system prompt and rules that guide agent behavior
2. **Tools**: File editing, codebase search, terminal execution, and more
3. **Model**: The agent model you pick for the task

Cursor's agent harness orchestrates these components for each model, tuning instructions and tools specifically for every frontier model based on internal evals and external benchmarks.

## Start with Plans

The most impactful change: planning before coding.

A [study](https://cursor.com/blog/productivity) from the University of Chicago found that experienced developers are more likely to plan before generating code.

### Using Plan Mode

Press `Shift+Tab` in the agent input to toggle Plan Mode. The agent will:

1. Research your codebase to find relevant files
2. Ask clarifying questions about your requirements
3. Create a detailed implementation plan with file paths and code references
4. Wait for your approval before building

Plans open as Markdown files you can edit directly.

> **Tip:** Click "Save to workspace" to store plans in `.cursor/plans/`. This creates documentation for your team and provides context for future agents.

### Starting Over from a Plan

When the agent builds something wrong: revert changes, refine the plan, and run again. Often faster than fixing an in-progress agent.

## Managing Context

### Let the Agent Find Context

Don't manually tag every file. Cursor's agent has powerful search tools and pulls context on demand. Including irrelevant files can confuse the agent about what's important.

### When to Start a New Conversation

**Start new when:**
- Moving to a different task or feature
- The agent seems confused or keeps making the same mistakes
- Finished one logical unit of work

**Continue when:**
- Iterating on the same feature
- The agent needs context from earlier
- Debugging something it just built

Long conversations cause the agent to lose focus — context accumulates noise after many turns and summarizations.

### Reference Past Work

Use `@Past Chats` to reference previous work rather than copy-pasting the whole conversation.

## Extending the Agent

### Rules: Static Context for Your Project

Rules provide persistent instructions. Create as markdown files in `.cursor/rules/`:

```markdown
# Commands
- `npm run build`: Build the project
- `npm run typecheck`: Run the typechecker
- `npm run test`: Run tests

# Code style
- Use ES modules (import/export), not CommonJS (require)
- Destructure imports when possible
- See `components/Button.tsx` for canonical component structure

# Workflow
- Always typecheck after making a series of code changes
- API routes go in `app/api/` following existing patterns
```

**Keep rules focused on essentials**: commands to run, patterns to follow, pointers to canonical examples. Reference files instead of copying contents.

**What to avoid in rules:**
- Copying entire style guides (use a linter instead)
- Documenting every possible command (the agent knows common tools)
- Adding instructions for edge cases that rarely apply

> **Tip:** Start simple. Add rules only when you notice the agent making the same mistake repeatedly.

### Skills: Dynamic Capabilities and Workflows

Skills extend what agents can do. Defined in `SKILL.md` files, they include:
- **Custom commands**: Reusable workflows triggered with `/` in the agent input
- **Hooks**: Scripts that run before or after agent actions
- **Domain knowledge**: Instructions for specific tasks the agent can pull in on demand

Unlike Rules (always included), Skills are loaded dynamically when the agent decides they're relevant.

## Common Workflows

### Test-Driven Development

1. Ask the agent to write tests based on expected input/output pairs
2. Tell the agent to run tests and confirm they fail (no implementation code yet)
3. Commit the tests when satisfied
4. Ask the agent to write code that passes the tests (no test modifications)
5. Commit the implementation

Agents perform best when they have a clear target to iterate against.

### Git Workflows

A `/pr` command example:
```markdown
Create a pull request for the current changes.
1. Look at the staged and unstaged changes with `git diff`
2. Write a clear commit message based on what changed
3. Commit and push to the current branch
4. Use `gh pr create` to open a pull request
5. Return the PR URL when done
```

## Reviewing Code

### During Generation

Watch the agent work. The diff view shows changes as they happen. Click **Stop** to cancel and redirect.

### Agent Review

Click **Review** → **Find Issues** to run a dedicated review pass.

### BugBot for Pull Requests

Push to source control to get automated reviews on pull requests. BugBot applies advanced analysis to catch issues early.

## Running Agents in Parallel

### Native Worktree Support

Cursor automatically creates and manages git worktrees for parallel agents. Each agent runs in its own worktree with isolated files and changes.

### Run Multiple Models at Once

Select multiple models from the dropdown, submit your prompt, compare results side by side. Useful for hard problems and finding edge cases.

## Delegating to Cloud Agents

Cloud agents work well for:
- Bug fixes that came up while working on something else
- Refactors of recent code changes
- Generating tests for existing code
- Documentation updates

Cloud agents clone your repo, create a branch, work autonomously, and open a pull request when finished.

## Debug Mode

Debug Mode provides evidence-based debugging:
1. Generates multiple hypotheses
2. Instruments code with logging
3. Asks you to reproduce the bug while collecting runtime data
4. Analyzes actual behavior to pinpoint root cause
5. Makes targeted fixes based on evidence

Best for reproducible bugs, race conditions, performance problems, and regressions.

## Developing Your Workflow

Key traits of effective agent users:

- **Write specific prompts**: Compare "add tests for auth.ts" with "Write a test case for auth.ts covering the logout edge case, using the patterns in `__tests__/` and avoiding mocks."
- **Iterate on setup**: Start simple. Add rules only when you notice repeated mistakes. Add commands after figuring out workflows you want to repeat.
- **Review carefully**: AI-generated code can look right while being subtly wrong. Treat AI code with the same rigor as a PR from a junior developer.
