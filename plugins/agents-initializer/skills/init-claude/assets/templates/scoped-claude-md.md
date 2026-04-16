<!-- TEMPLATE: Scoped CLAUDE.md (one per detected scope)
     Target: 10-30 lines after placeholders are filled
     Rule: Only include information that DIFFERS from root CLAUDE.md
     Rule: One scope per file — don't combine multiple scopes
     Placement: [scope-path]/CLAUDE.md (e.g., packages/api/CLAUDE.md)
     Note: Automatically loaded by Claude Code when working in this subdirectory
-->

# [One-sentence scope description]

## Tooling

<!-- CONDITIONAL: Include ONLY commands that differ from root.
     Remove the entire section if this scope uses the same tooling as root. -->
- Build: `[scope-specific command]`
- Test: `[scope-specific command]`
<!-- CONDITIONAL: Include ONLY if this scope has migration commands not in root.
     Remove if no migrations are scoped to this package. -->
- Migrate: `[scope-specific migration command]`

## Conventions

<!-- Include ONLY non-obvious, scope-specific conventions.
     Every instruction must be specific and verifiable.
     Do NOT include standard language conventions the model already knows. -->
- [Specific, verifiable instruction]
