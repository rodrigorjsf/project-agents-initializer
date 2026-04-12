---
applyTo: "**/assets/templates/**/*.md"
---

# Template File Review Guidelines

## Template Metadata

Templates should use HTML comment blocks for metadata:
- `<!-- TEMPLATE: ... -->` for placement, naming, line targets, and embedded rules
- `<!-- CONDITIONAL: ... -->` for optional sections included only when applicable
- `<!-- MIGRATION: ... -->` blocks apply only in improve (not init) context

## Placeholder Conventions

- Use bracket syntax for placeholders: `[PLACEHOLDER_NAME]` or `[placeholder-name]`
- Every placeholder must be filled by a specific skill phase — ambiguous placeholders are a defect
- Line count targets should appear in HTML comments guiding generation

## Content Patterns

- Templates define the exact structure of generated output files
- HTML comments guide the generating agent on what to include/exclude
- Templates must demonstrate progressive disclosure patterns (where to split content)
- Source attribution comments (`<!-- Migrated from [source-file]:lines [N-M] -->`) must be present in migration templates

## Distribution Awareness

- `hook-config.md` template must exist ONLY in plugin improve skill directories — never in standalone
- Standalone templates must never reference hooks or subagents
- Init skill templates do NOT include migration-specific templates

## Common Issues to Flag

- Placeholders without clear fill instructions
- Missing HTML comment metadata
- Hook-related templates in standalone skill directories
- Migration templates in init skill directories
- Templates that would generate files exceeding 200 lines
