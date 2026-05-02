# Docs Drift Manifest

Centralized registry of all reference file → source doc mappings for drift detection across the `cursor-customizer` plugin.

base_path: `plugins/cursor-customizer/skills/`

## Purpose

This manifest maps every per-skill reference file under `plugins/cursor-customizer/skills/*/references/` to the source documents it distills. Source documents are:

- **Primary** — Cursor official documentation under `docs/cursor/` (`rules.md`, `hooks-guide.md`, `agent-skills-guide.md`, `subagents-guide.md`).
- **Industry Research** — vendor-neutral research (e.g., ETH Zurich "Evaluating AGENTS.md", "Lost in the Middle", general context-engineering studies). Cited as research, never as product guidance.

The manifest enables auditable drift detection: when a source document changes, every reference file derived from it must be re-validated and either confirmed unchanged or refreshed.

## How to Use

The `docs-drift-checker` agent (landing in a follow-up slice) reads this manifest and verifies that:

1. Each reference file's attributed source documents still exist on disk.
2. The cited line ranges (where given) contain content consistent with the reference file's claims.
3. The set of reference files matches the set tracked here — no orphaned references, no missing entries.

The check runs as part of the plugin's quality gate and may also be invoked manually during documentation audits.

---

## Reference File Registry

> Each slice (rules / hooks / skills / subagents support) adds one section per skill it ships, listing every reference file in that skill's `references/` directory alongside its source documents.

## Slice C: rules

### create-rule

| Reference File | Source Document(s) | Derivation |
|----------------|-------------------|------------|
| `references/rule-authoring-guide.md` | `docs/cursor/rules/rules.md` | Derived: distilled guidance on activation modes, frontmatter contract, glob syntax, and anti-patterns. ≤200 lines. Source attribution at top. |
| `references/rule-validation-criteria.md` | `docs/cursor/rules/rules.md`; Industry Research (`research-context-engineering-comprehensive.md`) | Derived: hard limits, quality checks, `.mdc`-specific checks, validation-loop instructions. |
| `references/prompt-engineering-strategies.md` | `plugins/agent-customizer/skills/create-rule/references/prompt-engineering-strategies.md` | Verbatim copy. Vendor-neutral content; per the per-skill-copy convention this file is duplicated, not symlinked. |

### improve-rule

| Reference File | Source Document(s) | Derivation |
|----------------|-------------------|------------|
| `references/rule-authoring-guide.md` | `docs/cursor/rules/rules.md` | Verbatim copy of `create-rule/references/rule-authoring-guide.md` (per the per-skill-copy convention). |
| `references/rule-validation-criteria.md` | `docs/cursor/rules/rules.md`; Industry Research (`research-context-engineering-comprehensive.md`) | Verbatim copy of `create-rule/references/rule-validation-criteria.md`. |
| `references/rule-evaluation-criteria.md` | `docs/cursor/rules/rules.md`; Industry Research (`research-context-engineering-comprehensive.md`) | Derived: bloat / staleness / activation-mode appropriateness rubric and quality scoring. Improve-only reference. |
| `references/prompt-engineering-strategies.md` | `plugins/agent-customizer/skills/create-rule/references/prompt-engineering-strategies.md` | Verbatim copy. Vendor-neutral content; per the per-skill-copy convention this file is duplicated, not symlinked. |

### create-hook

_(populated by the hooks-support slice)_

### improve-hook

_(populated by the hooks-support slice)_

### create-skill

_(populated by the skills-support slice)_

### improve-skill

_(populated by the skills-support slice)_

### create-subagent

_(populated by the subagents-support slice)_

### improve-subagent

_(populated by the subagents-support slice)_

---

## Source Doc Index

_(populated as reference files land; lists each source document and the count of reference files distilling it)_

| Source Doc | Referenced By (count) |
|------------|----------------------|
| _(empty until artifact-type slices add entries)_ | — |

---

## Slice D: hooks

Mappings added by the hooks-support slice. Both `create-hook` and `improve-hook` ship the same two derived references and one verbatim copy.

### Derived references (distilled from a Cursor source doc)

| Reference file | Source doc | Notes |
|----------------|------------|-------|
| `create-hook/references/hook-authoring-guide.md` | `docs/cursor/hooks/hooks-guide.md` | ≤200 lines; covers when-to-use, config structure, two handler types, exit codes + `failClosed`, matchers, locations, security |
| `improve-hook/references/hook-authoring-guide.md` | `docs/cursor/hooks/hooks-guide.md` | Identical to the `create-hook` copy (intra-plugin shared) |
| `create-hook/references/hook-events-reference.md` | `docs/cursor/hooks/hooks-guide.md` | Authoritative Cursor-native event vocabulary the orchestration consults during validation |
| `improve-hook/references/hook-events-reference.md` | `docs/cursor/hooks/hooks-guide.md` | Identical to the `create-hook` copy (intra-plugin shared) |

### Verbatim copy (from the agent-customizer plugin)

| Reference file | Source | Notes |
|----------------|--------|-------|
| `create-hook/references/prompt-engineering-strategies.md` | `plugins/agent-customizer/skills/create-hook/references/prompt-engineering-strategies.md` | Copied verbatim; vendor-neutral prompt-engineering guidance |
| `improve-hook/references/prompt-engineering-strategies.md` | `plugins/agent-customizer/skills/improve-hook/references/prompt-engineering-strategies.md` | Copied verbatim; vendor-neutral prompt-engineering guidance |
