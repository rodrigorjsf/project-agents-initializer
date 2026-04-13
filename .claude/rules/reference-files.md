---
paths:
  - "plugins/agents-initializer/skills/*/references/*.md"
  - "plugins/cursor-initializer/skills/*/references/*.md"
  - "plugins/agent-customizer/skills/*/references/*.md"
  - "skills/*/references/*.md"
---
# Reference File Conventions

- Files over 100 lines MUST include a `## Contents` table of contents after the title block
- Maximum 200 lines per reference file
- Content must be framed as "read as instructions" — not as executable scripts
- Each file must have a clear source attribution (e.g., `Source: docs/research-*.md`)
- Identical-content parity applies only to explicitly shared references and same-platform copies
- Platform-specific references may reuse filenames when their content is intentionally platform-native
- No nested references — reference files must not import or reference other reference files
