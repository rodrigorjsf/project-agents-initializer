<!-- TEMPLATE: Root CLAUDE.md
     Target: 15-40 lines after placeholders are filled
     Rule: Remove any section that would be empty after filling
     Rule: Only include non-standard, non-obvious information
     Rule: This file is loaded at every session start — keep it minimal
     Rule: Maximize on-demand loading via subdirectory CLAUDE.md and .claude/rules/
-->

# [One-sentence project description from codebase analysis]

## Tooling

<!-- CONDITIONAL: Include ONLY if non-standard tooling was detected.
     Remove the entire section if all tooling is standard for the language.
     Remove individual lines where the command is the language/framework default. -->
- Package manager: [only if not the language default]
- Build: `[command]`
- Test: `[command]`
- Lint: `[command]`
- Typecheck: `[command]`
<!-- CONDITIONAL: Non-standard configuration values — include ONLY if project overrides tool defaults.
     Example: `strict = true` in mypy, `addopts = "--cov=src"` in pytest, line-length override in ruff.
     Remove if all tooling uses default configuration. -->
- Config: `[tool] [key] = [value]`
<!-- CONDITIONAL: Cross-scope prerequisites — include ONLY if a build step in one scope must complete
     before another scope can run (e.g., WASM package must build before web package).
     Remove if no cross-scope ordering dependencies exist. -->
- Prerequisite: `[command]` must run before `[scope]`

## Context

<!-- CONDITIONAL: Include ONLY if scopes with genuinely different tooling were detected.
     A simple single-package project should NOT have this section. -->
See scope-specific CLAUDE.md files:

- `[scope-path/]` — [one-line scope purpose]

## References

<!-- CONDITIONAL: Include ONLY if domain documentation files were generated.
     Use progressive disclosure: point to docs, don't inline their content. -->
- For [domain topic], see `[path/to/domain-doc.md]`
