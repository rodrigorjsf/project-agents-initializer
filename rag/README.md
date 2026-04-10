# RAG Knowledge Base

Local, serverless RAG system using SQLite + sqlite-vec + FTS5. Designed for AI coding assistants (Claude Code, GitHub Copilot) to search project documentation and code without polluting context windows.

## Quick Start

```bash
# 1. Install dependencies
cd rag && uv sync && cd ..

# 2. Index your content
uv run --project rag python -m rag -c rag.config.yaml index

# 3. Test search
uv run --project rag python -m rag -c rag.config.yaml search "how to create hooks"

# 4. Start MCP server (Claude Code auto-starts via .mcp.json)
uv run --project rag python -m rag serve
```

First run downloads embedding models (~710MB total). Subsequent runs are instant.

## Architecture

```
┌─────────────────────────────────────────────┐
│              MCP Server (FastMCP)            │
│  search_docs · search_code · search_all     │
│  get_doc_context · list_documents           │
├─────────────────────────────────────────────┤
│              Hybrid Search                   │
│  Vector KNN (sqlite-vec) + BM25 (FTS5)      │
│  Reciprocal Rank Fusion (RRF)               │
├──────────────────┬──────────────────────────┤
│  docs collection │    code collection       │
│  bge-small-en    │    jina-code-v2          │
│  384 dimensions  │    768 dimensions        │
│  Markdown chunks │    tree-sitter chunks    │
├──────────────────┴──────────────────────────┤
│         SQLite + sqlite-vec + FTS5          │
│              .rag/knowledge.db              │
└─────────────────────────────────────────────┘
```

**Dual-collection design**: Documentation and code are indexed separately with specialized models and chunking strategies. This prevents code results from drowning out documentation (and vice versa) and lets AI agents target their searches precisely.

## Configuration

`rag.config.yaml` controls all behavior. Key sections:

```yaml
project:
  name: "my-project"

collections:
  docs:
    description: "Project documentation"
    embedding:
      model: "BAAI/bge-small-en-v1.5"  # Optimized for text retrieval
      dimensions: 384
    sources:
      - path: "docs/"
        patterns: ["*.md"]
        recursive: true
    chunking:
      strategy: "markdown_header"       # Split on headers
      max_tokens: 512
      overlap_tokens: 256
      split_headers: ["h1", "h2", "h3"]

  code:
    description: "Source code and configurations"
    embedding:
      model: "jinaai/jina-embeddings-v2-base-code"  # Code-aware
      dimensions: 768
    sources:
      - path: "plugins/"
        patterns: ["*.md", "*.py", "*.sh", "*.yaml"]
        recursive: true
    chunking:
      strategy: "tree_sitter"           # AST-aware splitting
      max_tokens: 256
      overlap_tokens: 128

shared:
  cache_dir: ".rag/models"              # Downloaded model cache

database:
  path: ".rag/knowledge.db"

search:
  default_top_k: 5
  max_top_k: 10
  rrf_k: 60                             # RRF fusion parameter
  vector_candidates: 20                 # KNN candidates per search
  fts_candidates: 20                    # FTS candidates per search

server:
  name: "rag-knowledge-base"
  transport: "stdio"
```

### Chunking Strategies

| Strategy | Best For | How It Works |
|----------|----------|--------------|
| `markdown_header` | `.md` files | Splits on `#` headers, preserves section hierarchy, protects code blocks and tables from mid-split |
| `tree_sitter` | Code files | Uses tree-sitter AST to split on function/class boundaries |
| `fixed` | Fallback | Fixed-size token windows with overlap |

### Multiple Source Directories

Each collection can have multiple source directories with different patterns:

```yaml
collections:
  code:
    sources:
      - path: "src/"
        patterns: ["*.py", "*.ts"]
        recursive: true
      - path: "scripts/"
        patterns: ["*.sh"]
        recursive: false
```

## CLI Commands

```bash
# Scaffold config for a new project
uv run --project rag python -m rag init

# Index all collections
uv run --project rag python -m rag -c rag.config.yaml index

# Index only docs
uv run --project rag python -m rag -c rag.config.yaml index --collection docs

# Search across all collections
uv run --project rag python -m rag -c rag.config.yaml search "query here"

# Search specific collection
uv run --project rag python -m rag -c rag.config.yaml search --collection code "function signature" -k 10

# Start MCP server
uv run --project rag python -m rag -c rag.config.yaml serve
```

## MCP Tools

When connected via `.mcp.json`, AI agents get these tools:

