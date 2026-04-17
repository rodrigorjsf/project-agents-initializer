---
name: create-subagent
description: "Creates new subagent definitions with YAML frontmatter grounded in the docs corpus. Includes model selection heuristics and tool restriction patterns. Use when creating a new Claude Code subagent from scratch."
---

# Create Subagent

Generates a new subagent definition with correct YAML frontmatter, minimal tool restrictions, and a structured system prompt grounded in the docs corpus.

## Hard Rules

<RULES>
- **NEVER** create subagents with generic system prompts ("you are a helpful AI assistant")
- **NEVER** grant write tools (`Edit`, `Write`) to read-only analysis or review agents; allow `Bash` only for explicitly read-only commands when needed
- **NEVER** set `maxTurns` > 30 without explicit justification in the system prompt
- **EVERY** subagent must include: role definition, process steps, output format, and self-verification instructions
- **EVERY** `description` must include specific "Use when..." trigger phrases so Claude routes correctly
- **Subagents CANNOT spawn other subagents** — the `Agent` tool is unavailable to subagents at runtime; warn if the user requests nested subagent delegation
- Plugin context: `hooks`, `mcpServers`, and `permissionMode` fields are ignored for plugin agents
</RULES>

## Process

### Preflight Check

Check if a subagent with the same name already exists at:

- `.claude/agents/{requested-name}.md`
- `plugins/*/agents/{requested-name}.md`

**If a subagent already exists with that name:**

1. Inform the user: "A subagent named `{requested-name}` already exists."
2. Suggest using the `improve-subagent` skill to evaluate and optimize it instead.
3. **STOP** — do not proceed. The user should either choose a different name or use the improve skill.

**If no subagent exists with that name:**
Proceed to Phase 1 below.

### Phase 1: Codebase Analysis

Read `references/artifact-analyzer.md` and follow its analysis instructions to analyze the project at the current working directory.

Focus on: all agents in `.claude/agents/` and `plugins/*/agents/`; their tool restrictions, model choices, `maxTurns` values; which skills delegate to which agents; naming conventions used for existing agents. Flag any agents similar in purpose to `{requested-name}`.

### Phase 2: Generate Subagent

Before generating, read these reference documents:

- `references/subagent-authoring-guide.md` — when to use subagents, system prompt structure, model selection heuristics, tool restriction patterns, anti-patterns
- `references/subagent-config-reference.md` — YAML frontmatter fields, valid model IDs, tool allowlist/denylist, orchestration patterns, plugin restrictions
- `references/prompt-engineering-strategies.md` — subagent-specific prompting (role prompting, structured output, confidence filtering)

Read `assets/templates/subagent-definition.md` and fill its placeholders using:

- User requirements for the new subagent (role, purpose, tools needed)
- Phase 1 analysis output (existing agents, naming conventions, delegation patterns)
- Evidence from the reference files above

Apply model selection heuristic:

- `haiku` — fast read-only exploration agents (simple lookups, no reasoning required)
- `sonnet` — standard analysis and review agents (default for most subagents)
- `opus` — complex multi-step reasoning only (requires explicit justification)

Determine target location:

- `.claude/agents/{name}.md` — project-level agent (accessible everywhere)
- `plugins/{plugin}/agents/{name}.md` — plugin-scoped agent (restricted to plugin context)

### Phase 3: Self-Validation

Read `references/subagent-validation-criteria.md` and execute its **Validation Loop Instructions** against the generated subagent definition.

The loop evaluates all hard limits and quality checks, fixes any failures, and re-evaluates — maximum 3 iterations. Do not proceed to Phase 4 until ALL criteria pass.

### Phase 4: Present and Write

1. Show the user the complete generated subagent definition
2. Cite the evidence from reference files that informed key decisions:
   - Why this model was chosen (heuristic applied)
   - Why these tools are included/excluded (principle of least privilege)
   - What the output format enforces and why
3. If the user requested plugin-restricted fields (`hooks`, `mcpServers`, `permissionMode`), warn that these fields are ignored in plugin context
4. Ask for confirmation before writing any files
5. On approval, write the subagent definition to the target location
