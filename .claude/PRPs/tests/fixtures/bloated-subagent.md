---
# VIOLATION 7: [PLANTED] Missing required 'description' field in YAML frontmatter
name: code-analyzer
# VIOLATION 1: [PLANTED] Missing 'model' field in YAML frontmatter — model is required
# VIOLATION 2: [PLANTED] Write tools included — subagents must be read-only; Write and Edit are prohibited
tools: Read, Write, Edit, Grep, Glob, Bash
# VIOLATION 3: [PLANTED] maxTurns: 50 far exceeds the allowed maximum of 20
maxTurns: 50
---

# Code Analyzer Agent

<!-- VIOLATION 8: [PLANTED] No evidence citations — no references to agent design docs or source conventions -->
<!-- VIOLATION 5: [PLANTED] Generic system prompt — "you are a helpful assistant" with no specificity -->

You are a helpful assistant. You can analyze code and help with various tasks.

## Your Capabilities

You are very capable and can do many things. Help the user with whatever they need.
Be thorough and comprehensive in your analysis.

## Instructions

<!-- VIOLATION 4: [PLANTED] Instructions to spawn other agents — subagents must not spawn child agents -->

When you encounter complex tasks, delegate to specialized sub-agents:
1. For code analysis, spawn a `code-analysis-agent` using the Task tool
2. For documentation, spawn a `docs-agent` using the Task tool
3. For testing, spawn a `test-runner-agent` using the Task tool

If the task is too complex for a single agent, use the Dispatch tool to run multiple agents in parallel.

## Analysis Process

1. Read all files in the project directory
2. Write summary files to disk for each service analyzed
3. Edit configuration files to add missing conventions
4. Run `find . -name "*.md" | xargs grep -l "TODO"` to find pending items
5. Create reports at `./analysis-reports/` directory

## Output

<!-- VIOLATION 6: [PLANTED] No structured output specification — output format is undefined and unparseable -->

After analysis, report your findings in whatever format seems appropriate. Be thorough.
Include everything you found. The more detail the better.

## Notes

This agent has extensive capabilities and should use them all when needed. Feel free to
modify files, create new files, and make changes as you see fit to improve the codebase.
Always aim for comprehensive coverage even if it takes many turns.
