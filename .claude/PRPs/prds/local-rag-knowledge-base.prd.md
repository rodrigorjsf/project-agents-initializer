# Local RAG Knowledge Base

## Problem Statement

AI agents (Claude Code, GitHub Copilot) working on projects with substantial documentation and implementation code must repeatedly read large files to find relevant context for each task. This wastes context window tokens, increases response latency, and forces agents to either load too much irrelevant content or miss critical information buried in files they didn't read. There is no mechanism today to semantically search documentation or navigate code by concept — agents rely on keyword-based `grep`/`glob` or must read entire files.

In this project specifically, there are ~58 markdown files (~1.3MB, ~26K lines) of documentation plus skill definitions, plugin code, and shell scripts — a problem that will only grow as content is added and that repeats in every project with meaningful documentation and codebase.

## Evidence

- The project's own DESIGN-GUIDELINES.md documents the "200-line attention budget" — agents lose instruction adherence beyond ~150-200 lines of context. Loading full docs easily exceeds this.
- The ETH Zurich "Evaluating AGENTS.md" study (Feb 2026) showed LLM-generated comprehensive context files **hurt** performance by -3%, confirming that more context ≠ better results.
- Liu et al., "Lost in the Middle" (TACL 2023) demonstrated models retrieve information poorly from the middle of long contexts — exactly what happens when agents load multiple large docs.
- The project already uses a progressive disclosure pattern (root → scope → on-demand) to minimize always-loaded context, but documentation retrieval remains brute-force.
- The `docs/README.md` "Reading Order by Task" section is a manual workaround for the lack of semantic search — agents must follow prescribed reading paths instead of querying for what they need.

## Proposed Solution

Build a **reusable, configuration-driven**, fully local, serverless RAG (Retrieval-Augmented Generation) system that:

1. **Indexes** project documentation and source code into a SQLite database using sqlite-vec for vector search and FTS5 for full-text search, **with separate collections** (vec0 tables) for docs vs code to keep contexts clean and enable per-type embedding models
2. **Generates embeddings** locally using fastembed (ONNX Runtime) — no API keys, no network dependency. Uses general-purpose models for documentation and code-specific models for source code
3. **Exposes** the knowledge base via an MCP (Model Context Protocol) server with **type-aware tools** (`search_docs`, `search_code`, `search_all`) so AI agents can explicitly choose their search scope
4. **Auto-updates** incrementally when files change, using file hash-based change detection
5. **Uses hybrid search** (vector similarity + BM25 keyword matching via RRF) to maximize retrieval quality — independently per collection
6. **Is portable** — designed to be dropped into any project via configuration, not hardcoded to a specific codebase
7. **Parses code with tree-sitter** — AST-based chunking respects language syntax boundaries (functions, classes, blocks) instead of naive text splitting

The system's first deployment target is this project (`agent-engineering-toolkit`), but every design decision prioritizes reusability: configurable paths, swappable embedding models, project-agnostic schema, comprehensive documentation, and a single config file to customize for each project.

