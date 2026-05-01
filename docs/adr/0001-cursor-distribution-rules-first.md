# Cursor distribution is rules-first; AGENTS.md is legacy input only

The Cursor distribution (`cursor-initializer` + `cursor-customizer`) treats `.cursor/rules/*.mdc` as the canonical surface for project conventions. Plugins **never generate** AGENTS.md — when an existing project has one, `cursor-initializer:improve-cursor` recognises it as **legacy input** and proposes a non-destructive migration that decomposes its content into modular rules (the original file is preserved intact; the user removes it manually after validating the generated rules).

This deviates from Cursor's official documentation, which lists AGENTS.md as one of four valid rule types. The deviation is deliberate: a single monolithic AGENTS.md couples unrelated concerns and forces continuous edits to one file, while `.cursor/rules/*.mdc` supports four orthogonal activation modes (`alwaysApply`, `globs`, `description`, manual) that map cleanly to one-concern-per-rule. The trade-off is loss of "developer-written minimal file" gains from the ETH "Evaluating AGENTS.md" study; the mitigation is that the same minimalism principles are encoded into rule-authoring guidance (rule-domain hierarchy: tooling-non-obvious → file-pattern → monorepo-scope → on-demand), not in a separate AGENTS.md template.

## Considered options

- **(A) Strip AGENTS.md entirely** — rejected: legacy projects with significant AGENTS.md investment lose that input silently
- **(B) Rules-first with explicit legacy migration** — accepted
- **(C) Rules-first with optional minimal AGENTS.md** — rejected: reintroduces the monolithic file the posture is trying to eliminate
