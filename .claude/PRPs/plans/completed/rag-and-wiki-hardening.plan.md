# Feature: RAG and Wiki Hardening for Compliance Validation

## Summary

Reduce retrieval noise and misgrounding during compliance validation (Phase 8 of the Repository Compliance Validation and Correction Program, PRD #56) by: (1) indexing the existing 26-page wiki into the `docs` RAG collection; (2) adding four scoped wiki pages that provide thin, derived routing views of the normative-source-matrix; (3) patching the reindex hook to watch `wiki/knowledge/`; (4) adding a `.claude/rules/rag-routing.md` for quality-gate contexts; and (5) embedding a one-line routing prompt in the quality gate SKILL.md — the execution path validators already read. No Python code changes, no new RAG collections.

## User Story

As a compliance validator (or quality-gate agent)
I want to search for "compliance routing [platform]" and get back a compact, authoritative guide telling me which docs to load and which to avoid
So that I retrieve the correct platform-specific content without loading unrelated material

## Problem Statement

- `wiki/knowledge/` (26 pages of curated agent knowledge) is **not indexed** in the RAG system — validators cannot retrieve it via `search_docs()`.
- The `docs` collection is undifferentiated: a query about Cursor rule activation modes can surface Claude Code `.claude/rules/` content, and vice versa.
- No routing guidance exists telling validators which search queries, sources, or bundles apply to their scope.
- The reindex hook (`check-rag-reindex.sh`) does not watch `wiki/knowledge/`, so future wiki edits won't auto-reindex.
- The quality gate SKILL.md loads no routing guidance before delegating to validators.

## Solution Statement

Add `wiki/knowledge/` to the `docs` collection sources in `rag.config.yaml`. Write four scoped routing pages that are thin derived views of `docs/compliance/normative-source-matrix.md`: a master routing table plus one per platform (Claude, Cursor, standalone). Update the wiki index, log, and reindex hook. Add a path-scoped rules file for quality-gate contexts. Add a single routing hint to the quality gate SKILL.md "Convention sources" line. Reindex and verify with adversarial queries checking for forbidden-source contamination.

## Metadata

| Field            | Value                                                                        |
| ---------------- | ---------------------------------------------------------------------------- |
| Type             | ENHANCEMENT                                                                  |
| Complexity       | MEDIUM                                                                       |
| Systems Affected | `rag.config.yaml`, `wiki/knowledge/`, `.claude/hooks/check-rag-reindex.sh`, `.claude/skills/quality-gate/SKILL.md`, `.claude/rules/` |
| Dependencies     | BAAI/bge-small-en-v1.5 (384d, `docs` collection — already loaded); `uv` + `rag` Python package (already configured) |
| Estimated Tasks  | 10                                                                           |

---

## UX Design

### Before State

```
Validator query: "how should I validate a cursor .mdc rule file?"
    ↓
search_docs("cursor rule validation")
    ↓
docs collection (only docs/ indexed — wiki is invisible)
    ↓
Returns: mixed results from docs/claude-code/ and docs/cursor/
         No routing guidance, no scope-scoped entry point
         Validator may load Claude-specific .claude/rules/ content
         for a Cursor validation task → misgrounding

No routing instructions in quality-gate execution path
No wiki routing pages
Reindex hook ignores wiki/knowledge/ edits
```

### After State

```
Validator query: "compliance routing cursor"
    ↓
search_docs("compliance routing cursor")
    ↓
docs collection (wiki/knowledge/ now indexed)
    ↓
Returns: wiki/knowledge/validation-routing-cursor.md (top hit)
         → Decision table: scope=cursor, bundle=cursor-plugin-bundle
         → Primary: docs/cursor/**
         → Forbidden: docs/claude-code/**, .claude/rules/**
         → Recommended queries list

Quality gate SKILL.md: Convention sources note → routing hint loaded before validators run
.claude/rules/rag-routing.md: Path-scoped to .claude/skills/quality-gate/, .claude/agents/
Reindex hook: wiki/knowledge/ changes trigger auto-reindex
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `wiki/knowledge/` | 26 pages, not indexed | 26+4 pages, indexed in `docs` | All wiki knowledge retrievable via `search_docs()` |
| `docs` collection | Only `docs/` directory | `docs/` + `wiki/knowledge/` | ~30 new pages in search space |
| Quality gate SKILL.md | No routing guidance | One-line routing hint in Convention sources | Validators load routing wiki pages before searching |
| Reindex hook | Watches docs/, plugins/, skills/ | + wiki/knowledge/ | Wiki edits auto-reindex |
| `.claude/rules/` | No RAG routing rules | `rag-routing.md` for quality-gate paths | Agents in those paths receive scope-routing instructions |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `rag.config.yaml` | all | Source definition pattern to MIRROR exactly when adding wiki source |
| P0 | `docs/compliance/normative-source-matrix.md` | 260–310 | Named source bundles table — the authoritative data for wiki routing pages |
| P0 | `wiki/CLAUDE.md` | 36–56 | Wiki page format and `[[knowledge-link]]` conventions to follow |
| P1 | `wiki/knowledge/index.md` | all | Existing section structure to extend with new Compliance section |
| P1 | `wiki/knowledge/log.md` | all | Log format to mirror when adding new entry |
| P1 | `.claude/hooks/check-rag-reindex.sh` | 20–47 | Case statement pattern to extend with `wiki/knowledge/**` |
| P1 | `.claude/skills/quality-gate/SKILL.md` | 14 | "Convention sources" line to extend with routing hint |
| P2 | `.claude/rules/rag-storage-and-search.md` | all | Existing RAG rules — `rag-routing.md` must not duplicate |
| P2 | `wiki/knowledge/context-engineering.md` | 1–8 | Wiki page header format (Summary, Sources, Last updated fields) |

**External Documentation:** None — this plan uses only internal project patterns.

---

## Patterns to Mirror

**COLLECTION SOURCE ENTRY (rag.config.yaml):**
```yaml
# SOURCE: rag.config.yaml:17-19
# COPY THIS PATTERN when adding wiki source under docs collection:
sources:
  - path: "docs/"
    patterns: ["*.md"]
    recursive: true
```

**WIKI PAGE HEADER:**
```markdown
# SOURCE: wiki/knowledge/context-engineering.md:1-5
# COPY THIS PATTERN for every new wiki page:
# Page Title

**Summary**: One-sentence description
**Sources**: comma-separated source doc references
**Last updated**: YYYY-MM-DD
```

**RULE FILE FRONTMATTER:**
```yaml
# SOURCE: .claude/rules/rag-storage-and-search.md:1-4
# COPY THIS PATTERN for new rule files:
---
paths:
  - "specific/glob/**/*.ext"
---
```

**REINDEX HOOK CASE STATEMENT:**
```bash
# SOURCE: .claude/hooks/check-rag-reindex.sh:22-36
# COPY THIS PATTERN when adding new watch path:
  docs/*.md|docs/**/*.md)
    MATCHES=true
    ;;
