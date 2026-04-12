# Feature: Local RAG Knowledge Base

## Summary

Build a reusable, fully local RAG system using SQLite + sqlite-vec + FTS5 for dual-collection (docs + code) semantic search, exposed via MCP server. Python package managed by uv, embeddings via fastembed (ONNX), code chunking via tree-sitter-language-pack, markdown chunking via header-based parser. Configurable via a single YAML file for portability across projects. Distributed as a git submodule.

## User Story

As an AI coding agent (Claude Code, GitHub Copilot)
I want to semantically search project documentation and source code via MCP tools
So that I can load only the most relevant chunks instead of entire files and stay within my attention budget

## Problem Statement

AI agents load 500-2000 lines per file read to find 20-line answers. No semantic search exists — agents rely on keyword `grep`/`glob`. This project has ~58 markdown docs (~26K lines) plus skills, plugins, scripts. RAG reduces context waste by ≥70%.

## Solution Statement

A Python package (`rag/`) providing: (1) markdown-aware + tree-sitter code chunking, (2) dual-model embedding via fastembed, (3) SQLite storage with separate vec0 tables per collection, (4) hybrid search (vector + FTS5 + RRF), (5) MCP server with `search_docs`, `search_code`, `search_all` tools. Single `rag.config.yaml` drives all project-specific settings.

## Metadata

| Field | Value |
|---|---|
| Type | NEW_CAPABILITY |
| Complexity | HIGH |
| Systems Affected | rag/ (new), .mcp.json (new), .gitignore (update), .claude/hooks/ (new hook) |
| Dependencies | sqlite-vec >=0.1.9, fastembed >=0.8, mcp[cli] >=1.27, pyyaml >=6, tree-sitter-language-pack >=1.5 |
| Estimated Tasks | 18 |

---

## UX Design

### Before State

```
Agent receives task
    → grep/glob for keywords (misses semantic relationships)
    → view entire files (500-2000 lines each)
    → loads 3-5 files = 3000-10000 tokens of mostly irrelevant content
    → may still miss relevant docs in files it didn't open
    → or skip docs entirely and hallucinate
```

### After State

```
Agent receives task
    → calls search_docs("hook validation criteria", top_k=5)
    → receives 5 focused chunks (50-200 lines total) from documentation
    → calls search_code("hook implementation pattern", top_k=3)
    → receives 3 code chunks with function/symbol context
    → total context: ~300 lines, all relevant, with source attribution
    → agent completes task accurately with 70% fewer tokens
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Agent context loading | `view docs/general-llm/research-context-rot-and-management.md` (full 500+ line file) | `search_docs("context rot mechanisms", top_k=5)` (5 focused chunks) | ≥70% context reduction |
| Code pattern discovery | `grep -r "hook" .claude/hooks/` (keyword match, no semantics) | `search_code("PostToolUse hook pattern", top_k=3)` (semantic + keyword match) | Finds conceptually related code, not just keyword matches |
| Cross-domain queries | Read doc files + grep code separately | `search_all("hook validation", top_k=5)` (merged docs + code results) | Single query returns both design rationale and implementation |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude/PRPs/prds/local-rag-knowledge-base.prd.md` | 242-420 | Database schema, config YAML, and hybrid search algorithm to implement EXACTLY |
| P0 | `.claude/PRPs/prds/local-rag-knowledge-base.prd.md` | 480-543 | MCP server tool definitions — copy tool signatures and docstrings exactly |
| P1 | `.claude/hooks/check-docs-sync.sh` | all | PostToolUse hook pattern to MIRROR for auto-reindex hook |
| P1 | `docs/README.md` | 70-80 | "Reading Order by Task" hierarchy — extract reading_order metadata from this |
| P2 | `CLAUDE.md` | all | Project conventions (atomic commits, 200-line limit, file structure) |

**External Documentation (verified via web research):**