This approach was chosen over alternatives because:
- **vs. cloud-based RAG** (Pinecone, Weaviate): Requires API keys, network dependency, and ongoing cost. Violates the self-contained, portable philosophy.
- **vs. ChromaDB/LanceDB**: Adds heavy Python dependencies. sqlite-vec is a single C extension with zero dependencies, matching a minimalist approach.
- **vs. pure FTS5**: Keyword search misses semantic relationships (e.g., "context optimization" wouldn't find docs about "attention budget"). Vector search captures semantic similarity.
- **vs. loading docs into CLAUDE.md**: Violates the 200-line budget and progressive disclosure principles.
- **vs. building a single-use script**: A config-driven tool pays for itself across multiple projects and can be maintained as a shared utility.

## Key Hypothesis

We believe a **local, reusable, config-driven hybrid-search RAG system with separate documentation and code collections, exposed via MCP** will **reduce irrelevant context loading and improve retrieval precision** for **AI agents working on any documentation-heavy project with implementation code**.
We'll know we're right when **agents can find relevant documentation OR implementation code with a single semantic query that returns ≤5 focused chunks instead of loading entire files, with ≥80% relevance precision in manual spot-checks, code retrieval returns correct function/symbol context, and the system can be adopted in a new project by editing a single config file in under 5 minutes**.

## What We're NOT Building

- **A cloud/hosted service** — Everything runs locally, no servers, no API keys, no Docker
- **PDF parsing** — The one PDF (`Evaluating-AGENTS-paper.pdf`) has a corresponding `.md` extraction; PDF support is deferred
- **A web UI or query interface** — The only interface is the MCP server consumed by AI tools
- **Multi-user support** — Single developer, single machine
- **GPU-accelerated embeddings** — ONNX CPU inference is sufficient for typical documentation collections
- **Real-time streaming updates** — Batch re-indexing triggered on-demand or via git hooks is sufficient
- **A pip-installable package (v1)** — Reusability is via git submodule, not `pip install`. Packaging as a distributable package is a future consideration once the tool is battle-tested across 2-3 projects

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Doc retrieval precision (top-5) | ≥80% relevant chunks | Manual spot-check: 20 representative queries against indexed docs |
| Code retrieval precision (top-5) | ≥75% relevant chunks | Manual spot-check: 10 queries for functions/patterns against indexed code |
| Indexing time (full rebuild, both collections) | <90 seconds | Timed `rag index` command on full docs + code |
| Incremental update time | <10 seconds | Timed `rag index` after modifying 1-3 files |
| Query latency (MCP tool call) | <2 seconds | Timed round-trip from MCP tool invocation to results returned |
| Database size | <100MB | `ls -la` on the SQLite database file (both collections) |
| Context reduction | ≥70% fewer tokens loaded vs reading full files | Compare: tokens in top-5 chunks vs tokens in source files those chunks came from |
| Zero external dependencies | 0 API keys, 0 network calls at query time | Audit: run with network disabled |
| Collection separation accuracy | 100% correct collection in results | Verify: `search_docs` never returns code chunks, `search_code` never returns doc chunks |
| New project adoption time | <5 minutes to configure and index a new project | Timed: add submodule, `rag init`, edit config, `rag index` |
| Config-only setup | Zero code changes to adopt in a new project | Audit: only `rag.config.yaml` differs between deployments |
| Documentation completeness | All setup, usage, and architecture documented | Peer review: new developer can set up RAG from docs alone, no oral knowledge needed |

## Open Questions (Resolved)

- [x] **MCP `list_documents` resource** → Yes. Expose a `list_documents` MCP resource for browsing the index alongside search tools.
- [x] **Reading order hierarchy in metadata** → Yes. Chunk metadata will include the document's position in the "Reading Order by Task" hierarchy from `docs/README.md`.
- [x] **Embedding model testing** → Yes. Start with `BAAI/bge-small-en-v1.5` (384 dims) as default for docs, but also benchmark `nomic-ai/nomic-embed-text-v1.5` (768 dims) to validate quality. Config-driven model selection makes switching trivial.
- [x] **Re-indexing trigger** → Both. Manual CLI command is always available; additionally, a Claude Code PostToolUse hook triggers incremental re-indexing when docs/code change.
- [x] **Distribution method** → Git submodule. The `rag/` directory will be maintained as its own repository, consumed by projects as a git submodule. Config file (`rag.config.yaml`) stays in the consuming project.
- [x] **Per-source chunking strategies** → Yes. `rag.config.yaml` supports per-collection and per-source chunking strategies, each with its own settings.
- [x] **`rag init` command** → Yes. Include a `rag init` CLI command that scaffolds the config file and directory structure for a new project.
- [x] **Code file indexing** → Yes. Index source code files alongside documentation, but in **separate collections** (separate vec0 tables, separate FTS5 indexes, separate embedding models). Research validated this as best practice: Continue.dev, Qdrant, and Sourcegraph all recommend collection separation for heterogeneous content. sqlite-vec's brute-force KNN makes separate tables the only viable pre-filter mechanism. AI agents choose the collection explicitly via `search_docs` vs `search_code` tools (LLM-as-router pattern).

---

## Users & Context

**Primary User**
- **Who**: AI coding agents (Claude Code, GitHub Copilot) operating within this project
- **Current behavior**: Read entire doc files via `view`/`grep`, often loading 500-2000 lines of documentation to find a 20-line answer. For code, rely on `grep` for exact symbol matches but miss semantic relationships. Or skip docs entirely and hallucinate.
- **Trigger**: Agent receives a task that requires domain knowledge from the project's documentation (e.g., "what are the validation criteria for skills?") or needs to understand implementation patterns (e.g., "how do existing hooks work?")
- **Success state**: Agent queries the RAG system with a natural language question, choosing `search_docs` for conceptual knowledge or `search_code` for implementation examples, and receives 3-5 focused, relevant chunks with source attribution — enough to complete the task without loading full files

**Secondary User**
- **Who**: The project maintainer (developer) who runs indexing and verifies retrieval quality
- **Current behavior**: Manually maintains reading order guides and cross-references between docs
- **Trigger**: Adds or modifies documentation, needs to ensure the knowledge base stays current
- **Success state**: Runs a single CLI command to re-index; changes are reflected in queries immediately

**Tertiary User**
- **Who**: A developer adopting this RAG system in a different project
- **Current behavior**: Has a project with markdown documentation but no semantic search capability. May copy-paste doc content into prompts or rely on grep.
- **Trigger**: Wants to add RAG-powered doc search to their own project without building from scratch
- **Success state**: Adds the `rag/` submodule, runs `rag init`, edits `rag.config.yaml` to define their collections (docs + optionally code), runs `uv sync && python -m rag.index`, and has a working dual-collection RAG system in under 5 minutes

**Job to Be Done**
When an AI agent needs project-specific documentation context, I want to semantically search the knowledge base, so I can load only the most relevant chunks instead of entire files and stay within my attention budget.

**Non-Users**
- End-users of the plugins this project produces (they don't interact with the RAG system)
- Other AI tools without MCP support (until/unless we add a CLI query interface)

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | **SQLite + sqlite-vec vector storage** | Core requirement: portable, serverless, zero-dependency vector database |
| Must | **FTS5 full-text search** | Keyword matching catches exact terms that vector search may miss |
| Must | **Hybrid search with RRF** | Combining vector + keyword yields highest retrieval quality |
| Must | **Local embeddings via fastembed** | ONNX Runtime, no GPU, no API keys — fully offline operation |
| Must | **MCP server (stdio transport)** | Native integration with Claude Code; also works with Cursor and other MCP clients |
| Must | **Markdown-aware chunking** | Respect document structure (headers, sections) for coherent chunks |
| Must | **Separate collections for docs vs code** | Separate vec0 tables (`vec_docs`, `vec_code`) with independent embedding models. sqlite-vec uses brute-force KNN — separate tables ARE the pre-filter. Validated by Continue.dev, Qdrant multitenancy docs |
| Must | **Code-aware chunking via tree-sitter** | AST-based parsing respects syntax boundaries (functions, classes, blocks). Regex splitting breaks semantic units. tree-sitter is the industry standard (LlamaIndex, Sweep AI, Continue.dev) |
| Must | **Code-specific embedding model** | `jinaai/jina-embeddings-v2-base-code` (768d, 8192 context, fastembed-supported) for code. Code-specific models outperform general-purpose by ~14% on code retrieval (Voyage AI benchmarks) |
| Must | **Type-aware MCP search tools** | Separate `search_docs`, `search_code`, `search_all` tools. The LLM IS the router — explicit tools give agents control over search scope (Continue.dev pattern) |
| Must | **Source attribution in results** | Every chunk must include file path, section header, and line range |
| Must | **Incremental re-indexing** | Only re-embed documents that changed (SHA-256 hash comparison) |
| Must | **CLI for indexing** | `python -m rag_index` or similar for manual index builds |
| Must | **Project-level configuration file** | `rag.config.yaml` drives all project-specific settings (paths, model, chunk size, file patterns) — zero code changes to adopt in a new project |
| Must | **Per-source chunking strategies** | Each source directory in config can specify its own chunking strategy, patterns, and settings |
| Must | **Comprehensive documentation** | README with setup guide, architecture overview, configuration reference, usage examples, and troubleshooting. A new developer must be able to set up RAG from docs alone |
| Must | **`list_documents` MCP resource** | Expose a browseable index of all indexed documents alongside search tools |
| Must | **Reading order hierarchy metadata** | Chunk metadata includes the document's position in the `docs/README.md` reading order hierarchy |
| Must | **`rag init` CLI command** | Scaffolds `rag.config.yaml` and directory structure for a new project |
| Must | **Auto-reindex via Claude Code hook** | PostToolUse hook triggers incremental re-indexing when docs change (alongside manual CLI) |
| Must | **Dual embedding model benchmarking** | Benchmark both `bge-small-en-v1.5` (384d) and `nomic-embed-text-v1.5` (768d); config makes switching trivial |
| Should | **Cross-encoder reranking** | fastembed includes `TextCrossEncoder` — rerank top-N results for precision |
| Should | **Document metadata enrichment** | Store document category, scope, and hierarchy level from docs/README.md |
| Should | **Query expansion** | Expand queries with related terms for better recall |
| Could | **Index health reporting** | CLI command to show index stats: doc count, chunk count, staleness |
| Won't | **PDF parsing** | Deferred — the one PDF has a markdown counterpart already |
| Won't | **Web UI** | AI agents are the primary consumers; no human query interface needed |

### MVP Scope

The minimum to validate the hypothesis:

1. A Python package (`rag/`) that chunks both documentation (markdown header-based) and code files (tree-sitter AST-based), generates embeddings with fastembed, and stores them in **separate** SQLite vec0 tables (`vec_docs` + `vec_code`) with independent FTS5 indexes
2. An MCP server with `search_docs`, `search_code`, `search_all` tools, `get_doc_context` tool, and `list_documents` resource — hybrid search returns top-5 results with source attribution
3. MCP server configuration for Claude Code (`.mcp.json`)
4. CLI commands: `rag index` (rebuild), `rag init` (scaffold config for new project)
5. `rag.config.yaml` with per-source chunking strategy support and per-collection embedding model config
6. Reading order hierarchy metadata from `docs/README.md` stored in chunk metadata

**Not in MVP**: Reranking, query expansion, auto-reindex hook (Phase 8), Copilot-specific integration.

### User Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Developer runs: python -m rag.index                        │
│  → Scans configured sources for docs (.md) and code files   │
│  → Docs: chunks by markdown sections (h1/h2/h3 boundaries)  │
│  → Code: chunks by AST nodes via tree-sitter (functions,    │
│          classes, blocks) with syntax-aware boundaries       │
│  → Generates embeddings:                                     │
│    • Docs → bge-small-en-v1.5 (384d, general-purpose)       │
│    • Code → jina-embeddings-v2-base-code (768d, code-aware) │
│  → Stores in SEPARATE vec0 tables in .rag/knowledge.db:     │
│    • vec_docs + docs_fts  (documentation collection)         │
│    • vec_code + code_fts  (code collection)                  │
│  → Reports: "Indexed 58 docs (342 chunks) + 12 code files   │
│              (87 chunks), 52s"                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Claude Code starts → loads MCP server from config           │
│  → MCP server connects to .rag/knowledge.db                  │
│  → Exposes tools:                                            │
│    • search_docs(query, top_k)  → docs collection only       │
│    • search_code(query, top_k)  → code collection only       │
│    • search_all(query, top_k)   → both, merged by score      │
│  → Exposes resource: list_documents (browseable index)       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Agent receives task: "add validation for hook templates"    │
│  → Agent calls: search_docs("hook validation criteria")      │
│    (chooses docs because it needs design guidelines)         │
│  → MCP server performs on vec_docs:                          │
│    1. Embed query with bge-small-en (docs model)             │
│    2. Vector KNN search via sqlite-vec (top-20)              │
│    3. FTS5 keyword search (top-20)                           │
│    4. Merge via Reciprocal Rank Fusion                       │
│    5. Return top-5 chunks with metadata                      │
│  → Agent also calls: search_code("hook template validation") │
│    (to see how existing hooks implement validation)          │
│  → MCP server performs on vec_code:                          │
│    1. Embed query with jina-code (code model)                │
│    2. Vector KNN + FTS5 + RRF (same pipeline)                │
│    3. Return top-5 code chunks with file/function/line info  │
│  → Agent has both docs context AND implementation examples   │
│  → Agent completes task with minimal context usage            │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Approach

**Feasibility**: HIGH

All components are mature, well-documented, and have Python bindings. The document collection is small (~1.3MB) — well within the capacity of local CPU-based processing.

**Architecture Notes**

```
project-root/
├── rag/                        # RAG system (git submodule — its own repo for reuse)
│   ├── __init__.py
│   ├── index.py                # Indexing pipeline (chunk, embed, store)
│   ├── chunker.py              # Markdown-aware document chunker (header-based)
│   ├── code_chunker.py         # AST-based code chunker (tree-sitter)
│   ├── embedder.py             # fastembed wrapper (supports multiple models per collection)
│   ├── store.py                # SQLite + sqlite-vec + FTS5 storage (separate collections)
│   ├── search.py               # Hybrid search (vector + FTS5 + RRF) per collection
│   ├── server.py               # MCP server (search_docs, search_code, search_all)
│   ├── config.py               # Configuration loader (reads rag.config.yaml)
│   ├── cli.py                  # CLI entry point (index, init, health)
│   ├── pyproject.toml          # Python dependencies (uv/pip)
│   └── README.md               # Full documentation: setup, usage, architecture, config reference
├── rag.config.yaml             # Project-specific configuration (the ONLY file to edit when reusing)
├── .rag/                       # Data directory (gitignored)
│   ├── knowledge.db            # SQLite database (vec_docs + vec_code + FTS5 tables)
│   └── models/                 # Cached fastembed model files (both doc + code models)
└── .mcp.json                   # MCP server config for Claude Code
```

**Configuration File (`rag.config.yaml`)**

```yaml
# Project-specific RAG configuration
# This is the ONLY file you need to edit when adopting RAG in a new project.

project:
  name: "agent-engineering-toolkit"  # Used in MCP server name and logging

# Collections define separate search contexts with independent embedding models,
# chunking strategies, and vec0 tables. AI agents choose which collection to search.
# Research: separate collections outperform mixed+filtered (Continue.dev, Qdrant docs).
# sqlite-vec uses brute-force KNN — separate tables ARE the pre-filter.

collections:
  docs:                                # Documentation collection
    description: "Project documentation, guides, research, and design decisions"
    embedding:
      model: "BAAI/bge-small-en-v1.5"   # General-purpose, 384d, 67MB, 512 token window
      dimensions: 384
    sources:
      - path: "docs/"
        patterns: ["*.md"]
        recursive: true
    chunking:
      strategy: "markdown_header"       # Split on markdown headers
      max_tokens: 512
      overlap_tokens: 256
      split_headers: ["h1", "h2", "h3"]

  code:                                # Code/implementation collection
    description: "Source code, skill definitions, templates, scripts, and config files"
    embedding:
      model: "jinaai/jina-embeddings-v2-base-code"  # Code-specific, 768d, 640MB, 8192 token window
      dimensions: 768
    sources:
      - path: "plugins/"
        patterns: ["*.md", "*.sh", "*.yaml", "*.yml"]
        recursive: true
        chunking:                      # Per-source override
          strategy: "markdown_header"  # SKILL.md, references, templates are markdown
          max_tokens: 512
      - path: "skills/"
        patterns: ["*.md"]
        recursive: true
      - path: ".claude/hooks/"
        patterns: ["*.sh"]
        recursive: false
        chunking:
          strategy: "tree_sitter"      # AST-based for shell scripts
          language: "bash"
          max_chars: 1500
    chunking:                          # Default for this collection
      strategy: "tree_sitter"          # tree_sitter | markdown_header | recursive | fixed
      max_chars: 1500                  # ~300 tokens, optimal for code (Sweep AI research)
      languages:                       # Auto-detect from extension, or explicit mapping
        ".py": "python"
        ".sh": "bash"
        ".js": "javascript"
        ".ts": "typescript"
        ".yaml": "yaml"
        ".yml": "yaml"

shared:
  cache_dir: ".rag/models"             # Model cache location (shared across collections)

database:
  path: ".rag/knowledge.db"            # Single SQLite file, separate vec0 tables per collection

search:
  default_top_k: 5                     # Default number of results
  max_top_k: 10                        # Maximum allowed results
  rrf_k: 60                            # RRF constant
  vector_candidates: 20                # Candidates for vector search per collection
  fts_candidates: 20                   # Candidates for FTS5 search per collection

server:
  name: "rag-docs"                     # MCP server display name
  transport: "stdio"                   # stdio | sse
```

**Key Technical Decisions**

| Decision | Choice | Why |
|----------|--------|-----|
| Language | Python 3.11+ | Best embedding ecosystem (fastembed, ONNX), sqlite-vec first-class support |
| Package manager | uv | Fast, modern, single-binary — no system-wide pip pollution |
| Vector DB | sqlite-vec (vec0 virtual tables) | Pure C, zero deps, stores alongside FTS5 in same SQLite file |
| Full-text search | SQLite FTS5 | Built-in, BM25 scoring, same database file |
| Collection architecture | Separate vec0 tables per content type | sqlite-vec brute-force KNN has no pre-filter — separate tables ARE the filter; different dimensions require separate tables; AI agents choose collection explicitly via tool name |
| Doc embedding model | BAAI/bge-small-en-v1.5 (384d) | Top MTEB performer at 67MB, 512 token window, fast ONNX inference |
| Code embedding model | jinaai/jina-embeddings-v2-base-code (768d) | Only code-specific model in fastembed; trained on 30+ languages + English; 8192 token context; outperforms general models by ~14% on code retrieval |
| Embedding library | fastembed | ONNX Runtime, no PyTorch, ~90MB install, supports multiple models |
| Doc chunking | Markdown header-based + recursive split | Respect section boundaries, fallback to character split for long sections |
| Code chunking | tree-sitter AST-based | Industry standard (LlamaIndex, Sweep AI, Continue.dev); preserves semantic boundaries (functions, classes, blocks); `tree-sitter-language-pack` for 305+ languages |
| Chunk size (docs) | 512 tokens, 256 token overlap | Matches bge-small model's 512 token window; overlap preserves context at boundaries |
| Chunk size (code) | ~1500 chars (~300 tokens) | Optimal precision per Sweep AI research; maps to ~40 lines of code |
| MCP transport | stdio | Standard for local tools; supported by Claude Code, Cursor, and others |
| MCP framework | FastMCP (Python) | Official Python SDK, simple decorator-based tool definition |
| MCP tool routing | LLM-as-router (separate tools) | Expose `search_docs`, `search_code`, `search_all` — the LLM selects the right tool based on task context; no custom query router needed (validated by Continue.dev pattern) |
| Search fusion | Reciprocal Rank Fusion (RRF) | Simple, parameter-free, proven effective for combining ranked lists |
| Change detection | SHA-256 file hash stored per document | Compare hash on re-index; only re-embed changed/new documents |

**Database Schema**

```sql
-- ======= SHARED =======

-- All indexed source files (docs + code)
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    file_path TEXT UNIQUE NOT NULL,
    collection TEXT NOT NULL,       -- 'docs' or 'code'
    title TEXT,
    category TEXT,                  -- docs: claude-code, cursor, etc. | code: plugins, skills, hooks
    file_hash TEXT NOT NULL,        -- SHA-256 for change detection
    chunk_count INTEGER,
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======= DOCS COLLECTION (documentation) =======

-- Document chunks metadata
CREATE TABLE doc_chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    chunk_index INTEGER NOT NULL,
    section_header TEXT,
    content TEXT NOT NULL,
    start_line INTEGER,
    end_line INTEGER,
    token_count INTEGER,
    reading_order INTEGER           -- Position from docs/README.md task hierarchy
);

-- Document chunk embeddings (384d — BAAI/bge-small-en-v1.5)
CREATE VIRTUAL TABLE vec_docs USING vec0(
    embedding float[384],
    +chunk_id INTEGER               -- References doc_chunks(id)
);

-- Document full-text search index
CREATE VIRTUAL TABLE docs_fts USING fts5(
    content,
    section_header,
    file_path,
    content=''                      -- External content mode
);

-- ======= CODE COLLECTION (source code + config) =======

-- Code chunks metadata
CREATE TABLE code_chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id),
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    language TEXT,                   -- 'python', 'bash', 'markdown', 'yaml', etc.
    symbol_type TEXT,                -- 'function', 'class', 'method', 'block', 'section', NULL
    symbol_name TEXT,                -- e.g., 'hybrid_search', 'SearchResult', NULL
    parent_symbol TEXT,              -- Enclosing symbol name for nested definitions
    start_line INTEGER,
    end_line INTEGER,
    char_count INTEGER
);

-- Code chunk embeddings (768d — jinaai/jina-embeddings-v2-base-code)
CREATE VIRTUAL TABLE vec_code USING vec0(
    embedding float[768],
    +chunk_id INTEGER               -- References code_chunks(id)
);

-- Code full-text search index
CREATE VIRTUAL TABLE code_fts USING fts5(
    content,
    symbol_name,
    file_path,
    language,
    content=''                      -- External content mode
);
```

**Hybrid Search Query (RRF) — Per Collection**

```python
def search_collection(
    query: str, collection: str, top_k: int = 5
) -> list[SearchResult]:
    """Search a specific collection (docs or code) with hybrid retrieval."""
    # Select the right model, tables, and metadata based on collection
    config = COLLECTIONS[collection]  # docs | code
    embedder = config.embedder        # bge-small for docs, jina-code for code
    vec_table = config.vec_table      # vec_docs | vec_code
    fts_table = config.fts_table      # docs_fts | code_fts
    chunks_table = config.chunks_table  # doc_chunks | code_chunks

    query_embedding = embedder.embed(query)

    # 1. Vector search (top-20 candidates from this collection's vec0 table)
    vec_results = db.execute(f"""
        SELECT chunk_id, distance
        FROM {vec_table}
        WHERE embedding MATCH ?
        ORDER BY distance
        LIMIT 20
    """, [serialize_float32(query_embedding)])

    # 2. FTS5 keyword search (top-20 candidates from this collection's FTS index)
    fts_results = db.execute(f"""
        SELECT rowid, rank
        FROM {fts_table}
        WHERE {fts_table} MATCH ?
        ORDER BY rank
        LIMIT 20
    """, [fts5_query(query)])

    # 3. Reciprocal Rank Fusion (k=60)
    rrf_scores = {}
    for rank, (rowid, _) in enumerate(vec_results):
        rrf_scores[rowid] = rrf_scores.get(rowid, 0) + 1 / (60 + rank + 1)
    for rank, (rowid, _) in enumerate(fts_results):
        rrf_scores[rowid] = rrf_scores.get(rowid, 0) + 1 / (60 + rank + 1)

    # 4. Return top-k with full metadata from the collection's chunk table
    top_ids = sorted(rrf_scores, key=rrf_scores.get, reverse=True)[:top_k]
    return [build_result(id, chunks_table) for id in top_ids]


def search_all(query: str, top_k: int = 5) -> list[SearchResult]:
    """Search both collections and merge results by normalized RRF score."""
    docs_results = search_collection(query, "docs", top_k=top_k * 2)
    code_results = search_collection(query, "code", top_k=top_k * 2)

    # Normalize scores across collections (0-1 range) for fair merging
    all_results = normalize_scores(docs_results + code_results)
    all_results.sort(key=lambda r: r.score, reverse=True)
    return all_results[:top_k]
```

**MCP Server Tool Definition**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rag-knowledge-base")

@mcp.tool()
async def search_docs(query: str, top_k: int = 5) -> str:
    """Search project DOCUMENTATION (guides, research, design decisions, analysis).
    Use this when the agent needs conceptual knowledge, design rationale, guidelines,
    or research findings. Returns markdown documentation chunks.

    Args:
        query: Natural language search query about project documentation
        top_k: Number of results to return (default: 5, max: 10)
    """
    results = search_collection(query, "docs", min(top_k, 10))
    return format_results(results, collection="docs")

@mcp.tool()
async def search_code(query: str, top_k: int = 5) -> str:
    """Search project SOURCE CODE (skills, plugins, scripts, templates, config files).
    Use this when the agent needs implementation examples, existing patterns, function
    signatures, or configuration references. Returns code chunks with file/symbol context.

    Args:
        query: Search query about code implementation, functions, or patterns
        top_k: Number of results to return (default: 5, max: 10)
    """
    results = search_collection(query, "code", min(top_k, 10))
    return format_results(results, collection="code")

@mcp.tool()
async def search_all(query: str, top_k: int = 5) -> str:
    """Search BOTH documentation AND source code simultaneously.
    Use this when the agent needs a holistic view — e.g., understanding how a concept
    from the docs is actually implemented. Results include a 'collection' field
    ('docs' or 'code') so the agent knows what type each result is.

    Args:
        query: Broad search query spanning docs and code
        top_k: Number of combined results to return (default: 5, max: 10)
    """
    results = search_all_collections(query, min(top_k, 10))
    return format_results(results, collection="all")

@mcp.tool()
async def get_doc_context(file_path: str) -> str:
    """Get all indexed chunks from a specific file (documentation or code).

    Args:
        file_path: Relative path to the file (e.g., 'docs/general-llm/a-guide-to-agents.md')
    """
    chunks = get_chunks_by_file(file_path)
    return format_chunks(chunks)

@mcp.resource("docs://index")
async def list_documents() -> str:
    """Browse all indexed documents organized by collection (docs vs code),
    with metadata: path, category, chunk count, reading order position."""
    docs = get_all_documents()
    return format_document_list(docs)
```

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Embedding model too large for fast startup | Low | bge-small is 67MB; jina-code is 640MB — lazy-load each model on first query to that collection |
| sqlite-vec breaking changes (pre-v1) | Medium | Pin version in pyproject.toml; vec0 API is stable enough for our use case |
| MCP server startup latency (model loading) | Medium | Lazy-load embedding models on first query per collection, not on server start |
| Chunk quality varies by document structure | Medium | Markdown-aware chunker with fallback to recursive character split |
| MacOS SQLite extension loading blocked | Low | Use Homebrew Python or pysqlite3 as documented in sqlite-vec docs |
| fastembed model download on first run | Low | Document in README; models are cached after first download (~700MB total) |
| tree-sitter language pack compatibility | Medium | Pin `tree-sitter-language-pack` version; test against project's file types (markdown, bash, yaml) specifically |
| Dual-model memory usage | Low | Each model loads independently (~700MB combined when both loaded); acceptable for dev machines |
| jina-code model not in fastembed | Low | Already verified: `jinaai/jina-embeddings-v2-base-code` is in fastembed's supported model list |

---

## Implementation Phases

<!--
  STATUS: pending | in-progress | complete
  PARALLEL: phases that can run concurrently (e.g., "with 3" or "-")
  DEPENDS: phases that must complete first (e.g., "1, 2" or "-")
  PRP: link to generated plan file once created
-->

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Python project setup | Initialize `rag/` package with uv, pyproject.toml, dependencies (incl. tree-sitter) | in-progress | - | - | [plan](../plans/local-rag-knowledge-base.plan.md) |
| 2 | Document chunker | Markdown-aware chunking with header boundary detection | pending | - | 1 | - |
| 3 | Code chunker | tree-sitter AST-based code chunking with symbol extraction | pending | with 2 | 1 | - |
| 4 | Embedding pipeline | fastembed integration with multi-model support (bge-small + jina-code) | pending | with 2 | 1 | - |
| 5 | SQLite storage layer | sqlite-vec + FTS5 schema with separate collections (vec_docs + vec_code) | pending | with 2 | 1 | - |
| 6 | Indexing pipeline | Full pipeline: scan → route → chunk → embed → store with per-collection logic | pending | - | 2, 3, 4, 5 | - |
| 7 | Hybrid search engine | Per-collection search + cross-collection merge via normalized RRF | pending | - | 5, 6 | - |
| 8 | MCP server | FastMCP server with search_docs, search_code, search_all, get_doc_context, list_documents | pending | - | 7 | - |
| 9 | Integration & config | MCP config, .gitignore, rag.config.yaml, CLI entry points, PostToolUse hook | pending | - | 8 | - |
| 10 | Documentation & portability | README, architecture docs, config reference, setup guide, reuse instructions | pending | - | 9 | - |

### Phase Details

**Phase 1: Python Project Setup**
- **Goal**: Establish the Python package structure as a standalone git repository
- **Scope**: Create `rag/` package as its own git repo (will be consumed as submodule), `pyproject.toml` with uv, install sqlite-vec + fastembed + mcp SDK + pyyaml + tree-sitter + tree-sitter-language-pack. Add `.rag/` and model cache to `.gitignore`. Create `cli.py` with `rag init` scaffolding command
- **Success signal**: `uv run python -c "import sqlite_vec; import fastembed; from mcp.server.fastmcp import FastMCP; import yaml; import tree_sitter; import tree_sitter_language_pack"` succeeds; `python -m rag init` generates a `rag.config.yaml` template with both docs and code collection stubs

**Phase 2: Document Chunker**
- **Goal**: Parse markdown files into semantically coherent chunks
- **Scope**: Implement `chunker.py` — split by H1/H2/H3 headers (configurable per source), handle tables and code blocks atomically, recursive character split for sections exceeding max_tokens, preserve metadata (file path, section header, line numbers, reading order position from docs hierarchy)
- **Success signal**: Chunking `docs/` produces chunks where each chunk is 100-512 tokens, section headers are preserved, and tables/code blocks are not split mid-content

**Phase 3: Code Chunker**
- **Goal**: Parse source code files into semantically coherent chunks using AST analysis
- **Scope**: Implement `code_chunker.py` — use tree-sitter to parse files into AST nodes, extract functions/classes/methods/blocks as chunks, preserve metadata (language, symbol_type, symbol_name, parent_symbol, file path, line range). Language-to-parser mapping from config. Handle mixed files (markdown with embedded code in SKILL.md) via content-type detection. Fallback to line-based splitting for unsupported languages
- **Success signal**: Chunking `.claude/hooks/*.sh` produces chunks aligned to function/block boundaries with correct symbol names. Chunking SKILL.md files produces header-based sections (not tree-sitter). Each chunk is ≤1500 chars with symbol metadata populated

**Phase 4: Embedding Pipeline**
- **Goal**: Generate vector embeddings locally with multi-model support for different collections
- **Scope**: Implement `embedder.py` — wrapper around fastembed's `TextEmbedding` supporting multiple model instances, config-driven model selection per collection (docs → `BAAI/bge-small-en-v1.5` 384d, code → `jinaai/jina-embeddings-v2-base-code` 768d), lazy model loading per collection, batch embedding support, model caching in configurable directory. Include benchmarking utility to compare bge-small vs nomic-embed-text for docs collection
- **Success signal**: Can embed 500 doc chunks with bge-small AND 200 code chunks with jina-code independently; models auto-download on first use per collection; switching models via config works without code changes

**Phase 5: SQLite Storage Layer**
- **Goal**: Create and manage the SQLite database with separate collections for docs and code
- **Scope**: Implement `store.py` — database creation, schema migration, sqlite-vec extension loading. Create separate tables per collection: `vec_docs` (384d) + `doc_chunks` + `docs_fts` for documentation, `vec_code` (768d) + `code_chunks` + `code_fts` for code. Shared `documents` table with `collection` discriminator. CRUD operations per collection, collection-aware insert and query methods
- **Success signal**: Can insert 500 doc chunks (384d) and 200 code chunks (768d) into their respective tables; vector KNN and FTS5 search work independently per collection; cross-collection document listing works; database file size is reasonable (<100MB for full dual-collection index)

**Phase 6: Indexing Pipeline**
- **Goal**: End-to-end pipeline from source files to indexed database with per-collection routing
- **Scope**: Implement `index.py` — scan configured sources from `rag.config.yaml`, route files to correct collection based on config, apply per-collection chunking (markdown chunker for docs, code chunker for code sources), embed with the collection's model, store in the collection's tables. SHA-256 hashes for incremental updates. CLI entry point (`python -m rag.index`). Support indexing a single collection (`--collection docs`) or all
- **Success signal**: Full index of docs + code completes in <90s; incremental re-index after modifying 1 file completes in <10s; re-running without changes is a no-op; `--collection` flag indexes only the specified collection

**Phase 7: Hybrid Search Engine**
- **Goal**: High-quality per-collection retrieval with cross-collection merge capability
- **Scope**: Implement `search.py` — `search_collection(query, collection, top_k)` performs vector KNN + FTS5 + RRF against a specific collection's tables using its embedding model. `search_all(query, top_k)` queries both collections independently, normalizes scores to 0-1 range, merges, returns top-k. Result formatting with source attribution (file path, section/symbol, line range, relevance score, collection label)
- **Success signal**: `search_collection("hook validation", "docs")` returns documentation about hooks. `search_collection("hook validation", "code")` returns hook implementation code. `search_all("hook validation")` returns both, interleaved by score, with clear collection labels

**Phase 8: MCP Server**
- **Goal**: Expose the dual-collection knowledge base to AI agents via MCP protocol
- **Scope**: Implement `server.py` — FastMCP server with: `search_docs` tool (docs collection), `search_code` tool (code collection), `search_all` tool (merged cross-collection), `get_doc_context` tool (full file chunks from any collection), `list_documents` resource (browseable index organized by collection). Tool descriptions must clearly guide the LLM on when to use each tool (LLM-as-router pattern). stdio transport, lazy model loading per collection
- **Success signal**: Claude Code can invoke all three search tools and receive correctly formatted, collection-labeled results; `list_documents` shows docs and code separately; server starts in <3s (lazy load), queries respond in <2s

**Phase 9: Integration & Configuration**
- **Goal**: Make the system easy to use and maintain, configuration-driven for reusability
- **Scope**: Create `rag.config.yaml` with per-collection settings (embedding model, chunking strategy, source patterns); update `config.py` to load collections from YAML. Add `.mcp.json` config for Claude Code. Update `.gitignore` for `.rag/` directory. Create PostToolUse hook for auto-reindexing when docs/code change. Add CLI help text with `--config` flag for custom config path. Set up `rag/` as git submodule in consuming project
- **Success signal**: A fresh clone can set up the RAG system with `git submodule update --init && cd rag && uv sync && cd .. && python -m rag.index`, and Claude Code auto-connects to the MCP server. Auto-reindex hook fires when editing docs. `rag.config.yaml` changes propagate without touching Python code

**Phase 10: Documentation & Portability**
- **Goal**: Comprehensive documentation enabling independent adoption in new projects via git submodule
- **Scope**: Create `rag/README.md` covering: Quick Start (5-minute setup via submodule), Architecture Overview (with dual-collection diagram), Configuration Reference (every `rag.config.yaml` field explained, including per-collection models and chunking overrides), Usage Guide (CLI commands incl. `rag init`, all MCP tools, `list_documents` resource, example queries showing docs vs code search), Troubleshooting (common issues: macOS SQLite, model download, extension loading, dual-model memory), Design Decisions (why each tech was chosen, why separate collections), Reuse Guide (step-by-step: add submodule → `rag init` → edit config → define collections → index → done)
- **Success signal**: A developer unfamiliar with the project can adopt the RAG system in a new project by following the README alone, in under 5 minutes, without asking any questions

### Parallelism Notes

Phases 2, 3, 4, and 5 can run in parallel after Phase 1 completes — they touch different domains (document parsing, code parsing, embedding generation, database operations) with no shared state. Phase 6 integrates all four and must wait for their completion. Phases 7-9 are sequential as each builds on the previous. Phase 10 (Documentation) depends on Phase 9 because it documents the final configuration and CLI interface, but documentation drafting can begin earlier as an ongoing activity.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Database | SQLite + sqlite-vec | ChromaDB, LanceDB, Qdrant, Pinecone | Zero dependencies, single-file, same DB for vectors + FTS5, runs anywhere SQLite runs. Aligns with project's minimalist philosophy |
| Embedding library | fastembed (ONNX) | sentence-transformers (PyTorch), sqlite-lembed (GGUF), Ollama | Lightest option (~90MB vs ~2GB for sentence-transformers). No GPU needed. Built-in reranker support. ONNX Runtime is fast on CPU |
| Doc embedding model | BAAI/bge-small-en-v1.5 (384d) | all-MiniLM-L6-v2, nomic-embed-text-v1.5 (768d) | Best MTEB at small size. 512 token window matches doc chunk size. nomic will be benchmarked as alternative via config toggle |
| Code embedding model | jinaai/jina-embeddings-v2-base-code (768d) | nomic-embed-code (7B), voyage-code-3 (API) | Only code-specific model in fastembed. Trained on 30+ languages + English. 8192 token context fits large code blocks. ~14% better than general models on code retrieval. nomic-embed-code is 7B (too large for ONNX), voyage-code-3 is API-only |
| Collection architecture | Separate vec0 tables per content type | Single table + metadata filter, separate DB files | sqlite-vec uses brute-force KNN with no pre-filter — separate tables ARE the pre-filter. Different dimensions (384d vs 768d) require separate vec0 tables. Validated by Continue.dev (separate codebase/docs contexts) and Qdrant multitenancy docs |
| Code chunking engine | tree-sitter AST-based | regex splitting, line-based, LLM-based | Industry standard for code splitting (LlamaIndex, Sweep AI, Continue.dev). Preserves semantic boundaries (functions, classes). `tree-sitter-language-pack` covers 305+ languages |
| MCP tool routing | LLM-as-router (separate tools) | Custom query classifier, user-specified collection | Expose `search_docs`, `search_code`, `search_all` with clear descriptions — the LLM selects based on task context. Validated by Continue.dev pattern (`search_codebase` vs `get_file_context`). No custom routing code to maintain |
| Language | Python | Node.js/TypeScript | fastembed is Python-native. sqlite-vec has first-class Python bindings. tree-sitter has mature Python bindings. MCP SDK available in both but Python ecosystem for embeddings is far stronger |
| Package manager | uv | pip, poetry, conda | Fast, modern, no system pollution. Single binary. Supports pyproject.toml natively |
| Doc chunking | Markdown header-based + recursive | Fixed-size, sentence-based, semantic | Documents have clear structure (H1/H2/H3). Header-based preserves semantic coherence. Recursive fallback handles long sections |
| Code chunk size | ~1500 chars (~300 tokens, ~40 lines) | 500 chars, 3000 chars | Optimal precision per Sweep AI research. Maps to typical function/method size. Jina-code model supports up to 8192 tokens so no window pressure |
| Search strategy | Hybrid (vector + FTS5 + RRF) | Vector-only, keyword-only | Research consistently shows hybrid outperforms either alone. RRF is simple and parameter-free |
| Cross-collection search | Normalized RRF score merging | Reranking, learned fusion | Scores from different embedding models are not directly comparable — normalize to 0-1 range before merging. Simple, no training required |
| MCP transport | stdio | SSE, HTTP | stdio is the standard for local single-user MCP servers. Simplest to configure |
| Data directory | `.rag/` (gitignored) | `data/`, `db/`, embedded in `.claude/` | Follows convention of dotfiles for tool-specific data. Keeps project root clean. Easy to gitignore |
| Change detection | SHA-256 file hash | mtime, git diff, file watcher | Hash is deterministic and portable. mtime is unreliable across clones. Git diff adds complexity |
| Configuration | YAML config file (`rag.config.yaml`) | Hardcoded constants, .env, CLI-only | YAML is human-readable, supports complex structures (collections with per-source overrides). Single file to edit when reusing. CLI args complement but don't replace config |
| Reusability strategy | Git submodule + project config | Copy dir, pip package, monorepo | Git submodule provides versioning, easy updates via `git submodule update`, clean separation. Config-driven means zero code changes. Can evolve to pip package later once battle-tested |
| Re-indexing trigger | Manual CLI + PostToolUse hook | Manual only, file watcher | Both options cover different workflows: CLI for explicit rebuilds, hook for automatic freshness during editing sessions |

---

## Research Summary

**Market Context**

The local RAG space has matured significantly in 2024-2026:
- **sqlite-vec** (by Alex Garcia, Mozilla Builders project) is the leading SQLite vector extension, succeeding sqlite-vss. Pure C, zero dependencies, supports float32/int8/binary vectors. Pre-v1 but API is stable. Used in production by Fly.io, Turso, and SQLite Cloud.
- **fastembed** (by Qdrant) is the lightweight embedding alternative to sentence-transformers. Uses ONNX Runtime instead of PyTorch, resulting in ~90MB install vs ~2GB. Supports 25+ text embedding models, sparse embeddings (SPLADE++), and cross-encoder reranking.
- **MCP (Model Context Protocol)** by Anthropic is the emerging standard for AI tool integration. Claude Code, Cursor, and other tools natively support MCP servers via stdio transport. Python SDK (FastMCP) and TypeScript SDK are both mature.
- **sqlite-lembed** is a sister project to sqlite-vec that generates embeddings inside SQLite using llama.cpp GGUF models. Interesting but less mature than fastembed, lacks batch support, and model ecosystem is smaller.

**Code RAG Research (Collection Separation & Code Chunking)**

Collection separation is a validated best practice for RAG systems indexing heterogeneous content:
- **Continue.dev** (leading open-source AI code assistant) explicitly separates documentation context from codebase context in its retrieval pipeline. Different tools query different collections.
- **Qdrant multitenancy documentation** recommends per-embedding-model collections. Since different content types benefit from different embedding models (general vs code-specific), separate vec0 tables are the correct architecture.
- **Sourcegraph Cody** separates docs from code context in its retrieval system, confirming the pattern at scale.
- **sqlite-vec limitation**: Uses brute-force KNN with no WHERE clause filtering on vector search. This means a "collection" metadata column can't be used as a pre-filter — separate tables ARE the pre-filter mechanism.

Code-specific chunking and embedding research:
- **tree-sitter** is the industry standard for AST-based code chunking. Used by LlamaIndex CodeSplitter, Sweep AI, and Continue.dev. Python bindings via `tree-sitter` + `tree-sitter-language-pack` (305+ languages, actively maintained replacement for the unmaintained `tree-sitter-languages`).
- **Optimal code chunk size**: ~1500 chars (~300 tokens, ~40 lines) provides best precision per Sweep AI research. This maps to typical function/method size.
- **Code chunk metadata**: File path, function/class name, imports, parent hierarchy, and docstrings should be preserved. Symbol-level metadata enables structured code navigation beyond text search.
- **jinaai/jina-embeddings-v2-base-code** (768d, 8192 context, 640MB, Apache 2.0): The only code-specific embedding model available in fastembed. Trained on 30+ programming languages + English. Supports markdown, shell, YAML explicitly.
- **Code-specific models outperform general-purpose** by ~14% on code retrieval tasks (Voyage AI benchmarks, MTEB code retrieval leaderboard). This justifies the dual-model approach despite higher memory usage.
- **Not viable locally**: `nomic-embed-code` is 7B params (too large for ONNX Runtime); `voyage-code-3` is API-only. `jina-code` is the practical choice.

**Technical Context**

- **sqlite-vec API**: Uses `vec0` virtual tables with `CREATE VIRTUAL TABLE ... USING vec0(embedding float[N])`. KNN search via `WHERE embedding MATCH ? ORDER BY distance LIMIT k`. Supports cosine, L2, and hamming distances. Metadata columns via `+column_name TYPE` syntax.
- **fastembed models**: BAAI/bge-small-en-v1.5 (384d, 67MB, 512 tokens) is the best quality/size tradeoff for docs. jinaai/jina-embeddings-v2-base-code (768d, 640MB, 8192 tokens) is the best for code. all-MiniLM-L6-v2 (384d, 90MB) is the most popular but slightly lower MTEB scores.
- **FTS5 in SQLite**: Built-in full-text search with BM25 scoring. Can be combined with sqlite-vec in the same database file for hybrid search. External content mode (`content=''`) avoids data duplication.
- **Reciprocal Rank Fusion (RRF)**: Simple fusion method: `score(d) = Σ 1/(k + rank_i(d))` where k=60 is standard. Outperforms other fusion methods while being parameter-free.
- **MCP Server (Python)**: FastMCP decorator pattern (`@mcp.tool()`) with type hints auto-generates tool schemas. stdio transport is simplest. Server runs as a subprocess managed by the AI tool.
- **LLM-as-router pattern**: Instead of building a custom query classifier, expose separate tools (`search_docs`, `search_code`, `search_all`) with clear descriptions and let the LLM choose. This is exactly what Continue.dev does with `search_codebase` vs `get_file_context`.

**Key References**
- sqlite-vec: https://github.com/asg017/sqlite-vec | https://alexgarcia.xyz/sqlite-vec/python.html
- sqlite-lembed: https://github.com/asg017/sqlite-lembed
- fastembed: https://github.com/qdrant/fastembed | https://qdrant.github.io/fastembed/
- MCP SDK: https://modelcontextprotocol.io/quickstart/server
- RRF paper: Cormack et al., "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods" (SIGIR 2009)
- tree-sitter: https://tree-sitter.github.io/tree-sitter/ | https://github.com/nickmqb/tree-sitter-language-pack
- jina-embeddings-v2-base-code: https://huggingface.co/jinaai/jina-embeddings-v2-base-code
- Continue.dev context guide: https://docs.continue.dev/customize/deep-dives/context
- Qdrant multitenancy: https://qdrant.tech/documentation/guides/multiple-partitions/
- Sweep AI code chunking: https://docs.sweep.dev/blogs/chunking-2m-files

---

*Generated: 2026-04-10T03:33Z*
*Updated: 2026-04-10T14:30Z — Added code file indexing with dual-collection architecture*
*Status: PLAN READY — [`.claude/PRPs/plans/local-rag-knowledge-base.plan.md`](../.claude/PRPs/plans/local-rag-knowledge-base.plan.md)*
