---
paths:
  - "rag.config.yaml"
  - "rag/store.py"
  - "rag/search.py"
  - "rag/index.py"
  - "rag/config.py"
---
# RAG Storage and Search

- Treat `docs` and `code` as coordinated schemas, not config-only names: `vec_docs` is 384d, `vec_code` is 768d, and the CLI/MCP surfaces expose only those collections.
- Keep sqlite-vec KNN queries as standalone `MATCH` statements; do not add JOINs or subqueries around vec0 search. Fetch chunk metadata in a second query.
- When reindexing or deleting chunks, remove vec rows explicitly and let chunk-table triggers keep FTS tables in sync; vec0 tables do not support trigger-based cleanup.
- Store indexed `file_path` values relative to the config directory / project root, not as absolute paths, so change detection, stale cleanup, and `get_doc_context()` keep working.
