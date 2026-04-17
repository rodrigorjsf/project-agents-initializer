---
name: create-rule
description: "Creates new path-scoped .claude/rules/ files grounded in the docs corpus. Generates minimal, specific rules with correct glob patterns. Use when creating a new path-scoped rule from scratch."
---

# Create Rule

Generates a new `.claude/rules/` file with correct glob patterns and minimal, specific instructions grounded in the docs corpus.

## Hard Rules

<RULES>
- **NEVER** create path-scoped rules longer than 50 lines
- **NEVER** create rules for standard conventions Claude already knows (e.g., "write clean code")
- **NEVER** use overly broad glob patterns (`**/*`) unless truly global scope is required
- **EVERY** generated rule MUST have `paths:` YAML frontmatter listing the target glob patterns
- **EVERY** instruction must be specific and verifiable — not vague guidance
- **ONE** topic per rule file — do not bundle unrelated instructions
</RULES>

## Process

### Preflight Check

Check if a rule file already exists in `.claude/rules/` covering the same topic:

- Same filename (e.g., `.claude/rules/{topic}.md` already exists)
- Existing rule with overlapping glob patterns that would create contradiction or duplication

**If a conflicting or duplicate rule already exists:**

1. Inform the user: "A rule covering `{topic}` or overlapping glob patterns already exists."
2. Suggest using the `improve-rule` skill to evaluate and optimize it instead.
3. **STOP** — do not proceed. The user should either choose a different topic/pattern scope or use the improve skill.

**If no conflicting rule exists:**
Proceed to Phase 1 below.

### Phase 1: Codebase Analysis

Read `references/artifact-analyzer.md` and follow its analysis instructions to analyze the project at the current working directory.

Focus on: all `.claude/rules/` files and their path scopes; detect overlapping globs, naming conventions, and any conventions already documented in `CLAUDE.md` that would be redundant in a new rule.

### Phase 2: Generate Rule

Before generating, read these reference documents:

- `references/rule-authoring-guide.md` — when to use rules, path-scoping, glob syntax, and anti-patterns
- `references/prompt-engineering-strategies.md` — rule-specific prompting (zero-shot, no examples in rules)

Read `assets/templates/rule-file.md` and fill its placeholders using:

- User requirements for the new rule (topic, target paths, instructions)
- Phase 1 analysis output (existing rules, gaps, potential contradictions)
- Evidence from the reference files above

Generate a path-scoped rule:

- Include `paths:` YAML frontmatter with specific glob patterns (max 50 lines)

Generate: `.claude/rules/{topic-name}.md`

### Phase 3: Self-Validation

Read `references/rule-validation-criteria.md` and execute its **Validation Loop Instructions** against the generated rule.

The loop evaluates all hard limits and quality checks, fixes any failures, and re-evaluates — maximum 3 iterations. Additionally, cross-check against ALL existing rule files in `.claude/rules/` for contradictions and overlapping glob patterns. Do not proceed to Phase 4 until ALL criteria pass.

### Phase 4: Present and Write

1. Show the user the complete generated rule file
2. Cite the evidence from reference files that informed key decisions:
   - Why this glob pattern (what files it targets and why)
   - Why each instruction is necessary (what mistakes it prevents)
   - Why this `paths:` scope is correct for the rule
3. Ask for confirmation before writing any files
4. On approval, write the rule file to `.claude/rules/{topic-name}.md`
