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

> Empty until artifact-type slices populate it. Each slice (rules / hooks / skills / subagents support) adds one section per skill it ships, listing every reference file in that skill's `references/` directory alongside its source documents.

### create-rule

_(populated by the rules-support slice)_

### improve-rule

_(populated by the rules-support slice)_

### create-hook

_(populated by the hooks-support slice)_

### improve-hook

_(populated by the hooks-support slice)_

### create-skill

_See § Slice E below._

### improve-skill

_See § Slice E below._

### create-subagent

_(populated by the subagents-support slice)_

### improve-subagent

_(populated by the subagents-support slice)_

---

## Slice E: skills

This slice populates the `create-skill` and `improve-skill` reference inventories. Two references are copied **verbatim** from the `agent-customizer` skill-authoring pair (matching that pair's intentional cross-skill scoping); the rest are derived from local Cursor documentation.

### create-skill

| Reference File | Source Type | Source |
|----------------|-------------|--------|
| `references/skill-authoring-guide.md` | Derived (≤200 lines, with attribution) | `docs/cursor/skills/agent-skills-guide.md` |
| `references/skill-format-reference.md` | Derived | `docs/cursor/skills/agent-skills-guide.md` |
| `references/skill-validation-criteria.md` | Derived | `docs/cursor/skills/agent-skills-guide.md` |
| `references/behavioral-guidelines.md` | Verbatim copy | `plugins/agent-customizer/skills/create-skill/references/behavioral-guidelines.md` |
| `references/prompt-engineering-strategies.md` | Verbatim copy | `plugins/agent-customizer/skills/create-skill/references/prompt-engineering-strategies.md` |

### improve-skill

| Reference File | Source Type | Source |
|----------------|-------------|--------|
| `references/skill-authoring-guide.md` | Derived (≤200 lines, with attribution) | `docs/cursor/skills/agent-skills-guide.md` |
| `references/skill-format-reference.md` | Derived | `docs/cursor/skills/agent-skills-guide.md` |
| `references/skill-validation-criteria.md` | Derived | `docs/cursor/skills/agent-skills-guide.md` |
| `references/skill-evaluation-criteria.md` | Derived | `docs/cursor/skills/agent-skills-guide.md` |
| `references/behavioral-guidelines.md` | Verbatim copy | `plugins/agent-customizer/skills/create-skill/references/behavioral-guidelines.md` |
| `references/prompt-engineering-strategies.md` | Verbatim copy | `plugins/agent-customizer/skills/create-skill/references/prompt-engineering-strategies.md` |

The two verbatim files are copied (not symlinked) into both `create-skill/references/` and `improve-skill/references/`. When the canonical copy under `agent-customizer` changes, every copy listed above must be re-validated for byte equivalence.

---

## Source Doc Index

| Source Doc | Referenced By (count) |
|------------|----------------------|
| `docs/cursor/skills/agent-skills-guide.md` | 7 |
| `plugins/agent-customizer/skills/create-skill/references/behavioral-guidelines.md` | 2 |
| `plugins/agent-customizer/skills/create-skill/references/prompt-engineering-strategies.md` | 2 |
