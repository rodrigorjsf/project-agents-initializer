# Research Document Template

## Metadata

```markdown
---
date: {ISO timestamp with timezone}
git_commit: {short hash}
branch: {branch name}
repository: {repo name}
topic: "{User's Question/Topic}"
tags: [research, codebase, {relevant-component-names}]
status: complete
last_updated: {YYYY-MM-DD}
---
```

## Document Structure

```markdown
# Research: {User's Question/Topic}

**Date**: {ISO timestamp}
**Git Commit**: {short hash}
**Branch**: {branch name}
**Repository**: {repo name}

## Research Question

{Original user query}

## Summary

{High-level documentation of what was found}

## Detailed Findings

### {Component/Area 1}

- Description of what exists (`file.ts:123`)
- How it connects to other components
- Current implementation details

### {Component/Area 2}

...

## Code References

| File | Lines | Description |
|------|-------|-------------|
| `path/to/file.ts` | 123-145 | {What's there} |

## Architecture Documentation

{Current patterns, conventions, and design implementations found}

## Open Questions

- {Areas that need further investigation}
```

## GitHub Permalinks

When on main or a pushed branch, replace local file references with:
`https://github.com/{owner}/{repo}/blob/{commit}/{file}#L{line}`

Get permalink base:
```bash
gh repo view --json owner,name -q '"\(.owner.login)/\(.name)"'
```

## Follow-up Format

When appending to existing research (`--follow-up`):

1. Update frontmatter: `last_updated` and add `last_updated_note`
2. Append new section:

```markdown
## Follow-up Research {timestamp}

### Additional Findings

{New findings with file:line references}
```