```

**WIKI INDEX TABLE ROW:**
```markdown
# SOURCE: wiki/knowledge/index.md:8-15
# COPY THIS PATTERN for new index section:
## Section Name
| Page | Summary |
| ---- | ------- |
| [[page-name]] | One-line description |
```

---

## Files to Change

| File | Action | Justification |
| ---- | ------ | ------------- |
| `rag.config.yaml` | UPDATE | Add `wiki/knowledge/` as source under `docs` collection |
| `wiki/knowledge/compliance-routing.md` | CREATE | Master routing index: decision table (scope → bundle → forbidden → queries) |
| `wiki/knowledge/validation-routing-claude.md` | CREATE | Claude-scope validator routing: primary/forbidden sources, recommended queries |
| `wiki/knowledge/validation-routing-cursor.md` | CREATE | Cursor-scope validator routing: primary/forbidden sources, recommended queries |
| `wiki/knowledge/validation-routing-standalone.md` | CREATE | Standalone-scope validator routing: primary/forbidden sources, recommended queries |
| `wiki/knowledge/index.md` | UPDATE | Add new "## Compliance & Validation" section with 4 new page entries |
| `wiki/knowledge/log.md` | UPDATE | Add new log entry for Phase 8 wiki additions |
| `.claude/hooks/check-rag-reindex.sh` | UPDATE | Add `wiki/knowledge/*.md|wiki/knowledge/**/*.md)` case to watch pattern |
| `.claude/skills/quality-gate/SKILL.md` | UPDATE | Add routing hint to "Convention sources" note (line 14) |
| `.claude/rules/rag-routing.md` | CREATE | Path-scoped routing rule for quality-gate and validator agent contexts |

---

## NOT Building (Scope Limits)

- **New RAG collections** — `store.py` binary schema requires Python changes across 5 files; `.claude/rules/rag-storage-and-search.md` explicitly treats `docs`/`code` as coordinated schemas, not config-only names. Ruled out per PRD "harden only when evidence shows gap" guidance.
- **New MCP tools** (e.g., `search_wiki`, `search_claude_docs`) — depends on new collections; out of scope.
- **Python changes to `store.py`, `search.py`, `index.py`, `server.py`** — no code changes; YAML + wiki + rules only.
- **Per-platform FTS filtering within a collection** — requires collection-level metadata filtering not in current search.py implementation.
- **Exclude patterns in `rag.config.yaml`** — `SourceConfig` has no `exclude` field; `index.md` and `log.md` will be indexed. This is accepted: both are short, navigational, and low-risk for misgrounding.

---

## Step-by-Step Tasks

### Task 1: UPDATE `rag.config.yaml` — add wiki source

- **ACTION**: Add `wiki/knowledge/` as a second source entry under the `docs` collection
- **IMPLEMENT**: Append under `docs.sources` after the existing `docs/` entry:
  ```yaml
      - path: "wiki/knowledge/"
        patterns: ["*.md"]
        recursive: false
  ```
  Use `recursive: false` — all pages are flat in `wiki/knowledge/`, no subdirectories.
- **MIRROR**: `rag.config.yaml:17-19` — existing source entry format
- **GOTCHA**: Do NOT add a `chunking:` override — inherit the collection-level `markdown_header` strategy. Wiki pages use H2/H3 headers that `split_headers: ["h1", "h2", "h3"]` handles correctly.
- **VALIDATE**: `grep -A3 "wiki/knowledge" rag.config.yaml` — verify the entry exists and is under `docs` collection

---

### Task 2: CREATE `wiki/knowledge/compliance-routing.md`

- **ACTION**: Create the master routing index page with a decision table derived from `normative-source-matrix.md`
- **IMPLEMENT**: Page content must include:
  - Header block: Summary, Sources, Last updated (mirror `context-engineering.md:1-5`)
  - Opening paragraph: what this page is for (validator scope selection)
  - **Decision table**: 4 rows (claude-plugin, cursor-plugin, standalone, governance) × 4 columns (Scope, Named Bundle, Primary Source Dirs, Forbidden Source Dirs)
    - Populate from `docs/compliance/normative-source-matrix.md:261-306` — do NOT invent values
  - **Search query guidance**: for each scope, 2–3 recommended `search_docs()` queries
  - Cross-references: `[[validation-routing-claude]]`, `[[validation-routing-cursor]]`, `[[validation-routing-standalone]]`
  - Authoritative source note: "This table is a derived view of [[normative-source-matrix]]"
- **MIRROR**: `wiki/knowledge/context-engineering.md:1-5` for header; `wiki/knowledge/index.md` table format for the decision table
- **GOTCHA**: This page must NOT define new scope logic — only restate the normative matrix in compact, query-friendly form. If the matrix changes, this page must change too.
- **VALIDATE**: `wc -l wiki/knowledge/compliance-routing.md` — target 60-100 lines (dense but not exhaustive); `grep "normative-source-matrix" wiki/knowledge/compliance-routing.md` — must reference the authority

---

### Task 3: CREATE `wiki/knowledge/validation-routing-claude.md`

- **ACTION**: Create Claude-scope validator routing page
- **IMPLEMENT**: Page content must include:
  - Header block: Summary="Routing guide for validators checking Claude Code plugin artifacts", Sources=normative-source-matrix.md, Last updated=today
  - **Scope identifier**: `claude-plugin-bundle` (from normative-source-matrix.md:261-290)
  - **Primary sources**: `docs/claude-code/`, `docs/general-llm/`, `docs/shared/`, `docs/analysis/`, `plugins/agents-initializer/`, `plugins/agent-customizer/`
  - **Forbidden sources**: All `docs/cursor/`, `docs/cursor/**`, `.cursor/rules/**`
  - **Validation entry points**: relevant `.claude/rules/` files (e.g., `plugin-skills.md`, `agent-files.md`)
  - **Recommended queries** (3–5): `search_docs("claude code plugin skill conventions")`, `search_docs("claude code agent definition")`, `search_code("plugins/agents-initializer SKILL.md pattern")`
  - Cross-reference: `[[compliance-routing]]`
- **MIRROR**: Header and format from `wiki/knowledge/context-engineering.md:1-5`
- **GOTCHA**: Bundle data must match `normative-source-matrix.md:261-290` exactly — read that file before writing
- **VALIDATE**: `grep "claude-plugin-bundle" wiki/knowledge/validation-routing-claude.md` and `grep "Forbidden" wiki/knowledge/validation-routing-claude.md`

---

### Task 4: CREATE `wiki/knowledge/validation-routing-cursor.md`

- **ACTION**: Create Cursor-scope validator routing page
- **IMPLEMENT**: Page content must include:
  - Header block: Summary="Routing guide for validators checking Cursor IDE plugin artifacts"
  - **Scope identifier**: `cursor-plugin-bundle` (from normative-source-matrix.md:261-290)
  - **Primary sources**: `docs/cursor/`, `docs/general-llm/`, `docs/shared/`, `plugins/cursor-initializer/`
  - **Forbidden sources**: All `docs/claude-code/`, `.claude/rules/`, `CLAUDE.md`
  - **Validation entry points**: `.cursor/rules/` patterns, `.mdc` frontmatter requirements
  - **Recommended queries** (3–5): `search_docs("cursor rule activation modes")`, `search_docs("cursor plugin skill format")`, `search_code("cursor-initializer SKILL.md pattern")`
  - Cross-reference: `[[compliance-routing]]`
- **MIRROR**: Same header/table pattern as Task 3
- **GOTCHA**: Must NOT reference Claude Code hooks, paths: frontmatter, or `${CLAUDE_SKILL_DIR}` — those are Claude-only and forbidden for this scope
- **VALIDATE**: `grep "cursor-plugin-bundle" wiki/knowledge/validation-routing-cursor.md` and `grep "Forbidden" wiki/knowledge/validation-routing-cursor.md`

---

### Task 5: CREATE `wiki/knowledge/validation-routing-standalone.md`

- **ACTION**: Create standalone-scope validator routing page
- **IMPLEMENT**: Page content must include:
  - Header block: Summary="Routing guide for validators checking standalone skills (npx skills add distribution)"
  - **Scope identifier**: `standalone-bundle` (from normative-source-matrix.md:261-290)
  - **Primary sources**: `docs/shared/`, `docs/general-llm/`, `skills/`
  - **Forbidden sources**: All `docs/claude-code/`, All `docs/cursor/`, ALL plugin-specific directories
  - **Key constraint**: Standalone skills must use inline bash (no agent delegation); no `${CLAUDE_SKILL_DIR}` references
  - **Recommended queries** (3–5): `search_docs("standalone skill inline analysis")`, `search_code("skills/ SKILL.md pattern")`, `search_docs("agent skills standard specification")`
  - Cross-reference: `[[compliance-routing]]`
- **MIRROR**: Same header/table pattern as Tasks 3 and 4
- **GOTCHA**: `standalone-bundle` forbids BOTH Claude-specific and Cursor-specific material — both must appear in the Forbidden sources list
- **VALIDATE**: `grep "standalone-bundle" wiki/knowledge/validation-routing-standalone.md` and `grep "Forbidden" wiki/knowledge/validation-routing-standalone.md`

---

### Task 6: UPDATE `wiki/knowledge/index.md` — add Compliance section

- **ACTION**: Add a new "## Compliance & Validation" section to the wiki index
- **IMPLEMENT**: Append before the closing of the file (after the existing "## Research" section):
  ```markdown
  ## Compliance & Validation

  | Page                                   | Summary                                                             |
  | -------------------------------------- | ------------------------------------------------------------------- |
  | [[compliance-routing]]                 | Decision table: scope → bundle → primary/forbidden sources → queries |
  | [[validation-routing-claude]]          | Claude plugin scope: primary sources, forbidden sources, query guide |
  | [[validation-routing-cursor]]          | Cursor plugin scope: primary sources, forbidden sources, query guide |
  | [[validation-routing-standalone]]      | Standalone scope: primary sources, forbidden sources, query guide    |
  ```
- **ALSO UPDATE**: The total page count at the top of index.md — currently "Total pages: **26**" → "Total pages: **30**"
- **MIRROR**: `wiki/knowledge/index.md:7-15` — existing section table format
- **VALIDATE**: `grep "compliance-routing" wiki/knowledge/index.md` and `grep "Total pages: \*\*30\*\*" wiki/knowledge/index.md`

---

### Task 7: UPDATE `wiki/knowledge/log.md` — add Phase 8 entry

- **ACTION**: Prepend a new log entry at the top of the log (after the `# Operation Log` header)
- **IMPLEMENT**: New entry format (mirror existing entries at `log.md:5-30`):
  ```markdown
  ## YYYY-MM-DD — Phase 8 RAG & Wiki hardening

  **Source**: Phase 8 of PRD #56 — Repository Compliance Validation and Correction Program

  **Pages created:** 4 compliance/validation routing pages

  **Categories added:**
  - Compliance & Validation: 4 pages (compliance-routing, validation-routing-claude, validation-routing-cursor, validation-routing-standalone)

  **Changes:**
  - `wiki/knowledge/` added to `docs` RAG collection sources in `rag.config.yaml`
  - `wiki/knowledge/` added to reindex hook watch patterns
  - 4 new routing pages are thin derived views of `docs/compliance/normative-source-matrix.md`

  **Known accepted limitation:** `index.md` and `log.md` are also indexed (no exclude filter in `SourceConfig`). Both are navigational/operational pages with low semantic content — misgrounding risk is minimal.
  ```
- **MIRROR**: `wiki/knowledge/log.md:5-30` — existing entry format with Source, Pages created, Method, Excluded
- **VALIDATE**: `head -20 wiki/knowledge/log.md` — verify new entry at top

---

### Task 8: UPDATE `.claude/hooks/check-rag-reindex.sh` — add wiki watch

- **ACTION**: Add `wiki/knowledge/` patterns to the case statement
- **IMPLEMENT**: Insert after line 43 (`.claude/hooks/*.sh` case), before the `esac`:
  ```bash
    wiki/knowledge/*.md|wiki/knowledge/**/*.md)
      MATCHES=true
      ;;
  ```
- **MIRROR**: `.claude/hooks/check-rag-reindex.sh:22-26` — existing case entry format
- **GOTCHA**: Bash `case` patterns use `|` for OR — match the exact syntax of surrounding entries
- **VALIDATE**: `bash -n .claude/hooks/check-rag-reindex.sh` — syntax check passes; `grep "wiki/knowledge" .claude/hooks/check-rag-reindex.sh` — entry exists

---

### Task 9: UPDATE `.claude/skills/quality-gate/SKILL.md` — add routing hint

- **ACTION**: Extend the "Convention sources" line (line 14) with a routing note
- **IMPLEMENT**: Change line 14 from:
  ```
  **Convention sources:** `.claude/rules/`, `plugins/agents-initializer/CLAUDE.md`, `DESIGN-GUIDELINES.md`
  ```
  To:
  ```
  **Convention sources:** `.claude/rules/`, `plugins/agents-initializer/CLAUDE.md`, `DESIGN-GUIDELINES.md`

  **Routing guidance:** For platform-scoped validation, run `search_docs("compliance routing [platform]")` before loading convention files to retrieve the scope-specific source bundle and forbidden-source list. See `[[compliance-routing]]` in the wiki.
  ```
- **MIRROR**: Quality gate SKILL.md metadata block style (bold labels, inline code for paths)
- **GOTCHA**: Add the routing guidance as a separate line after Convention sources — do NOT modify the existing line itself, which is also used by the artifact-inspector agent
- **VALIDATE**: `grep "compliance routing" .claude/skills/quality-gate/SKILL.md`

---

### Task 10: CREATE `.claude/rules/rag-routing.md`

- **ACTION**: Create a path-scoped rule file for quality-gate and validator agent contexts
- **IMPLEMENT**: Content (YAML frontmatter + rules):
  ```markdown
  ---
  paths:
    - ".claude/skills/quality-gate/**"
    - ".claude/agents/**"
  ---

  ## RAG Routing for Validation Contexts

  - Before searching for platform-specific conventions, run `search_docs("compliance routing [scope]")` to load the scoped source bundle and forbidden-source list for that validation context.
  - For Claude Code plugin validation: use `claude-plugin-bundle` (primary: `docs/claude-code/`, forbidden: `docs/cursor/`).
  - For Cursor IDE plugin validation: use `cursor-plugin-bundle` (primary: `docs/cursor/`, forbidden: `docs/claude-code/`, `.claude/rules/`).
  - For standalone skills validation: use `standalone-bundle` (primary: `docs/shared/`, `skills/`, forbidden: `docs/claude-code/`, `docs/cursor/`).
  - Retrieve routing details from wiki pages: `[[compliance-routing]]`, `[[validation-routing-claude]]`, `[[validation-routing-cursor]]`, `[[validation-routing-standalone]]`.
  - Do NOT load `docs/cursor/` sources when validating Claude plugin artifacts, and vice versa.
  ```
- **MIRROR**: `.claude/rules/rag-storage-and-search.md` — frontmatter format, bullet-list assertions style
- **GOTCHA**: Paths must use glob patterns that match actual directories; `.claude/agents/**` may not exist yet — this is fine, rules with non-matching paths simply never load
- **VALIDATE**: `grep "paths:" .claude/rules/rag-routing.md` and `cat .claude/rules/rag-routing.md | head -10`

---

### Task 11: REINDEX — apply all changes

- **ACTION**: Trigger a full reindex to ingest the new wiki pages and wiki source
- **IMPLEMENT**:
  ```bash
  uv run --project rag python -m rag index --config rag.config.yaml
  ```
- **GOTCHA**: This command must be run from the repo root (`/home/rodrigo/Workspace/agent-engineering-toolkit/`) where `rag.config.yaml` lives. The `--config` flag is required.
- **VALIDATE**: Check exit code is 0; look for `wiki/knowledge/` entries in index output; check DB exists at `.rag/knowledge.db`

---

### Task 12: VERIFY — adversarial query validation

- **ACTION**: Run adversarial queries to confirm routing noise reduction
- **IMPLEMENT** (run in Python or via MCP tool tests):

  **Positive recall tests** (must surface routing pages):
  ```python
  # These must return the routing wiki page in top-5
  search_docs("compliance routing cursor", top_k=5)
  search_docs("compliance routing claude", top_k=5)
  search_docs("compliance routing standalone", top_k=5)
  ```

  **Adversarial contamination tests** (must NOT surface cross-platform material):
  ```python
  # Query about Cursor rules — results must NOT include docs/claude-code/ or .claude/rules/ paths
  results = search_docs("cursor rule globs activation", top_k=5)
  assert all("claude-code" not in r["file_path"] for r in results), "Claude content leaked into Cursor query"

  # Query about Claude Code hooks — results must NOT include docs/cursor/ paths
  results = search_docs("claude code hook lifecycle events", top_k=5)
  assert all("cursor" not in r["file_path"] for r in results), "Cursor content leaked into Claude query"
  ```

  **Wiki visibility test** (wiki pages must now be retrievable):
  ```python
  results = search_docs("context engineering token budget", top_k=5)
  assert any("wiki/knowledge" in r["file_path"] for r in results), "Wiki pages not indexed"
  ```

- **MIRROR**: `rag/search.py:55-114` for the search API; `rag/server.py:44-93` for MCP tool reference
- **GOTCHA**: The adversarial tests check file_path in results — the path stored will be relative to repo root. Use `search_all()` if `search_docs` alone is insufficient.
- **VALIDATE**: All 3 contamination assertions pass; routing pages appear in positive recall queries

---

## Testing Strategy

| What to Test | Method | Validates |
|-------------|--------|-----------|
| Wiki source ingestion | Check `.rag/knowledge.db` after reindex; run `search_docs("wiki compliance routing")` | `rag.config.yaml` update correct |
| Routing page retrievability | Positive recall queries (Task 12) | Wiki pages indexed and retrievable |
| Forbidden-source contamination | Adversarial queries (Task 12) | Existing platform separation holds post-index |
| Hook syntax | `bash -n .claude/hooks/check-rag-reindex.sh` | Bash case statement addition valid |
| Rule file path scoping | `cat .claude/rules/rag-routing.md` — verify paths frontmatter | Rule applies only to quality-gate + agent contexts |

**Edge Cases:**
- Wiki pages with no H2/H3 headers: `markdown_header` strategy falls back to full-page chunks — acceptable, routing pages use tables which are always single-chunk
- `index.md` / `log.md` in search results: these are navigational pages with low semantic content; if they surface for compliance queries, they won't cause misgrounding (they contain only names/links)
- Empty wiki/knowledge/ subdirectory match: `recursive: false` prevents subdirectory traversal — correct since pages are flat
- Reindex with models not cached: `uv run --project rag python -m rag index` downloads models to `.rag/models/` if not already cached — first run may be slow

---

## Validation Commands

```bash
# Syntax check on hook (no model required)
bash -n .claude/hooks/check-rag-reindex.sh

# Verify wiki source in config
grep -A4 "wiki/knowledge" rag.config.yaml

# Verify routing pages exist
ls wiki/knowledge/compliance-routing.md wiki/knowledge/validation-routing-claude.md \
   wiki/knowledge/validation-routing-cursor.md wiki/knowledge/validation-routing-standalone.md

# Verify wiki added to index
grep "compliance-routing" wiki/knowledge/index.md

# Full reindex
uv run --project rag python -m rag index --config rag.config.yaml

# Positive recall: routing page must appear (requires .rag/knowledge.db)
uv run --project rag python -c "
from rag.search import SearchEngine
from rag.config import load_config
cfg = load_config('rag.config.yaml')
engine = SearchEngine(cfg)
results = engine.search('docs', 'compliance routing cursor', top_k=5)
paths = [r['file_path'] for r in results]
print('Paths:', paths)
assert any('validation-routing-cursor' in p for p in paths), 'Routing page not found!'
print('PASS: routing page retrieved')
"

# Adversarial: no claude-code content in cursor query
uv run --project rag python -c "
from rag.search import SearchEngine
from rag.config import load_config
cfg = load_config('rag.config.yaml')
engine = SearchEngine(cfg)
results = engine.search('docs', 'cursor rule globs activation', top_k=5)
contaminated = [r['file_path'] for r in results if 'claude-code' in r['file_path']]
if contaminated: print('WARNING: Claude content in Cursor query:', contaminated)
else: print('PASS: no cross-platform contamination')
"
```

---

## Acceptance Criteria

- [ ] `wiki/knowledge/` appears as a source under `docs` collection in `rag.config.yaml`
- [ ] Four routing wiki pages created: `compliance-routing.md`, `validation-routing-claude.md`, `validation-routing-cursor.md`, `validation-routing-standalone.md`
- [ ] Each routing page cites `normative-source-matrix.md` as authority (no invented scope logic)
- [ ] `wiki/knowledge/index.md` has a new "## Compliance & Validation" section with all 4 pages listed; total count updated to 30
- [ ] `wiki/knowledge/log.md` has new entry for Phase 8
- [ ] `.claude/hooks/check-rag-reindex.sh` watches `wiki/knowledge/*.md`; `bash -n` passes
- [ ] `.claude/skills/quality-gate/SKILL.md` has routing hint after Convention sources line
- [ ] `.claude/rules/rag-routing.md` created with correct `paths:` scoping to quality-gate and agents
- [ ] `uv run --project rag python -m rag index` exits 0 after all changes
- [ ] Positive recall: `search_docs("compliance routing cursor")` returns `validation-routing-cursor.md` in top-5
- [ ] Positive recall: wiki pages generally retrievable (`search_docs("context engineering token budget")` returns wiki path)
- [ ] Adversarial: no documented forbidden-source contamination on platform-specific queries

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| ---- | ---------- | ------ | ---------- |
| `index.md`/`log.md` pollute search results | LOW | LOW | Both are navigational/short; monitor in verify step; future: add `exclude` to `SourceConfig` if needed |
| Routing pages compete with actual docs for top-k slots (crowd-out) | MEDIUM | MEDIUM | Keep routing pages focused and compact (60-100 lines); if crowd-out observed, refine page headers to be less generic |
| Normative matrix changes without routing pages updating | MEDIUM | HIGH | Routing pages include explicit "derived view" disclaimer with `[[normative-source-matrix]]` cross-ref; future: add parity check |
| Reindex fails due to missing model cache | LOW | LOW | Models already cached from prior indexing; add `--force-download` flag if needed |
| `store.py` binary dispatch returns wrong collection for `wiki` path | N/A | N/A | No new collection added; wiki goes into existing `docs` collection — no dispatch change needed |

---

## Notes

**Why no new collections?** The PRD explicitly says "Harden RAG only when evidence shows a gap" and "Extend knowledge layer only when needed." Adding new collections requires Python changes to `store.py:295-422` (binary if/else dispatch), `server.py`, `search.py`, and `index.py`. The `.claude/rules/rag-storage-and-search.md` rule explicitly says "Treat `docs` and `code` as coordinated schemas, not config-only names." The wiki-into-docs approach achieves the Phase 8 success signal with YAML-only changes.

**Why `recursive: false` for wiki?** All 30 wiki pages are flat in `wiki/knowledge/` — no subdirectories exist. `recursive: false` is cleaner than `true` and avoids accidentally indexing any future subdirectory that isn't curated knowledge.

**Future path**: If adversarial verification shows contamination that wiki routing can't fix, Phase 9 can revisit adding platform-scoped collections — but that would require a new plan with Python changes.

**PRD reference:** `.claude/PRPs/prds/repository-compliance-validation-and-correction.prd.md` — Phase 8, lines 199-202.

**GitHub issue:** #56 — Repository Compliance Validation and Correction Program.