| Tool | Description |
|------|-------------|
| `search_docs(query, top_k)` | Search documentation collection only |
| `search_code(query, top_k)` | Search code collection only |
| `search_all(query, top_k)` | Search across all collections with score normalization |
| `get_doc_context(file_path)` | Get all chunks from a specific indexed file |
| `list_documents` | Resource listing all indexed documents with metadata |

### Example MCP Queries

```
search_docs("how to create Claude Code hooks")
search_code("hook validation implementation")
search_all("context engineering best practices")
get_doc_context("docs/claude-code/hooks/automate-workflow-with-hooks.md")
```

## How It Works

### Indexing Pipeline

1. **Scan** — Walk configured source directories, match file patterns
2. **Hash** — SHA-256 each file, skip unchanged files (incremental)
3. **Route** — Select chunking strategy based on collection config
4. **Chunk** — Split content into semantic units (markdown headers or AST nodes)
5. **Embed** — Generate vectors via fastembed (runs locally, no API calls)
6. **Store** — Insert chunks + vectors into SQLite with sqlite-vec + FTS5
7. **Reconcile** — Remove chunks from deleted/renamed files

### Search Pipeline

1. **Vector search** — KNN via sqlite-vec (semantic similarity)
2. **FTS search** — BM25 via FTS5 (keyword matching)
3. **RRF fusion** — Reciprocal Rank Fusion combines both result sets
4. **Score normalization** — Min-max normalization for cross-collection queries
5. **Return** — Top-k results with file path, line range, section, score, content

## Design Decisions

| Choice | Why |
|--------|-----|
| **SQLite + sqlite-vec** | Single file, zero infrastructure, WAL mode for concurrent read/write |
| **fastembed** | Local ONNX inference, no API keys, ~50ms/batch |
| **Dual collections** | Prevents code noise in doc searches; specialized models per domain |
| **bge-small-en-v1.5** (docs) | Best quality/size ratio for English text retrieval (384d) |
| **jina-embeddings-v2-base-code** (code) | Trained on code+text pairs, understands both (768d) |
| **tree-sitter-language-pack** (code chunking) | AST-aware splits preserve function boundaries |
| **Hybrid search (RRF)** | Vector catches semantic matches; FTS catches exact terms; fusion outperforms either alone |
| **FastMCP** | Official MCP SDK, stdio transport, zero config |

## Reuse in Other Projects

### Via Git Submodule

```bash
# Add to your project
git submodule add <rag-repo-url> rag
cd rag && uv sync && cd ..

# Scaffold config
uv run --project rag python -m rag init

# Edit rag.config.yaml for your project, then index
uv run --project rag python -m rag -c rag.config.yaml index
```

### MCP Integration

Create `.mcp.json` in your project root:

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

### Auto-Reindex Hook (Claude Code)

Copy `.claude/hooks/check-rag-reindex.sh` and register in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Create",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/check-rag-reindex.sh"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### First run is slow
Model downloads (~67MB for bge-small, ~642MB for jina-code) happen once. Subsequent runs use the cache in `.rag/models/`.

### Memory usage
Embedding models load ~700MB total when both collections are indexed. Single-collection indexing uses less.

### Python version
Requires Python ≥3.11. Tested with 3.13 and 3.14.

### SQLite extension loading
If `sqlite_vec.load()` fails, ensure your Python was built with extension loading enabled. Most distributions include this by default.

### "database is locked"
The database uses WAL mode for concurrent access. If you see lock errors, check for zombie indexing processes: `ps aux | grep "rag index"`.

## Tech Stack

| Component | Package | Version | Purpose |
|-----------|---------|---------|---------|
| Database | `sqlite3` (stdlib) | — | Storage engine |
| Vector search | `sqlite-vec` | 0.1.9 | KNN similarity search |
| Full-text search | FTS5 (SQLite) | — | BM25 keyword search |
| Doc embeddings | `fastembed` | 0.8.0 | Local ONNX inference |
| Doc model | `BAAI/bge-small-en-v1.5` | — | 384d text embeddings |
| Code model | `jinaai/jina-embeddings-v2-base-code` | — | 768d code embeddings |
| Code chunking | `tree-sitter-language-pack` | 1.5.1 | AST-aware splitting |
| Config | `PyYAML` | 6.0 | YAML configuration |
| MCP server | `mcp` (FastMCP) | 1.27 | AI tool integration |
| Package manager | `uv` | 0.11+ | Fast Python packaging |
