"""Hybrid search engine: vector (sqlite-vec) + FTS5 + Reciprocal Rank Fusion."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag.config import RagConfig
from rag.embedder import Embedder
from rag.store import Store


@dataclass
class SearchResult:
    chunk_id: int
    content: str
    file_path: str
    score: float
    collection: str
    section_header: str | None = None
    symbol_name: str | None = None
    start_line: int | None = None
    end_line: int | None = None
    language: str | None = None
    reading_order: int | None = None


def _fts5_query(query: str) -> str:
    """Convert natural language to FTS5 query.

    Wraps each token in double quotes and joins with OR for safe matching.
    """
    tokens = query.split()
    if not tokens:
        return '""'
    # Remove special FTS5 chars, wrap each token
    safe_tokens = []
    for t in tokens:
        cleaned = re.sub(r'[^\w\-]', '', t)
        if cleaned:
            safe_tokens.append(f'"{cleaned}"')
    return " OR ".join(safe_tokens) if safe_tokens else '""'


class SearchEngine:
    """Hybrid search with per-collection and cross-collection support."""

    def __init__(self, config: RagConfig) -> None:
        self.config = config
        db_path = config.resolve_path(config.database.path)
        cache_dir = config.resolve_path(config.shared.cache_dir)
        self.store = Store(db_path)
        self.embedder = Embedder(cache_dir)

    def search_collection(
        self, query: str, collection: str, top_k: int = 5
    ) -> list[SearchResult]:
        """Hybrid search within a single collection using RRF fusion."""
        top_k = min(top_k, self.config.search.max_top_k)
        col_config = self.config.collections.get(collection)
        if not col_config:
            return []

        candidates = self.config.search.vector_candidates
        rrf_k = self.config.search.rrf_k

        # Vector search
        query_embedding = self.embedder.embed_query(
            query, col_config.embedding.model
        )
        vec_results = self.store.vector_search(collection, query_embedding, candidates)

        # FTS search
        fts_query = _fts5_query(query)
        fts_results = self.store.fts_search(
            collection, fts_query, self.config.search.fts_candidates
        )

        # RRF fusion: score(d) = Σ 1/(k + rank)  where rank is 1-indexed
        scores: dict[int, float] = {}
        chunk_data: dict[int, dict] = {}

        for rank, r in enumerate(vec_results, 1):
            cid = r["id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank)
            chunk_data[cid] = r

        for rank, r in enumerate(fts_results, 1):
            cid = r["id"]
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_k + rank)
            if cid not in chunk_data:
                chunk_data[cid] = r

        # Sort by RRF score descending, take top_k
        sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)[:top_k]

        results = []
        for cid in sorted_ids:
            data = chunk_data[cid]
            results.append(SearchResult(
                chunk_id=cid,
                content=data["content"],
                file_path=data["file_path"],
                score=scores[cid],
                collection=collection,
                section_header=data.get("section_header"),
                symbol_name=data.get("symbol_name"),
                start_line=data.get("start_line"),
                end_line=data.get("end_line"),
                language=data.get("language"),
                reading_order=data.get("reading_order"),
            ))

        return results

    def search_all(self, query: str, top_k: int = 5) -> list[SearchResult]:
        """Search across all collections with normalized score fusion."""
        top_k = min(top_k, self.config.search.max_top_k)

        all_results: list[SearchResult] = []
        for collection in self.config.collections:
            results = self.search_collection(query, collection, top_k * 2)
            all_results.extend(results)

        if not all_results:
            return []

        # Normalize scores to 0-1 per collection
        for collection in self.config.collections:
            col_results = [r for r in all_results if r.collection == collection]
            if not col_results:
                continue
            max_score = max(r.score for r in col_results)
            min_score = min(r.score for r in col_results)
            spread = max_score - min_score
            for r in col_results:
                r.score = (r.score - min_score) / spread if spread > 0 else 1.0

        # Sort by normalized score, return top_k
        all_results.sort(key=lambda r: r.score, reverse=True)
        return all_results[:top_k]


def format_results(results: list[SearchResult], collection: str) -> str:
    """Format search results for MCP tool output."""
    if not results:
        return f"No results found in {collection}."

    parts = [f"## Search Results ({collection})\n"]
    for i, r in enumerate(results, 1):
        header = f"### Result {i} — `{r.file_path}`"
        if r.start_line and r.end_line:
            header += f" (lines {r.start_line}-{r.end_line})"
        header += f" [score: {r.score:.4f}]"
        parts.append(header)

        if r.collection == "docs" and r.section_header:
            parts.append(f"**Section**: {r.section_header}")
        elif r.collection == "code":
            meta_parts = []
            if r.language:
                meta_parts.append(f"Language: {r.language}")
            if r.symbol_name:
                meta_parts.append(f"Symbol: {r.symbol_name}")
            if meta_parts:
                parts.append(f"**{' | '.join(meta_parts)}**")

        if collection == "all":
            parts.append(f"**Collection**: {r.collection}")

        parts.append(f"\n```\n{r.content}\n```\n")

    return "\n".join(parts)
