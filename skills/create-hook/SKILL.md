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
- **EVERY** hook must use a handler type supported by the selected event — verify this against the handler support matrix in `hook-events-reference.md`
- **EVERY** `command` hook must document the decision path used by the script: exit `2` + stderr for blocking, or exit `0` with JSON decision output when applicable
- **EVERY** hook configuration must produce valid JSON before writing
</RULES>

## Process

### Preflight Check

Check if hooks already exist for the target event in:

- `.claude/settings.json`
- `.claude/settings.local.json`
- Plugin `hooks/hooks.json`

**If the exact same event + matcher combination already exists:**

1. Inform the user: "A hook for `{event}` with this matcher already exists."
2. Suggest using the `improve-hook` skill to evaluate and optimize it instead.
3. **STOP** — do not proceed. The user should either choose a different matcher/event combination or use the improve skill.

**If no hook exists for this event+matcher combination:**
Proceed to Phase 1 below.

### Phase 1: Codebase Analysis

Read `references/artifact-analyzer.md` and follow its analysis instructions to analyze the project at the current working directory.

Focus on: existing hook configurations in `.claude/settings.json`, `.claude/settings.local.json`, and plugin `hooks/hooks.json`; project hook scripts in `.claude/hooks/`; plugin hook scripts in `scripts/`; event types currently in use; handler types used (command/http/prompt/agent); and any gaps in lifecycle event coverage. Also read root `CLAUDE.md`, `README.md`, and any service-level README files to understand non-standard build commands, tooling, or conventions that hook scripts should use.

### Phase 2: Generate Hook

Before generating, read these reference documents:

- `references/hook-authoring-guide.md` — when to use hooks, 4 handler types, exit code semantics, blocking vs non-blocking behavior
- `references/hook-events-reference.md` — all 22 valid events, matcher fields per event, full JSON schema
- `references/prompt-engineering-strategies.md` — hook-specific prompting (zero-shot only for hooks)

Read `assets/templates/hook-config.md` and fill its placeholders using:

- User requirements for the new hook (event, purpose, handler type)
- Phase 1 analysis output (existing hooks, coverage gaps)
- Evidence from the reference files above

Before choosing the handler, verify in `hook-events-reference.md` that the selected event supports it. If the selected event only supports `command`, do not generate `http`, `prompt`, or `agent` guidance for that hook. If the requested handler is unsupported, stop and ask the user to change the event or handler choice.

Choose the target location based on the requested scope:

- `.claude/settings.json` — committed project hook
- `.claude/settings.local.json` — local-only hook
- `hooks/hooks.json` — plugin-bundled hook

Generate the complete hook configuration:

1. Hook JSON block — to be merged into the `hooks` key of the selected target file
2. Shell script (if `command` type):
   - Project/local hook: write to `.claude/hooks/{name}.sh` with executable permissions
   - Plugin hook: write to `scripts/{name}.sh` with executable permissions and reference it with `${CLAUDE_PLUGIN_ROOT}/scripts/{name}.sh`

**Important**: The hook JSON must be merged into the selected target file, not replace it. Read the current target file first and produce the merged result.

### Phase 3: Self-Validation

Read `references/hook-validation-criteria.md` and execute its **Validation Loop Instructions** against the generated hook configuration.

The loop evaluates all hard limits and quality checks, fixes any failures, and re-evaluates — maximum 3 iterations. Do not proceed to Phase 4 until ALL criteria pass.

### Phase 4: Present and Write

1. Show the user the complete hook configuration (JSON + shell script if applicable)
2. Cite the evidence from reference files that informed key decisions:
   - Which event was chosen and why
   - Why this handler type (command/http/prompt/agent)
   - What the exit code behavior means for this event
3. Ask for confirmation before writing any files
4. On approval:
   - Merge hook JSON into the selected target file
   - Write shell script to `.claude/hooks/{name}.sh` or `scripts/{name}.sh` and set executable (`chmod +x`)
