# Operation Log

---

## 2026-04-19 — Phase 8: RAG & wiki hardening

**Source**: `docs/compliance/normative-source-matrix.md` (bundle definitions at lines 261-306)

**Pages created:** 4 routing pages under `Compliance & Validation`

- `compliance-routing.md` — master routing decision table (scope → bundle → sources → queries)
- `validation-routing-claude.md` — Claude plugin scope routing guide
- `validation-routing-cursor.md` — Cursor plugin scope routing guide
- `validation-routing-standalone.md` — Standalone scope routing guide

**wiki/knowledge/ added to RAG `docs` collection** via `rag.config.yaml` update. Reindexed via `uv run --project rag python -m rag index --config rag.config.yaml`.

**Pages updated:** `index.md` — added `## Compliance & Validation` section; count updated 26 → 30.

---

## 2026-04-18 — Batch ingest from docs/

**Source directories scanned:**

- `docs/analysis/` (16 files)
- `docs/claude-code/` (9 files)
- `docs/cursor/` (13 files)
- `docs/general-llm/` (10 files)
- `docs/shared/` (8 files)
- `docs/compliance/` (4 files + reports)

**Pages created:** 26 content pages + index.md + log.md

**Categories:**

- Foundational Concepts: 4 pages (context-engineering, context-rot, progressive-disclosure, prompt-engineering)
- Agent Architecture: 5 pages (evaluating-agents-paper, agent-workflows, subagents, agent-configuration-files, agent-best-practices)
- Claude Code Platform: 5 pages (skills, hooks, plugins, memory, subagents)
- Cursor IDE Platform: 7 pages (rules, skills, subagents, plugins, hooks, mcp, tools)
- Agent Skills Standard: 2 pages (agent-skills-standard, skill-authoring)
- Research: 3 pages (persuasion-in-ai, multilingual-performance, whitespace-and-formatting)

**Method:** Parallel explore agents extracted structured knowledge from all source docs; pages synthesized as concept-oriented knowledge (not 1:1 source summaries) with cross-references via `[[knowledge-links]]`.

**Excluded:** `docs/plans/` (historical design documents per project convention)

---

## 2026-04-18 — Depth expansion pass

**Reason:** Initial batch ingest pages were unconsciously capped at ~60-113 lines due to reference file conventions bleeding into wiki authoring. Wiki pages have no line limit per wiki/CLAUDE.md.

**Pages expanded (10 of 26):**

| Page                        | Before | After | Key additions                                                                                |
| --------------------------- | ------ | ----- | -------------------------------------------------------------------------------------------- |
| claude-code-hooks.md        | 83     | 266   | Complete 22-event lifecycle table, advanced control patterns, async hooks, security patterns |
| skill-authoring.md          | 113    | 181   | Eval-driven iteration, description optimization, script conventions, multi-model testing     |
| claude-code-subagents.md    | 89     | 168   | Agent Teams (experimental), effort levels, session-scoped hooks, team sizing                 |
| claude-code-plugins.md      | 96     | 153   | Namespace isolation, marketplace format, plugin security constraints, $ARGUMENTS             |
| cursor-mcp.md               | 83     | 144   | Full protocol capabilities, OAuth detail, tool approval, MCP Apps                            |
| prompt-engineering.md       | 71     | 119   | Quantitative benchmarks table, token budget, automated optimization, Reflexion               |
| multilingual-performance.md | 74     | 113   | High-overhead languages, internal English thinking, self-translate strategy, Sabiá-2         |
| subagents.md                | 65     | 102   | System prompt structure, 10 anti-patterns, confidence filtering, community patterns          |
| evaluating-agents-paper.md  | 59     | 90    | Per-model data table, AGENTBENCH methodology, tool mention effects                           |
| context-engineering.md      | 59     | 76    | Implementation strategies detail, Ball of Mud anti-pattern, instruction budget               |

**Total:** 2138 → 2758 lines (+29%), 16 pages unchanged (already adequate)
