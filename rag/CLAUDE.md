# Local RAG package for indexing project content and serving MCP search tools.

## Tooling

- Package manager: `uv`
- Run repo-root commands as `uv run --project rag python -m rag [index|search|serve|init]`
- Start MCP the same way as `.mcp.json`: `uv run --project rag python -m rag.server` with `RAG_CONFIG_PATH=rag.config.yaml`

## Conventions

- Config resolution is `--config` -> `RAG_CONFIG_PATH` -> `rag.config.yaml`; relative sources, database paths, and model cache paths resolve from the config file directory, not `rag/`.
- `docs` and `code` are coordinated across YAML config, CLI, MCP tools, and SQLite schema; changing collections or embedding dimensions requires code changes beyond `rag.config.yaml`.
- For MCP transport invariants, see `../.claude/rules/rag-mcp-server.md`.
- For SQLite/sqlite-vec/FTS invariants, see `../.claude/rules/rag-storage-and-search.md`.
