---
paths:
  - "[glob pattern matching relevant files]"
---
<!-- TEMPLATE: .claude/rules/ Path-Scoped Rule File
     Placement: .claude/rules/[topic-name].md (e.g., .claude/rules/testing.md)
     Rule: paths: frontmatter is REQUIRED — rules without it load unconditionally (token waste)
     Rule: One topic per file with a descriptive filename
     Rule: Only non-obvious conventions that would cause mistakes if not followed
     Rule: Create for TWO categories only:
           1. Convention rules — file-pattern-specific coding conventions
           2. Domain-critical rules — security/privacy/compliance for sensitive file patterns
     Rule: Do NOT create rules for: general project-wide conventions (use root CLAUDE.md),
           scope-wide conventions (use subdirectory CLAUDE.md), or obvious patterns
-->
<!-- CONDITIONAL: Migration context only — apply this block when generating a rule
     from migrated CLAUDE.md/AGENTS.md content (automation migration approved by user).
     MIGRATION: paths: frontmatter must target the specific file patterns the original
       instruction applied to — derive from the source content's context, not generic globs
     MIGRATION: Rewrite content as concise, verifiable instructions — do NOT copy verbatim
       from source (original phrasing may be verbose or vague)
     MIGRATION: Add source attribution comment immediately after frontmatter:
       <!-- Migrated from [source-file]:lines [N-M] -->
     MIGRATION: Migrated rules follow the same two-category constraint above
-->

# [Topic Name]

- [Specific, verifiable instruction]
- [Specific, verifiable instruction]
