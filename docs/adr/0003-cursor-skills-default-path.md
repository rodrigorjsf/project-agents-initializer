# cursor-customizer:create-skill defaults to .cursor/skills/

Cursor's Agent Skills standard recognises three project-level discovery paths: `.agents/skills/` (open-standard, portable across Agent Skills implementations), `.cursor/skills/` (Cursor-specific), and `~/.cursor/skills/` (user-global). The `cursor-customizer:create-skill` skill writes new skills to `.cursor/skills/` by default and documents the user-driven move to `.agents/skills/` for projects that need cross-tool portability.

The decision aligns the generated artifact with the plugin's namespace (`cursor-customizer`), which simplifies troubleshooting and matches the user's stated intent of a Cursor-targeted distribution. The portable `.agents/skills/` path was rejected as the default because it introduces an implicit coupling to other Agent Skills consumers that the user may not want; the interactive-prompt option was rejected because it adds friction to a one-time investment workflow.