| Source | Key API | Why Needed |
|--------|---------|------------|
| [sqlite-vec Python docs](https://alexgarcia.xyz/sqlite-vec/python.html) | `sqlite_vec.load(db)`, `serialize_float32()`, `vec0` virtual tables, `MATCH ? AND k = N` | Core vector storage API |
| [fastembed docs](https://qdrant.github.io/fastembed/) | `TextEmbedding(model_name, cache_dir, lazy_load=True)`, `embed()` returns generator | Embedding generation |
| [tree-sitter-language-pack](https://pypi.org/project/tree-sitter-language-pack/) | `process(source, ProcessConfig(...))`, `detect_language(path)` | Code chunking with built-in `process()` API |
| [MCP Python SDK](https://modelcontextprotocol.io/quickstart/server) | `from mcp.server.fastmcp import FastMCP`, `@mcp.tool()`, `@mcp.resource()`, `mcp.run(transport="stdio")` | MCP server implementation |

---

## Patterns to Mirror

**HOOK_PATTERN** (PostToolUse stdin JSON processing):
```bash
# SOURCE: .claude/hooks/check-docs-sync.sh:1-25
# COPY THIS PATTERN for the auto-reindex hook:
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
file_path=$(echo "$input" | jq -r '.file_path // empty')
# ... check conditions, output JSON with description
```

**CONFIG_YAML_STRUCTURE** (collection-based configuration):
```yaml
# SOURCE: PRD lines 243-320
# The rag.config.yaml structure with per-collection settings
# Each collection has: description, embedding (model, dimensions), sources, chunking
# See PRD for complete reference — implement config.py to load this exact structure
```

**MCP_TOOL_PATTERN** (FastMCP decorator with type hints):
```python
# SOURCE: PRD lines 480-543 + web research
# FastMCP auto-generates JSON schema from type hints + docstrings
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("rag-knowledge-base")

@mcp.tool()
async def search_docs(query: str, top_k: int = 5) -> str:
    """Docstring becomes the tool description for the LLM."""
    # Tool descriptions guide the LLM on when to use each tool (LLM-as-router)
```

**No existing Python patterns in this project** — `rag/` is the first Python code. Follow standard Python best practices: type hints, dataclasses, `if __name__ == "__main__"` guards.

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `rag/pyproject.toml` | CREATE | Python package definition, dependencies, CLI entry points |
| `rag/__init__.py` | CREATE | Package marker with version |
| `rag/__main__.py` | CREATE | `python -m rag` entry point |
| `rag/config.py` | CREATE | YAML config loader, dataclass models for config structure |
| `rag/chunker.py` | CREATE | Markdown header-based document chunker |
| `rag/code_chunker.py` | CREATE | tree-sitter-language-pack code chunker |
| `rag/embedder.py` | CREATE | fastembed multi-model wrapper (lazy loading per collection) |
| `rag/store.py` | CREATE | SQLite + sqlite-vec + FTS5 dual-collection storage |
| `rag/index.py` | CREATE | Full indexing pipeline: scan → route → chunk → embed → store |
| `rag/search.py` | CREATE | Hybrid search (vector + FTS5 + RRF) per collection + cross-collection |
| `rag/server.py` | CREATE | FastMCP server with search_docs, search_code, search_all, get_doc_context, list_documents |
| `rag/cli.py` | CREATE | CLI entry points: `rag index`, `rag init`, `rag search` |
| `rag/README.md` | CREATE | Full documentation: setup, architecture, config reference, usage guide |
| `rag/.gitignore` | CREATE | Ignore `.rag/`, `__pycache__/`, model cache for the standalone repo |
| `rag.config.yaml` | CREATE | Project-specific configuration for agent-engineering-toolkit |
| `.mcp.json` | CREATE | MCP server configuration for Claude Code |
| `.gitignore` | UPDATE | Add `.rag/` directory |
| `.claude/hooks/check-rag-reindex.sh` | CREATE | PostToolUse hook for auto-reindex when docs/code change |

---

## NOT Building (Scope Limits)

- **Unit test framework** — No test infrastructure exists; validation is via CLI commands and manual spot-checks (tests can be added later)
- **PDF parsing** — The one PDF has a markdown counterpart
- **Web UI / query interface** — MCP server is the only consumer interface
- **GPU acceleration** — ONNX CPU inference is sufficient
- **pip-installable package** — Git submodule is the distribution method for v1
- **Cross-encoder reranking** — SHOULD priority from PRD, deferred to post-MVP
- **Query expansion** — SHOULD priority, deferred to post-MVP
- **Multi-user support** — Single developer, single machine

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `rag/pyproject.toml`

- **ACTION**: Create Python package definition with all dependencies
- **IMPLEMENT**:
  - `[project]`: name="rag-local", requires-python=">=3.11", version="0.1.0"
  - Dependencies: `sqlite-vec>=0.1.9`, `fastembed>=0.8`, `mcp[cli]>=1.27`, `pyyaml>=6`, `tree-sitter-language-pack>=1.5`
  - `[project.scripts]`: `rag = "rag.cli:main"` — CLI entry point
  - `[build-system]`: use hatchling (uv default)
- **GOTCHA**: Do NOT include `tree-sitter` as a separate dependency — `tree-sitter-language-pack` is standalone and does not depend on it
- **GOTCHA**: Use `mcp[cli]` not `fastmcp` — the package is `mcp`, FastMCP is a class inside it
- **VALIDATE**: `cd rag && uv sync && uv run python -c "import sqlite_vec; import fastembed; from mcp.server.fastmcp import FastMCP; import yaml; from tree_sitter_language_pack import process"`

### Task 2: CREATE `rag/__init__.py` and `rag/__main__.py`

- **ACTION**: Create package marker and `python -m rag` entry point
- **IMPLEMENT**:
  - `__init__.py`: `__version__ = "0.1.0"`
  - `__main__.py`: `from rag.cli import main; main()`
- **VALIDATE**: `cd rag && uv run python -c "import rag; print(rag.__version__)"`

### Task 3: CREATE `rag/config.py`

- **ACTION**: Create YAML configuration loader with dataclass models
- **IMPLEMENT**:
  - Dataclasses: `RagConfig`, `CollectionConfig`, `SourceConfig`, `ChunkingConfig`, `EmbeddingConfig`, `SearchConfig`, `DatabaseConfig`
  - `load_config(path: str) -> RagConfig`: Load and validate YAML, resolve paths relative to config file location
  - Default values matching the PRD's YAML example (lines 243-320)
  - Support per-source chunking overrides (source-level `chunking` overrides collection-level)
  - Config path resolution: CLI `--config` flag → `rag.config.yaml` in cwd → error
- **GOTCHA**: Paths in config are relative to the project root (where `rag.config.yaml` lives), NOT relative to the `rag/` package directory
- **VALIDATE**: Create a minimal test YAML, load it, verify dataclass fields are populated

### Task 4: CREATE `rag/chunker.py`

- **ACTION**: Create markdown-aware document chunker
- **IMPLEMENT**:
  - `@dataclass ChunkResult`: content, section_header, start_line, end_line, token_count, reading_order (optional)
  - `chunk_markdown(text: str, config: ChunkingConfig, file_path: str = "") -> list[ChunkResult]`:
    - Split on configurable headers (h1, h2, h3 based on `split_headers` config)
    - Keep tables and fenced code blocks atomic (never split mid-block)
    - Recursive character split for sections exceeding `max_tokens`
    - Overlap: carry last `overlap_tokens` from previous chunk
  - `extract_reading_order(docs_readme_path: str) -> dict[str, int]`: Parse `docs/README.md` "Reading Order by Task" section to build `{file_path: order_position}` mapping
  - Token estimation: `len(text.split())` is ~75% accurate, sufficient for chunking
- **GOTCHA**: Tables use `|` delimiters — detect table start/end to keep them atomic. Fenced code blocks use ``` — count fence depth for nested blocks
- **GOTCHA**: Header hierarchy matters — an H3 chunk includes its parent H2 and H1 headers as context in `section_header`
- **VALIDATE**: `uv run python -c "from rag.chunker import chunk_markdown; chunks = chunk_markdown(open('../docs/README.md').read(), ...); print(len(chunks), [c.section_header for c in chunks])"`

### Task 5: CREATE `rag/code_chunker.py`

- **ACTION**: Create AST-based code chunker using tree-sitter-language-pack
- **IMPLEMENT**:
  - `@dataclass CodeChunkResult`: content, language, symbol_type, symbol_name, parent_symbol, start_line, end_line, char_count
  - `chunk_code(source: str, file_path: str, config: ChunkingConfig) -> list[CodeChunkResult]`:
    - Detect language: check config `languages` mapping first, then `detect_language(file_path)` from language-pack
    - If language is "markdown" or file extension is `.md`: delegate to `chunker.chunk_markdown()` — SKILL.md and reference files are markdown, not code
    - Otherwise: use `process(source, ProcessConfig(language=lang, chunk_max_size=config.max_chars, structure=True, docstrings=True))`
    - Map results: access chunk data via `chunk["metadata"]` dict for `start_line`, `end_line`; derive `symbol_type`/`symbol_name` from `result["structure"]` tree (not from `node_types` alone); `parent_symbol` comes from the structure hierarchy
  - Fallback: if tree-sitter fails (unsupported language, parse error), fall back to fixed-size character splitting with line-boundary alignment
- **KEY FINDING**: `tree-sitter-language-pack` has a built-in `process()` API with 3-pass chunking algorithm (collect leaf units → bin-pack → split oversized). This replaces the need for custom AST traversal. Use it directly.
- **GOTCHA**: `process()` result structure: `result["chunks"]` contains chunk dicts with `content`, `start_byte`, `end_byte`, and a `metadata` sub-dict for `start_line`, `end_line`, `node_types`. The `result["structure"]` tree provides the symbol hierarchy — use it to derive `symbol_name` and `parent_symbol`, not `node_types`
- **GOTCHA**: `.yaml`/`.yml` files may not chunk well with tree-sitter — consider using fixed-size splitting for YAML
- **VALIDATE**: `uv run python -c "from rag.code_chunker import chunk_code; chunks = chunk_code(open('../.claude/hooks/check-docs-sync.sh').read(), 'check-docs-sync.sh', ...); print(len(chunks), [(c.symbol_name, c.start_line) for c in chunks])"`

### Task 6: CREATE `rag/embedder.py`

- **ACTION**: Create fastembed multi-model wrapper with lazy loading
- **IMPLEMENT**:
  - `class Embedder`:
    - Constructor: `__init__(self, cache_dir: str = ".rag/models")`
    - `_models: dict[str, TextEmbedding]` — one instance per model name, created on first use
    - `_get_model(model_name: str) -> TextEmbedding`: Lazy-load with `TextEmbedding(model_name=model_name, cache_dir=self.cache_dir, lazy_load=True)`
    - `embed_texts(texts: list[str], model_name: str, batch_size: int = 256) -> list[list[float]]`: Get model, call `model.embed(texts, batch_size=batch_size)`, materialize generator with `list()`, convert each `NDArray[float32]` to Python list via `.tolist()`
    - `embed_query(query: str, model_name: str) -> list[float]`: Use `model.query_embed(query)` — NOT `embed()`. Some models (e.g., bge) prepend a query instruction prefix for retrieval; `query_embed()` handles this automatically
  - **Memory note**: bge-small ~67MB + jina-code ~640MB = ~700MB combined. Each model loads independently on first query to its collection.
- **GOTCHA**: `embed()` returns a **generator** of `NDArray[np.float32]` — MUST materialize with `list()` before accessing elements
- **GOTCHA**: Use `query_embed()` for search queries, `embed()` for document indexing — models with asymmetric encoding (like bge) produce better retrieval with distinct query/document embeddings
- **GOTCHA**: Use `lazy_load=True` in `TextEmbedding()` constructor — defers ONNX session creation until first `embed()` call
- **GOTCHA**: fastembed downloads models on first use. Cache dir: constructor arg > `FASTEMBED_CACHE_PATH` env var > `/tmp/fastembed_cache`
- **VALIDATE**: `uv run python -c "from rag.embedder import Embedder; e = Embedder('../.rag/models'); v = e.embed_query('test', 'BAAI/bge-small-en-v1.5'); print(len(v), type(v[0]))"`

### Task 7: CREATE `rag/store.py`

- **ACTION**: Create SQLite + sqlite-vec + FTS5 dual-collection storage layer
- **IMPLEMENT**:
  - `class Store`:
    - `__init__(self, db_path: str)`: Create directories, open connection, `PRAGMA journal_mode=WAL`, `PRAGMA busy_timeout=5000`, load sqlite-vec extension, create schema
    - `_init_schema()`: Execute CREATE TABLE IF NOT EXISTS for all 8 tables. **IMPORTANT: Denormalize `file_path` into chunk tables** so FTS5 external content works:
      - Shared: `documents` (file_path, collection, title, category, file_hash, chunk_count, indexed_at)
      - Docs: `doc_chunks` (id, document_id, chunk_index, section_header, content, **file_path**, start_line, end_line, token_count, reading_order), `vec_docs USING vec0(embedding float[384], +chunk_id INTEGER)`, `docs_fts USING fts5(content, section_header, file_path, content='doc_chunks', content_rowid='id')`
      - Code: `code_chunks` (id, document_id, chunk_index, content, **file_path**, language, symbol_type, symbol_name, parent_symbol, start_line, end_line, char_count), `vec_code USING vec0(embedding float[768], +chunk_id INTEGER)`, `code_fts USING fts5(content, symbol_name, file_path, language, content='code_chunks', content_rowid='id')`
    - `_create_fts_triggers()`: Create INSERT/DELETE/UPDATE triggers for FTS5 external content sync on BOTH `doc_chunks` and `code_chunks`
    - `upsert_document(file_path, collection, title, category, file_hash) -> int`: Insert or update document record
    - `insert_doc_chunks(doc_id, chunks: list, embeddings: list)`: Bulk insert into `doc_chunks` + `vec_docs` (triggers handle `docs_fts`)
    - `insert_code_chunks(doc_id, chunks: list, embeddings: list)`: Bulk insert into `code_chunks` + `vec_code` (triggers handle `code_fts`)
    - `get_document_hash(file_path) -> str | None`: For incremental change detection
    - `delete_document_chunks(doc_id, collection)`: Delete ALL data for a document — chunks from `doc_chunks`/`code_chunks` (triggers handle FTS), **AND explicitly delete from `vec_docs`/`vec_code` WHERE chunk_id IN (SELECT id FROM {chunks_table} WHERE document_id = ?)** — vec0 tables do NOT have triggers, so deletion must be explicit
    - `delete_stale_documents(collection, current_file_paths: set[str])`: Remove documents from DB that no longer exist on disk — query `documents` table for collection, find file_paths not in `current_file_paths`, call `delete_document_chunks()` for each, then delete from `documents`
    - `vector_search(collection, embedding, top_k) -> list`: KNN search on `vec_docs` or `vec_code`
    - `fts_search(collection, query, top_k) -> list`: FTS5 BM25 search on `docs_fts` or `code_fts`
    - `get_all_documents(collection=None) -> list`: For `list_documents` resource
    - `get_chunks_by_file(file_path) -> list`: For `get_doc_context` tool
    - `rebuild_fts()`: Call `INSERT INTO docs_fts(docs_fts) VALUES('rebuild')` and same for `code_fts` — needed ONLY on first index when triggers weren't present during initial load, or as a repair command
- **KEY API PATTERNS** (from sqlite-vec research):
  - Load extension: `db.enable_load_extension(True); sqlite_vec.load(db)`
  - Serialize embedding: `sqlite_vec.serialize_float32(embedding_list)`
  - KNN query: `WHERE embedding MATCH ? AND k = ?` (portable, works on all SQLite versions)
  - FTS5 external content: `content='doc_chunks', content_rowid='id'` — FTS5 columns MUST match columns in the content table (this is why `file_path` must be denormalized into chunk tables)
  - FTS5 delete trigger: `INSERT INTO docs_fts(docs_fts, rowid, content, section_header, file_path) VALUES('delete', old.id, old.content, old.section_header, old.file_path)` — table name repeated in VALUES is NOT a typo, it's the FTS5 delete command syntax
  - WAL mode: `PRAGMA journal_mode=WAL` — allows concurrent reads while writing (critical for hook-triggered reindex while MCP server reads)
  - Busy timeout: `PRAGMA busy_timeout=5000` — wait up to 5s for locks instead of immediate SQLITE_BUSY error
- **GOTCHA**: FTS5 triggers handle sync for incremental inserts/deletes — do NOT call `rebuild_fts()` on every index run (defeats incremental performance). Only call on first-ever index or as repair
- **GOTCHA**: vec0 tables do NOT support trigger-based deletion — must explicitly DELETE FROM vec_docs/vec_code when removing chunks
- **GOTCHA**: Python 3.14 removed `sqlite3.version` — use `sqlite3.sqlite_version` instead if checking SQLite version
- **GOTCHA**: Use transactions for bulk inserts — wrap chunk insertion in `BEGIN`/`COMMIT` for 10-100x speedup
- **GOTCHA**: Create FTS triggers BEFORE inserting data so that inserts are automatically indexed. Only use `rebuild_fts()` if data was loaded without triggers present
- **VALIDATE**: `uv run python -c "from rag.store import Store; s = Store('/tmp/test-rag.db'); print('Tables:', s.get_all_documents())"`

### Task 8: CREATE `rag.config.yaml`

- **ACTION**: Create project-specific configuration for agent-engineering-toolkit
- **NOTE**: Moved before index.py/server.py because both depend on config at validation time
- **IMPLEMENT**: Copy the YAML from PRD lines 243-320 exactly — it's already tailored for this project with:
  - `docs` collection: `docs/` directory, `*.md` patterns, bge-small 384d, markdown_header chunking
  - `code` collection: `plugins/`, `skills/`, `.claude/hooks/` directories with per-source patterns and chunking overrides
  - Search defaults: top_k=5, max_top_k=10, rrf_k=60
  - Database path: `.rag/knowledge.db`
  - Model cache: `.rag/models`
- **VALIDATE**: `cd rag && uv run python -c "from rag.config import load_config; c = load_config('../rag.config.yaml'); print(list(c.collections.keys()))"`

### Task 9: CREATE `rag/index.py`

- **ACTION**: Create full indexing pipeline: scan → route → chunk → embed → store
- **IMPLEMENT**:
  - `class Indexer`:
    - `__init__(self, config: RagConfig)`: Initialize Store, Embedder, load reading_order from `docs/README.md`
    - `index_all(collection: str | None = None)`: Index all collections (or specific one if `--collection` flag)
    - `index_collection(name: str, collection_config: CollectionConfig)`:
      1. Scan: Walk source directories, apply glob patterns, build file list (`current_files: set[str]`)
      2. **Reconcile stale entries**: Call `store.delete_stale_documents(name, current_files)` — removes documents from DB that no longer exist on disk, cleaning up chunks + vec rows + FTS entries
      3. Change detection: Compare SHA-256 hash with `store.get_document_hash()` — skip unchanged files
      4. Route: Determine chunking strategy (tree_sitter vs markdown_header) per source config
      5. Chunk: Call `chunk_markdown()` or `chunk_code()` based on strategy
      6. Embed: Call `embedder.embed_texts()` with collection's model
      7. For changed files: Delete old chunks first (`store.delete_document_chunks()`), then insert new
      8. Store: Call `store.insert_doc_chunks()` or `store.insert_code_chunks()`
    - `_is_first_index(collection: str) -> bool`: Check if `documents` table has any entries for this collection — if yes, FTS triggers handle sync; if no (first run), call `store.rebuild_fts()` after all inserts
    - `_compute_file_hash(path: str) -> str`: SHA-256 of file contents
    - `_detect_category(file_path: str, collection: str) -> str`: Infer category from path (e.g., `docs/claude-code/` → "claude-code", `plugins/agents-initializer/` → "agents-initializer")
    - `_skip_binary(path: str) -> bool`: Skip binary files by checking for null bytes in first 8KB
    - Report: Print summary — "Indexed N docs (M chunks) + N code files (M chunks), Xs. Removed K stale documents."
  - CLI integration: `python -m rag index [--collection docs|code] [--config path]`
- **GOTCHA**: Embed texts in batches per collection — don't mix models. Batch size 256 is default for fastembed.
- **GOTCHA**: Order matters — delete old chunks BEFORE inserting new ones for a changed file. The `delete_document_chunks()` method handles vec + FTS cleanup.
- **GOTCHA**: Only call `rebuild_fts()` on first-ever index for a collection (no triggers present during initial schema creation) — on subsequent runs, triggers handle FTS sync automatically
- **GOTCHA**: File scanning should skip binary files (PDFs, images) — check for null bytes or use extension allowlist from config patterns
- **VALIDATE**: `cd .. && uv run --project rag python -m rag index --config rag.config.yaml` — should index all docs and code, print summary

### Task 10: CREATE `rag/search.py`

- **ACTION**: Create hybrid search engine with per-collection and cross-collection search
- **IMPLEMENT**:
  - `@dataclass SearchResult`: chunk_id, content, file_path, score, collection, section_header (docs) | symbol_name (code), start_line, end_line, language (code only), reading_order (docs only)
  - `class SearchEngine`:
    - `__init__(self, config: RagConfig)`: Initialize Store, Embedder
    - `search_collection(query: str, collection: str, top_k: int = 5) -> list[SearchResult]`:
      1. Get collection's embedding model from config
      2. Embed query with `embedder.embed_query(query, model_name)` — uses `query_embed()` for asymmetric encoding
      3. Vector KNN: `store.vector_search(collection, embedding, config.search.vector_candidates)`
      4. FTS5: `store.fts_search(collection, fts5_query(query), config.search.fts_candidates)`
      5. RRF fusion: `score(d) = Σ 1/(k + rank + 1)` where k=`config.search.rrf_k` (default 60)
      6. Return top-k results with full metadata from chunk table
    - `search_all(query: str, top_k: int = 5) -> list[SearchResult]`:
      1. `search_collection(query, "docs", top_k * 2)`
      2. `search_collection(query, "code", top_k * 2)`
      3. Normalize scores to 0-1 range per collection (min-max normalization)
      4. Merge, sort by normalized score, return top-k
    - `_fts5_query(query: str) -> str`: Convert natural language to FTS5 query — split on spaces, wrap each token in double quotes (escape special chars), join with OR
  - `format_results(results: list[SearchResult], collection: str) -> str`: Format for MCP tool output — markdown with file path, line range, score, content
- **GOTCHA**: RRF ranks are 1-indexed (rank 1 = best), so formula is `1/(k + rank)` where rank starts at 1
- **GOTCHA**: FTS5 query syntax requires escaping special chars — wrap each token in double quotes for safety
- **GOTCHA**: Cross-collection score normalization is critical — raw RRF scores from different collections are not comparable
- **VALIDATE**: After indexing, `uv run python -c "from rag.search import SearchEngine; from rag.config import load_config; c = load_config('../rag.config.yaml'); s = SearchEngine(c); print(s.search_collection('hook validation', 'docs'))"`

### Task 11: CREATE `rag/server.py`

- **ACTION**: Create FastMCP server with all search tools and list_documents resource
- **IMPLEMENT**:
  - Import: `from mcp.server.fastmcp import FastMCP`
  - **ToolError import**: Verify exact import path at implementation time — try `from mcp.server.fastmcp.exceptions import ToolError`, fall back to `from mcp.shared.exceptions import McpError`. If neither works, use plain `Exception` with error message string
  - `mcp = FastMCP("rag-knowledge-base")`
  - Config + SearchEngine: Lazy-initialize on first tool call (NOT at module level) — avoids import failures when config file doesn't exist yet. Use a module-level `_engine: SearchEngine | None = None` with a `_get_engine()` helper
  - Tools (copy signatures and docstrings from PRD lines 487-535 EXACTLY):
    - `@mcp.tool() async def search_docs(query: str, top_k: int = 5) -> str`
    - `@mcp.tool() async def search_code(query: str, top_k: int = 5) -> str`
    - `@mcp.tool() async def search_all(query: str, top_k: int = 5) -> str`
    - `@mcp.tool() async def get_doc_context(file_path: str) -> str`
  - Resource:
    - `@mcp.resource("docs://index") async def list_documents() -> str`
  - Config path resolution: env var `RAG_CONFIG_PATH` → `rag.config.yaml` in cwd → error on first tool call
  - Entry point: `mcp.run(transport="stdio")`
- **GOTCHA**: NEVER use `print()` in MCP server — it corrupts the JSON-RPC stdio transport. Use `logging` to stderr instead: `logging.basicConfig(stream=sys.stderr)`
- **GOTCHA**: Both sync and async tool functions are supported — use `async def` for consistency with FastMCP examples
- **GOTCHA**: `top_k` must be capped at `config.search.max_top_k` (default 10) in each tool
- **GOTCHA**: Tool docstrings are critical — they are the ONLY way the LLM knows when to use each tool. Copy from PRD exactly.
- **VALIDATE**: `cd rag && uv run python -c "from rag.server import mcp; print(mcp.name)"` — should print "rag-knowledge-base"

### Task 12: CREATE `rag/cli.py`

- **ACTION**: Create CLI entry points for `rag index`, `rag init`, `rag search`
- **IMPLEMENT**:
  - Use `argparse` (stdlib, no extra dependency)
  - `main()`: Parse subcommands
  - `cmd_index(args)`: Load config, create Indexer, call `index_all(collection=args.collection)`
  - `cmd_init(args)`: Scaffold `rag.config.yaml` in current directory with template content + create `.rag/` directory
  - `cmd_search(args)`: Load config, create SearchEngine, call `search_collection()` or `search_all()`, print formatted results — useful for testing without MCP
  - `cmd_serve(args)`: Start MCP server (imports and calls `server.mcp.run()`)
  - Common flags: `--config` (config file path), `--collection` (for index/search)
- **VALIDATE**: `uv run python -m rag --help` — should show subcommands

### Task 13: CREATE `.mcp.json`

- **ACTION**: Create MCP server configuration for Claude Code
- **IMPLEMENT**:
  ```json
  {
    "mcpServers": {
      "rag-knowledge-base": {
        "command": "uv",
        "args": ["run", "--project", "rag", "python", "-m", "rag.server"],
        "env": {
          "RAG_CONFIG_PATH": "rag.config.yaml"
        }
      }
    }
  }
  ```
- **GOTCHA**: The `command` must be `uv` with `--project rag` so it uses the rag package's virtual environment
- **GOTCHA**: Relative paths (`--project rag`, `rag.config.yaml`) are resolved relative to the repo root where `.mcp.json` lives. Claude Code launches MCP servers from the repo root, so relative paths work. Document this assumption in README
- **VALIDATE**: Claude Code should auto-detect and connect to the MCP server on next session start

### Task 14: UPDATE `.gitignore`

- **ACTION**: Add `.rag/` directory to gitignore
- **IMPLEMENT**: Append `.rag/` to existing `.gitignore`
- **VALIDATE**: `git status` should not show `.rag/` after indexing

### Task 15: CREATE `rag/.gitignore`

- **ACTION**: Create gitignore for the standalone rag repository
- **IMPLEMENT**:
  ```
  __pycache__/
  *.pyc
  .venv/
  .rag/
  *.egg-info/
  dist/
  build/
  ```
- **VALIDATE**: File exists and covers Python artifacts

### Task 16: CREATE `.claude/hooks/check-rag-reindex.sh`

- **ACTION**: Create PostToolUse hook for auto-reindex when docs/code change
- **MIRROR**: `.claude/hooks/check-docs-sync.sh` — same stdin JSON processing pattern
- **IMPLEMENT**:
  - Read JSON from stdin (tool_name, file_path)
  - Trigger on: `tool_name` is "Edit" or "Create" AND `file_path` matches patterns from `rag.config.yaml` sources (docs/, plugins/, skills/, .claude/hooks/)
  - Debounce with dirty-flag pattern:
    1. If `.rag/reindex.lock` exists → set `.rag/reindex.dirty` flag → skip (another reindex will pick it up)
    2. Otherwise: create `.rag/reindex.lock`, run reindex, check `.rag/reindex.dirty` after completion — if set, delete dirty flag and rerun
    3. Use `trap 'rm -f .rag/reindex.lock' EXIT` to clean up lock on any exit (including crashes)
  - Action: Run `uv run --project rag python -m rag index --config rag.config.yaml` in background
  - Output: JSON `{"description": "🔄 RAG index updated for: {file_path}"}` on success
- **GOTCHA**: Hook must be fast — run indexing in background with `&` and redirect output to `.rag/reindex.log`
- **GOTCHA**: Only trigger for file paths matching configured source patterns, not ALL file edits
- **GOTCHA**: SQLite WAL mode (configured in store.py) allows the MCP server to read while the hook writes — no "database is locked" errors
- **VALIDATE**: Edit a doc file, verify hook triggers and prints the description

### Task 17: CREATE `rag/README.md`

- **ACTION**: Create comprehensive documentation for standalone adoption
- **IMPLEMENT** (sections):
  1. **Quick Start** (5 minutes): Add submodule → `rag init` → edit config → `rag index` → done
  2. **Architecture Overview**: Dual-collection diagram, component relationships, data flow
  3. **Configuration Reference**: Every `rag.config.yaml` field explained with defaults
  4. **CLI Commands**: `rag init`, `rag index`, `rag search`, `rag serve` with examples
  5. **MCP Tools**: `search_docs`, `search_code`, `search_all`, `get_doc_context`, `list_documents` with example queries
  6. **Design Decisions**: Why each tech (sqlite-vec, fastembed, tree-sitter-language-pack, FastMCP), why separate collections
  7. **Troubleshooting**: macOS SQLite extension loading, model download, memory usage (~700MB for dual models), Python version requirements
  8. **Reuse Guide**: Step-by-step adoption in a new project
- **VALIDATE**: Read through — a developer unfamiliar with the project should be able to set up RAG in <5 minutes

### Task 18: EXTRACT `rag/` to standalone git repo

- **ACTION**: Initialize `rag/` as its own git repository, then set up as submodule
- **IMPLEMENT**:
  1. `cd rag && git init && git add -A && git commit -m "feat: initial RAG system"`
  2. Create a GitHub repository for the RAG system
  3. Push to remote
  4. In the main project: `git submodule add <repo-url> rag`
  5. Commit the `.gitmodules` file
- **NOTE**: This task is optional during initial development — can develop in-place first and extract later
- **VALIDATE**: `git submodule status` shows the rag submodule

---

## Testing Strategy

### Validation Commands (per task)

Each task includes its own VALIDATE command. After all tasks complete:

### Level 1: IMPORT_CHECK

```bash
cd rag && uv run python -c "
import sqlite_vec
import fastembed
from mcp.server.fastmcp import FastMCP
import yaml
from tree_sitter_language_pack import process
from rag.config import load_config
from rag.chunker import chunk_markdown
from rag.code_chunker import chunk_code
from rag.embedder import Embedder
from rag.store import Store
from rag.search import SearchEngine
from rag.server import mcp
print('All imports OK')
"
```

**EXPECT**: Exit 0, prints "All imports OK"

### Level 2: FULL_INDEX

```bash
uv run --project rag python -m rag index --config rag.config.yaml
```

**EXPECT**: Indexes ~58 docs + ~135 code files, prints summary with chunk counts, completes in <90s

### Level 3: SEARCH_VALIDATION

```bash
# Docs search — should return documentation about hooks
uv run --project rag python -m rag search --collection docs "hook validation criteria"

# Code search — should return hook implementation code
uv run --project rag python -m rag search --collection code "PostToolUse hook pattern"

# Cross-collection — should return both docs and code
uv run --project rag python -m rag search "hook validation"

# Collection separation — docs search must NOT return code chunks
uv run --project rag python -m rag search --collection docs "bash function definition"
```

**EXPECT**: Relevant results with source attribution; collection separation maintained

### Level 4: MCP_SERVER_TEST

```bash
# Start server and test with MCP inspector
uv run --project rag python -m rag serve
# In another terminal: verify tools are listed, execute search_docs
```

**EXPECT**: Server starts in <3s (lazy loading), tools respond in <2s

### Level 5: INCREMENTAL_REINDEX

```bash
# Modify a doc file
echo "<!-- test -->" >> docs/README.md
uv run --project rag python -m rag index --config rag.config.yaml
# Should only re-index the modified file, not all files
git checkout docs/README.md  # Restore
```

**EXPECT**: Incremental re-index completes in <10s, reports only 1 file changed

### Edge Cases Checklist

- [ ] Empty document (0 bytes) — should skip, not crash
- [ ] Document with no headers — should fall back to recursive character split
- [ ] Code file with unsupported language — should fall back to fixed-size splitting
- [ ] Binary file in source directory — should be skipped (detect via null bytes or extension)
- [ ] Very long section (>5000 chars) — should be recursively split
- [ ] Unicode content — should handle UTF-8 correctly throughout pipeline
- [ ] Config with non-existent source path — should warn and skip
- [ ] Database file doesn't exist yet — should create on first run
- [ ] Re-indexing with deleted files — should remove stale entries from database (reconciliation)
- [ ] Concurrent read/write — MCP server reading while hook triggers reindex (WAL mode handles this)
- [ ] Hook fires during active reindex — dirty flag ensures no updates are lost
- [ ] Vec0 table has orphaned rows after partial failure — `rebuild_fts()` + manual vec cleanup available
- [ ] tree-sitter parser not downloaded yet — should download on first use or fail gracefully

---

## Acceptance Criteria

- [ ] All 17 implementation tasks completed (Task 18 is optional)
- [ ] Level 1-4 validation commands pass
- [ ] `search_docs` never returns code chunks; `search_code` never returns doc chunks
- [ ] Retrieval precision ≥80% on 20 representative doc queries (manual spot-check)
- [ ] Code retrieval precision ≥75% on 10 representative queries (manual spot-check)
- [ ] Full index completes in <90s
- [ ] Incremental re-index <10s after modifying 1 file
- [ ] MCP server starts in <3s, queries respond in <2s
- [ ] Database size <100MB
- [ ] `rag init` generates valid config template for new projects
- [ ] README enables standalone adoption in <5 minutes

---

## Completion Checklist

- [ ] All tasks completed in dependency order
- [ ] Each task validated immediately after completion
- [ ] Level 1: All imports succeed
- [ ] Level 2: Full index completes successfully
- [ ] Level 3: Search returns relevant results with collection separation
- [ ] Level 4: MCP server starts and responds to tool calls
- [ ] Level 5: Incremental re-index works correctly
- [ ] .gitignore updated for `.rag/`
- [ ] `.mcp.json` created and Claude Code auto-connects
- [ ] README covers setup, usage, architecture, troubleshooting
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| fastembed model download fails (network) | LOW | HIGH | Document in README; models are cached after first download; `cache_dir` is configurable |
| sqlite-vec extension loading fails on macOS | LOW | HIGH | Document: use Homebrew Python or `pysqlite3-binary`; test on macOS if available |
| tree-sitter-language-pack `process()` API changes | MEDIUM | MEDIUM | Pin version `>=1.5,<2.0` in pyproject.toml; the API is new but kreuzberg-dev is active |
| Dual model memory usage (~700MB) | LOW | LOW | Lazy loading — only the queried collection's model loads. Document memory requirements |
| FTS5 external content triggers miss edge cases | MEDIUM | MEDIUM | Call `rebuild_fts()` after bulk operations as safety net; test with incremental updates |
| Python 3.14 compatibility issues | LOW | MEDIUM | sqlite-vec uses `py3-none` wheels (safe); fastembed uses ONNX Runtime (test); tree-sitter-language-pack has abi3 wheels (safe) |
| Chunk quality varies by document structure | MEDIUM | MEDIUM | Markdown chunker handles tables/code blocks atomically; recursive fallback for long sections |
| MCP server startup latency | MEDIUM | LOW | Lazy-load models on first query, not on server start; SearchEngine initialized on first tool call |
| jina-code model quality for non-Python code | LOW | MEDIUM | Jina-code supports 30+ languages including bash, YAML, markdown; test with project's actual file types |
| Config schema changes break existing deployments | LOW | MEDIUM | Version the config schema; provide migration guidance in README |
| Concurrent read/write (hook reindex + MCP query) | MEDIUM | HIGH | WAL journal mode + busy_timeout in Store init; SQLite WAL allows concurrent reads during writes |
| Orphaned vec/FTS entries after partial failures | MEDIUM | MEDIUM | Wrap chunk delete+insert in transaction; `rebuild_fts()` available as repair command |
| tree-sitter parser auto-download stalls offline | LOW | MEDIUM | Consider pre-downloading configured languages during `rag init`; document offline requirements |

---

## Notes

### Corrections from Rubber-Duck Critique

The following issues were identified via independent review and addressed in this plan:

1. **FTS5 schema mismatch (BLOCKING)**: PRD's chunk tables didn't include `file_path`, but FTS5 external content requires all indexed columns to exist in the content source. Fix: denormalized `file_path` into `doc_chunks` and `code_chunks`.

2. **vec0 table cleanup on delete (BLOCKING)**: vec0 virtual tables don't support trigger-based deletion. Fix: `delete_document_chunks()` now explicitly deletes from `vec_docs`/`vec_code` by chunk_id.

3. **Deleted-file reconciliation (BLOCKING)**: No mechanism to remove stale entries when source files are deleted. Fix: added `delete_stale_documents()` to Store and reconciliation step in Indexer.

4. **Task ordering (BLOCKING)**: Tasks 8/10 validation needed `rag.config.yaml` before it was created. Fix: moved config creation to Task 8, before index.py and server.py.

5. **`rebuild_fts()` on every run (HIGH)**: Defeats incremental indexing performance. Fix: create FTS triggers before inserts; only call `rebuild_fts()` on first-ever index or as repair.

6. **`query_embed()` vs `embed()` (HIGH)**: fastembed models with asymmetric encoding (like bge) produce better retrieval with dedicated query encoding. Fix: `embed_query()` now uses `model.query_embed()`.

7. **SQLite concurrency (MEDIUM)**: Hook-triggered reindex while MCP reads the DB causes "database is locked". Fix: added WAL journal mode + busy_timeout to Store init.

8. **Hook debounce (MEDIUM)**: Simple lock-based skip can lose updates. Fix: dirty-flag pattern with trap for lock cleanup.

### Key Design Decision: tree-sitter-language-pack `process()` API

Web research revealed that `tree-sitter-language-pack` (by kreuzberg-dev) includes a built-in `process()` function with a 3-pass syntax-aware chunking algorithm. This **replaces the need for custom AST traversal** that the PRD originally envisioned. The `process()` API handles:
- Collecting leaf syntax units (functions, classes, blocks)
- Bin-packing units into chunks within size limits
- Splitting oversized units with line-boundary alignment
- Auto language detection from file path
- Structure extraction (node types, docstrings)

This significantly simplifies Phase 3 (Code Chunker) — `code_chunker.py` becomes a thin wrapper around `process()` rather than a custom tree-sitter walker.

### FTS5 External Content Mode

The PRD uses `content=''` (contentless FTS5) but this prevents DELETE operations on the index. For incremental updates, we need `content='doc_chunks'` (external content mode) with INSERT/DELETE/UPDATE triggers. This is a correction from the PRD — the plan uses external content with triggers for both `docs_fts` and `code_fts`.

### Module Dependency Graph

```
config.py ──────────┐
chunker.py ─────────┤
code_chunker.py ────┤──→ index.py ──→ cli.py
embedder.py ────────┤                    ↑
store.py ───────────┤──→ search.py ──→ server.py
```

Phases 2-5 (chunker, code_chunker, embedder, store) have no mutual dependencies and can be implemented in any order after config.py. index.py integrates all four. search.py uses store + embedder. server.py wraps search. cli.py ties everything together.

### Task 18 Guidance

Extracting `rag/` to a standalone git repo (Task 18) should be done AFTER all functionality is working and tested. During development, keep `rag/` as a regular directory. The extraction involves:
1. Creating a new GitHub repository
2. Moving the git history (or starting fresh)
3. Converting to a submodule in the consuming project

This is a distribution concern, not a functionality concern. It can be deferred until the system is stable.
