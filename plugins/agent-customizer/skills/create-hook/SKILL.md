---
name: create-hook
description: "Creates new hook configurations for Claude Code lifecycle events, grounded in the docs corpus. Covers all hook event types with JSON schema compliance. Use when creating a new hook from scratch."
---

# Create Hook

Generates a new hook configuration for a Claude Code lifecycle event, with correct JSON schema, handler type, and exit code behavior grounded in the docs corpus.

## Hard Rules

<RULES>
- **NEVER** create hooks with invalid event names — only events from the 22-event list in hook-events-reference.md are valid
- **NEVER** use broad matchers (`"*"`) for blocking hooks — overly broad matchers block too many operations
- **NEVER** hardcode secrets in command strings — use environment variables (e.g., `$MY_SECRET`)
- **EVERY** hook must use the correct handler type for its purpose: `command` for deterministic checks, `http` for external endpoints, `prompt` or `agent` only when judgment is needed
- **EVERY** `command` hook must document the decision path used by the script: exit `2` + stderr for blocking, or exit `0` with JSON decision output when applicable
- **EVERY** hook configuration must produce valid JSON before writing
</RULES>

## Process

### Preflight Check

Check if hooks already exist for the target event in `.claude/settings.json` and `.claude/settings.local.json`.

**If the exact same event + matcher combination already exists:**

1. Inform the user: "A hook for `{event}` with this matcher already exists."
2. Inform the user that `improve-hook` is currently a Phase 5 placeholder and not yet executable.
3. **STOP** — do not proceed to Phase 1 or any subsequent phase of this create skill. Ask the user to choose a different matcher/event combination or wait for the improve workflow implementation.

**If no hook exists for this event+matcher combination:**
Proceed to Phase 1 below.

### Phase 1: Codebase Analysis

Delegate to the `artifact-analyzer` agent with this task:

> Analyze the project to understand existing hook configurations. Focus on: hooks defined in `.claude/settings.json` and `.claude/settings.local.json`, hook scripts in `.claude/hooks/`, event types currently in use, handler types used (command/http/prompt/agent), and any gaps in lifecycle event coverage.

The agent runs on Sonnet with read-only tools (Read, Grep, Glob, Bash) in an isolated context. Wait for it to complete and parse its structured output.

### Phase 2: Generate Hook

Before generating, read these reference documents:

- `${CLAUDE_SKILL_DIR}/references/hook-authoring-guide.md` — when to use hooks, 4 handler types, exit code semantics, blocking vs non-blocking behavior
- `${CLAUDE_SKILL_DIR}/references/hook-events-reference.md` — all 22 valid events, matcher fields per event, full JSON schema
- `${CLAUDE_SKILL_DIR}/references/prompt-engineering-strategies.md` — hook-specific prompting (zero-shot only for hooks)

Read `${CLAUDE_SKILL_DIR}/assets/templates/hook-config.md` and fill its placeholders using:

- User requirements for the new hook (event, purpose, handler type)
- Phase 1 analysis output (existing hooks, coverage gaps)
- Evidence from the reference files above

Generate the complete hook configuration:

1. Hook JSON block — to be merged into the `hooks` key of `.claude/settings.json`
2. Shell script (if `command` type) — written to `.claude/hooks/{name}.sh` with executable permissions

**Important**: The hook JSON must be merged into existing settings, not replace them. Read the current `.claude/settings.json` first and produce the merged result.

### Phase 3: Self-Validation

Read `${CLAUDE_SKILL_DIR}/references/hook-validation-criteria.md` and execute its **Validation Loop Instructions** against the generated hook configuration.

The loop evaluates all hard limits and quality checks, fixes any failures, and re-evaluates — maximum 3 iterations. Do not proceed to Phase 4 until ALL criteria pass.

### Phase 4: Present and Write

1. Show the user the complete hook configuration (JSON + shell script if applicable)
2. Cite the evidence from reference files that informed key decisions:
   - Which event was chosen and why
   - Why this handler type (command/http/prompt/agent)
   - What the exit code behavior means for this event
3. Ask for confirmation before writing any files
4. On approval:
   - Merge hook JSON into `.claude/settings.json`
   - Write shell script to `.claude/hooks/{name}.sh` and set executable (`chmod +x`)
