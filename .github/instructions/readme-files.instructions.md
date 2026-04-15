---
applyTo: "README.md,plugins/*/README.md,skills/README.md"
---

# README File Review Guidelines

## Standard Cost Warning Block

Every README must contain the following section verbatim as section 2 (immediately after the title and opening description). Flag any README where this section is absent, paraphrased, or shortened.

Standard wording:

```text
## Cost and Model Guidance

This plugin analyzes your entire codebase before generating or improving configuration files.
Execution cost scales with project size and scope — a large or complex project can be expensive to run.

**Recommended model:** Claude Opus delivers the best analysis quality for this workload.
**Viable alternative:** Claude Sonnet with High effort produces decent results at lower cost.

**Usage pattern:** run each skill once per project, or when the codebase has changed significantly.
Not on every session.

The long-term benefit is that every future agent session becomes cheaper and more accurate after
the generated files are in place. Treat the first execution as a one-time investment — not routine work.
```

The first sentence may be adapted to match the distribution (e.g., "This plugin", "These skills"). Core messaging about Opus, Sonnet High, and one-time investment must not be altered.

## Required Section Order

### Root README

1. Title + one-paragraph description
2. `## Cost and Model Guidance`
3. `## Distributions` — table with links to per-plugin READMEs
4. `## Research Foundation`
5. `## Installation` — one-liner per distribution, each with a link to the plugin README
6. `## Repository Structure`
7. `## Contributing`
8. `## License`

### Plugin / Distribution READMEs

1. Title + one-sentence description
2. `## Cost and Model Guidance`
3. `## Why This Plugin Exists`
4. `## Documentation Base`
5. `## Architecture`
6. `## Skills`
7. `## Installation`
8. `## Usage`
9. `## Anti-Patterns This Plugin Avoids`
10. `## Repository Structure`

## Content Scope Boundaries

- Root README must not contain per-skill detail — flag any skill `### subsection` in the root README
- Each plugin README covers only its own distribution — flag cross-plugin skill references
- `skills/README.md` is the standalone distribution — flag any reference to `init-cursor` or `improve-cursor` (plugin-only skills)
- Installation in root README is one-liners only — full scope/team install detail belongs in plugin READMEs

## Staleness Prevention

- Skill invocation examples must match actual skill directory names under `skills/` or `plugins/*/skills/`
- Plugin installation commands must match the `name` field in the plugin's `plugin.json` manifest
- Repository structure trees must reflect actual directory layouts — verify against the filesystem
- Marketplace identifiers must match entries in `.claude-plugin/marketplace.json` or `.cursor-plugin/marketplace.json`

## Line Budget

- Root README: ≤ 200 lines
- Per-plugin READMEs: ≤ 400 lines
- Flag READMEs that exceed their budget

## Common Issues to Flag

- Missing `## Cost and Model Guidance` section
- `## Cost and Model Guidance` not in position 2 (after title)
- Cost warning text that omits or softens the Opus recommendation or one-time investment framing
- Root README containing plugin-specific `### skill-name` documentation subsections
- Plugin README containing skills from other plugins
- `skills/README.md` referencing `init-cursor` or `improve-cursor`
- Installation commands that don't match `plugin.json` `name` fields
- Skill invocation examples using wrong or missing namespace prefix
- Root README installation one-liners missing links to plugin READMEs
- READMEs over their line budget
