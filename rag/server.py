"""FastMCP server exposing RAG search tools for AI agents."""

from __future__ import annotations

import logging
import sys

from mcp.server.fastmcp import FastMCP

# All output must go to stderr — stdout is the JSON-RPC transport
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("rag.server")

mcp = FastMCP("rag-knowledge-base")

# Lazy-initialized on first tool call
_engine = None
_store = None


def _get_engine():
    global _engine
    if _engine is None:
        from rag.config import load_config
        from rag.search import SearchEngine

        config = load_config()
        _engine = SearchEngine(config)
    return _engine


def _get_store():
    global _store
    if _store is None:
        from rag.config import load_config
        from rag.store import Store

        config = load_config()
        db_path = config.resolve_path(config.database.path)
        _store = Store(db_path)
    return _store


@mcp.tool()
async def search_docs(query: str, top_k: int = 5) -> str:
    """Search project DOCUMENTATION (guides, research, design decisions, analysis).
    Use this when the agent needs conceptual knowledge, design rationale, guidelines,
    or research findings. Returns markdown documentation chunks.

    Args:
        query: Natural language search query about project documentation
        top_k: Number of results to return (default: 5, max: 10)
    """
    from rag.search import format_results

    engine = _get_engine()
    results = engine.search_collection(query, "docs", min(top_k, 10))
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
    from rag.search import format_results

    engine = _get_engine()
    results = engine.search_collection(query, "code", min(top_k, 10))
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
    from rag.search import format_results

    engine = _get_engine()
    results = engine.search_all(query, min(top_k, 10))
    return format_results(results, collection="all")


@mcp.tool()
async def get_doc_context(file_path: str) -> str:
    """Get all indexed chunks from a specific file (documentation or code).

    Args:
        file_path: Relative path to the file (e.g., 'docs/general-llm/a-guide-to-agents.md')
    """
    store = _get_store()
    chunks = store.get_chunks_by_file(file_path)
    if not chunks:
        return f"No indexed content found for: {file_path}"

    parts = [f"## All chunks from `{file_path}`\n"]
    for i, chunk in enumerate(chunks, 1):
        start = chunk.get("start_line", "?")
        end = chunk.get("end_line", "?")
        parts.append(f"### Chunk {i} (lines {start}-{end})")
        parts.append(f"```\n{chunk['content']}\n```\n")
    return "\n".join(parts)


@mcp.resource("docs://index")
async def list_documents() -> str:
    """Browse all indexed documents organized by collection (docs vs code),
    with metadata: path, category, chunk count, reading order position."""
    store = _get_store()
    docs = store.get_all_documents()
    if not docs:
        return "No documents indexed yet. Run `rag index` first."

    parts = ["# Indexed Documents\n"]
    current_collection = None
    for doc in docs:
        if doc["collection"] != current_collection:
            current_collection = doc["collection"]
            parts.append(f"\n## {current_collection.upper()}\n")
            parts.append("| File | Category | Chunks |")
            parts.append("|------|----------|--------|")
        parts.append(
            f"| `{doc['file_path']}` | {doc['category']} | {doc['chunk_count']} |"
        )

    return "\n".join(parts)


if __name__ == "__main__":
    mcp.run(transport="stdio")
