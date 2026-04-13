# Scope Registry

Maps project scopes to their `applyTo` patterns, convention sources, and instruction file names. Used by the update-review-instructions skill to generate scoped review guidelines.

## Registered Scopes

| Scope ID | Instruction File | applyTo Pattern | Convention Sources |
|----------|-----------------|-----------------|-------------------|
| skill-files | `skill-files.instructions.md` | `**/skills/*/SKILL.md` | `.claude/rules/plugin-skills.md`, `.claude/rules/cursor-plugin-skills.md`, `.claude/rules/standalone-skills.md`, DESIGN-GUIDELINES.md §7 |
| reference-files | `reference-files.instructions.md` | `**/references/**/*.md` | `.claude/rules/reference-files.md`, DESIGN-GUIDELINES.md §2 |
| agent-definitions | `agent-definitions.instructions.md` | `**/agents/**/*.md` | `.claude/rules/agent-files.md`, `.claude/rules/cursor-agent-files.md`, DESIGN-GUIDELINES.md §6 |
| template-files | `template-files.instructions.md` | `**/assets/templates/**/*.md,**/assets/templates/**/*.mdc` | DESIGN-GUIDELINES.md §15 |
| rules | `rules.instructions.md` | `.claude/rules/**/*.md` | DESIGN-GUIDELINES.md §1, §10 |
| documentation | `documentation.instructions.md` | `docs/**/*.md` | DESIGN-GUIDELINES.md §5, Research Foundation section |
| plugin-config | `plugin-config.instructions.md` | `**/.claude-plugin,**/.cursor-plugin,**/CLAUDE.md,DESIGN-GUIDELINES.md` | DESIGN-GUIDELINES.md §1-§4, plugins/*/CLAUDE.md |
| prp-artifacts | `prp-artifacts.instructions.md` | `**/*.prd.md,**/*.plan.md,.claude/PRPs/**/*.md` | `.claude/PRPs/CLAUDE.md`, CLAUDE.md §Conventions |

## Adding New Scopes

When a new scope is identified (e.g., new file type or directory with distinct conventions):

1. Determine the `applyTo` glob pattern matching the relevant files
2. Identify convention sources (rules, DESIGN-GUIDELINES.md sections, CLAUDE.md files)
3. Add an entry to this registry table
4. Generate the instruction file using the skill's Phase 1-4 workflow

## Scope Coverage Gaps

Review these areas periodically for potential new scopes:

- `.claude/hooks/` — Hook configuration files (if hooks are added)
- `.claude/settings*.json` — Settings files
- `.cursor/rules/` — Generated Cursor rules (output of cursor-initializer skills)
- Root config files — `README.md`, `LICENSE`, `.gitignore`, `next-steps.md`
