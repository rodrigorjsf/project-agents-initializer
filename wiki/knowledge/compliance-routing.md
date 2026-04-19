# Compliance Routing

**Summary**: Decision table mapping every validator scope to its named source bundle, primary directories, forbidden sources, and recommended search queries — derived from the normative-source-matrix.
**Sources**: docs/compliance/normative-source-matrix.md
**Last updated**: 2026-04-19

---

> **Derived view** — This page is a compact routing reference for validators. The authoritative definitions live in [[normative-source-matrix]] (`docs/compliance/normative-source-matrix.md`). If those definitions change, this page must be updated to match.

Before loading any platform-specific conventions, run `search_docs("compliance routing [scope]")` to retrieve the routing entry for your validation context. This prevents loading forbidden sources and reduces retrieval noise.

---

## Routing Decision Table

| Scope | Named Bundle | Primary Source Dirs | Forbidden Sources |
|-------|-------------|---------------------|-------------------|
| Claude Code plugins (`agents-initializer`, `agent-customizer`) | `claude-plugin-bundle` | `docs/claude-code/`, `docs/general-llm/`, `docs/shared/`, `docs/analysis/` | All `docs/cursor/**`, all `CURSOR-*` sources |
| Cursor IDE plugin (`cursor-initializer`) | `cursor-plugin-bundle` | `docs/cursor/`, `docs/general-llm/`, `docs/shared/`, `docs/analysis/` | All `docs/claude-code/**`, all `CLAUDE-*` sources |
| Standalone skills (`skills/`) | `standalone-bundle` | `docs/shared/`, `docs/general-llm/`, `skills/` | All `docs/claude-code/**`, all `docs/cursor/**`, all `CLAUDE-*`, all `CURSOR-*`, hook/subagent-specific guidance |
| Repository governance | `governance-bundle` | `DESIGN-GUIDELINES.md`, `docs/claude-code/memory/`, `docs/general-llm/` | Completed PRPs, historical plans, `next-steps.md` |
| Claude Code plugins (agent-customizer only) | `agent-customizer-bundle` (extends `claude-plugin-bundle`) | As `claude-plugin-bundle` + `docs/claude-code/hooks/`, `instr:rules` | All `docs/cursor/**` |

---

## Recommended Search Queries per Scope

### Claude Code plugin scope
```
search_docs("claude code skill SKILL.md format")
search_docs("claude code agent definition frontmatter")
search_docs("claude code plugin structure manifest")
search_code("plugins/agents-initializer SKILL.md pattern")
```

### Cursor IDE plugin scope
```
search_docs("cursor rule mdc format activation modes")
search_docs("cursor skill SKILL.md invocation")
search_docs("cursor plugin manifest bundling")
search_code("plugins/cursor-initializer SKILL.md pattern")
```

### Standalone skills scope
```
search_docs("agent skills standard specification")
search_docs("standalone skill inline bash analysis")
search_code("skills/ SKILL.md pattern")
```

### Repository governance scope
```
search_docs("design guidelines evidence research")
search_docs("CLAUDE.md hierarchy progressive disclosure")
```

---

## Scope-Specific Pages

For a detailed routing guide including entry points, validation paths, and common gotchas:

- [[validation-routing-claude]] — Claude Code plugin validation
- [[validation-routing-cursor]] — Cursor IDE plugin validation
- [[validation-routing-standalone]] — Standalone skills validation
