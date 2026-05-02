<!-- TEMPLATE: Root AGENTS.md
     Target: 15-40 lines after placeholders are filled
     Rule: Remove any section that would be empty after filling
     Rule: Only include non-standard, non-obvious information
     Rule: This file is loaded on every agent request — keep it minimal
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

## Critical Constraints

<!-- CONDITIONAL: Include ONLY if codebase analysis found 1-3 repo-wide non-obvious constraints,
     architectural boundaries, or domain terms that would cause agent mistakes if omitted.
     This section is especially useful for sparse single-scope projects: prefer short behavioral constraints
     over filler so the root file can still carry enough signal without boilerplate. -->
- `[constraint or non-obvious pattern]`

## Context

<!-- CONDITIONAL: Include ONLY if scopes with genuinely different tooling were detected.
     A simple single-package project should NOT have this section. -->
See scope-specific AGENTS.md files:

- `[scope-path/]` — [one-line scope purpose]

## References

<!-- CONDITIONAL: Include ONLY if domain documentation files were generated.
     Use progressive disclosure: point to docs, don't inline their content. -->
- For [domain topic], see `[path/to/domain-doc.md]`
