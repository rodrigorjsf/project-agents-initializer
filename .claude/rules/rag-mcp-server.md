---
paths:
  - ".mcp.json"
  - "rag/server.py"
  - "rag/cli.py"
---
# RAG MCP Server

- Keep server logs and other diagnostic output on `stderr`; `stdout` is reserved for FastMCP JSON-RPC transport.
- Preserve lazy initialization in `rag/server.py`; create `SearchEngine` and `Store` inside `_get_engine()` / `_get_store()`, not at import time.
- Keep `serve` aligned with `.mcp.json`: pass config through `RAG_CONFIG_PATH` and run the shared `mcp` instance over `stdio`.
