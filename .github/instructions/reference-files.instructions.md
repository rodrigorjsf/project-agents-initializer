---
applyTo: "**/references/**/*.md"
---

# Reference File Review Guidelines

## Hard Limits

- Maximum 200 lines per reference file — flag any file exceeding this
- Files over 100 lines MUST include a `## Contents` table of contents after the title block
- Reference files must be one level deep from SKILL.md — no nested `references/references/` paths

## Content Requirements

- Content must be framed as instructions ("do this", "check for") — not as executable scripts or documentation
- Each file must have clear source attribution (e.g., `Source: docs/research-*.md` or citing specific Anthropic docs)
- No nested references — reference files must not import or reference other reference files

## Cross-Distribution Parity

- Explicitly shared references MUST have identical content across their intended copies
- Platform-specific references may reuse filenames when the target artifact system differs
- When reviewing a change to an intentionally shared reference, verify the same change is applied to all intended copies

## Information Density

- Prefer tables and structured formats over prose paragraphs
- Each instruction must be specific and actionable — flag vague guidance like "ensure quality"
- Content should provide high signal per token — avoid repetition or filler

## Common Issues to Flag

- Missing source attribution
- Reference file exceeding 200 lines
- Files over 100 lines missing `## Contents` TOC
- Content framed as documentation rather than instructions
- Importing or referencing other reference files (nesting violation)
- Divergence from copies in other distributions
