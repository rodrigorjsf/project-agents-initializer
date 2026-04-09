# Instruction Writing Guide

Standards for writing effective GitHub Copilot review instruction files. Derived from GitHub official documentation and this project's prompt engineering research.

Source: GitHub Docs — Adding repository custom instructions, Copilot code review tutorial, docs/claude-prompting-best-practices.md

## Hard Constraints

| Constraint | Value | Applies To |
|-----------|-------|-----------|
| Character limit | 4,000 chars | Code review only |
| File location | `.github/instructions/` | All instruction files |
| File naming | Must end with `.instructions.md` | All instruction files |
| Frontmatter | YAML with `applyTo` required | All instruction files |
| External links | NOT followed by Copilot | Never include URLs as references |

## Frontmatter Format

```yaml
---
applyTo: "glob/pattern/**/*.ext"
---
```

Multiple patterns use comma separation: `applyTo: "**/*.ts,**/*.tsx"`

Optional: `excludeAgent: "code-review"` or `excludeAgent: "cloud-agent"` to limit which Copilot feature uses the file.

## Writing Effective Directives

### Do

- Use imperative statements: "Flag any...", "Check for...", "Verify that..."
- Be specific: name exact fields, patterns, or values to check
- Group related directives under clear `##` headings
- Include short code examples showing correct AND incorrect patterns
- Place highest-priority rules first (lost-in-the-middle effect — models retrieve best from start and end)
- End with a "Common Issues to Flag" bullet list as a quick-reference checklist

### Do Not

- Write narrative paragraphs — use bullet lists
- Include vague quality directives ("be more accurate", "don't miss issues")
- Reference external URLs (copy content inline instead)
- Try to change review comment formatting or UX
- Add instructions about response style or verbosity

## Priority Ordering

Within each instruction file, order content by review impact:

1. **Critical**: Security vulnerabilities, data integrity, architectural violations
2. **High**: Convention violations that cause maintenance problems
3. **Medium**: Style and consistency issues
4. **Low**: Suggestions and improvements

## Character Budget Strategy

Target 2,500-3,500 characters to leave buffer. If over 4,000:

1. Remove lowest-priority items first
2. Compress verbose explanations into terse directives
3. Drop code examples if the directive is clear without them
4. Merge overlapping rules

## Deriving Guidelines from Convention Sources

For each scope, extract review guidelines from:

1. **`.claude/rules/` files** — direct conversion: each rule becomes a review directive
2. **`DESIGN-GUIDELINES.md`** — extract the "In practice" and implemented-in traceability
3. **Plugin/scope CLAUDE.md** — convert conventions to review checks
4. **Actual file patterns** — scan real files to identify undocumented conventions worth reviewing

Test each guideline: "Can a reviewer verify this by looking at the PR diff?" If not, rephrase or remove it.
