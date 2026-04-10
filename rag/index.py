"""Full indexing pipeline: scan → route → chunk → embed → store."""

from __future__ import annotations

import fnmatch
import hashlib
import os
import sys
import time

from rag.chunker import chunk_markdown, extract_reading_order
from rag.code_chunker import chunk_code
from rag.config import RagConfig, CollectionConfig, SourceConfig, ChunkingConfig
from rag.embedder import Embedder
from rag.store import Store


def _compute_file_hash(path: str) -> str:
    """SHA-256 hash of file contents."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            h.update(block)
    return h.hexdigest()


def _is_binary(path: str) -> bool:
    """Check if a file is binary by looking for null bytes in the first 8KB."""
    try:
        with open(path, "rb") as f:
            chunk = f.read(8192)
        return b"\x00" in chunk
    except (OSError, IOError):
        return True


def _detect_category(file_path: str, collection: str) -> str:
    """Infer category from file path."""
    parts = file_path.replace("\\", "/").split("/")
    if collection == "docs" and len(parts) >= 2:
        return parts[1] if parts[0] == "docs" else parts[0]
    if collection == "code":
        if "plugins/" in file_path and len(parts) >= 2:
            return f"plugins/{parts[1]}" if parts[0] == "plugins" else parts[0]
        if "skills/" in file_path:
            return "skills"
        if ".claude/" in file_path:
            return "claude"
    return "general"


def _extract_title(content: str, file_path: str) -> str:
    """Extract title from first H1 header or use filename."""
    for line in content.split("\n")[:10]:
        if line.startswith("# "):
            return line[2:].strip()
    return os.path.basename(file_path)


def _get_effective_chunking(
    source: SourceConfig, collection: CollectionConfig
) -> ChunkingConfig:
    """Get effective chunking config: source override > collection default."""
    return source.chunking if source.chunking else collection.chunking


class Indexer:
    """Orchestrates the full indexing pipeline."""

    def __init__(self, config: RagConfig) -> None:
        self.config = config
        db_path = config.resolve_path(config.database.path)
        cache_dir = config.resolve_path(config.shared.cache_dir)
        self.store = Store(db_path)
        self.embedder = Embedder(cache_dir)

        # Load reading order from docs/README.md
        readme_path = config.resolve_path("docs/README.md")
        self.reading_order = extract_reading_order(readme_path)

    def index_all(self, collection: str | None = None) -> None:
        """Index all collections (or a specific one)."""
        start = time.time()
        total_files = 0
        total_chunks = 0
        total_stale = 0

        targets = (
            {collection: self.config.collections[collection]}
            if collection and collection in self.config.collections
            else self.config.collections
        )

        for name, col_config in targets.items():
            files, chunks, stale = self._index_collection(name, col_config)
            total_files += files
            total_chunks += chunks
            total_stale += stale

        elapsed = time.time() - start
        print(
            f"\nIndexed {total_files} files ({total_chunks} chunks) in {elapsed:.1f}s.",
            file=sys.stderr,
        )
        if total_stale:
            print(f"Removed {total_stale} stale documents.", file=sys.stderr)

    def _index_collection(
        self, name: str, col_config: CollectionConfig
    ) -> tuple[int, int, int]:
        """Index a single collection. Returns (files_indexed, chunks_created, stale_removed)."""
        print(f"\n[{name}] Scanning sources...", file=sys.stderr)

        # 1. Scan all source directories for files
        current_files: set[str] = set()
        file_source_map: dict[str, SourceConfig] = {}

        for source in col_config.sources:
            source_path = self.config.resolve_path(source.path)
            if not os.path.isdir(source_path):
                print(
                    f"  Warning: source path not found: {source_path}",
                    file=sys.stderr,
                )
                continue

            for root, dirs, files in os.walk(source_path):
                if not source.recursive and root != source_path:
                    dirs.clear()
                    continue
                for fname in files:
                    abs_path = os.path.join(root, fname)
                    # Check patterns
                    if not any(
                        fnmatch.fnmatch(fname, pat) for pat in source.patterns
                    ):
                        continue
                    # Get relative path from project root
                    rel_path = os.path.relpath(abs_path, self.config._config_dir)
                    current_files.add(rel_path)
                    file_source_map[rel_path] = source

        # 2. Reconcile stale entries
        stale = self.store.delete_stale_documents(name, current_files)
        if stale:
            print(f"  [{name}] Removed {stale} stale documents", file=sys.stderr)

        # 3. Process each file
        files_indexed = 0
        chunks_created = 0
        is_first = self._is_first_index(name)

        for rel_path in sorted(current_files):
            abs_path = os.path.join(self.config._config_dir, rel_path)

            # Skip binary files
            if _is_binary(abs_path):
                continue

            # Change detection
            file_hash = _compute_file_hash(abs_path)
            existing_hash = self.store.get_document_hash(rel_path)
            if existing_hash == file_hash:
                continue

            try:
                with open(abs_path, encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except (OSError, IOError) as e:
                print(f"  Warning: cannot read {rel_path}: {e}", file=sys.stderr)
                continue

            if not content.strip():
                continue

            title = _extract_title(content, rel_path)
            category = _detect_category(rel_path, name)
            source = file_source_map[rel_path]
            chunking = _get_effective_chunking(source, col_config)

            # Chunk
            chunk_dicts = self._chunk_file(
                content, rel_path, name, chunking
            )

            if not chunk_dicts:
                continue

            # Embed
            texts = [c["content"] for c in chunk_dicts]
            embeddings = self.embedder.embed_texts(
                texts, col_config.embedding.model
            )

            # Delete old data if re-indexing
            if existing_hash is not None:
                doc_row = self.store.db.execute(
                    "SELECT id FROM documents WHERE file_path = ?", (rel_path,)
                ).fetchone()
                if doc_row:
                    self.store.delete_document_chunks(doc_row["id"], name)

            # Store
            doc_id = self.store.upsert_document(
                rel_path, name, title, category, file_hash
            )

            if name == "docs":
                self.store.insert_doc_chunks(doc_id, chunk_dicts, embeddings, rel_path)
            else:
                self.store.insert_code_chunks(doc_id, chunk_dicts, embeddings, rel_path)

            files_indexed += 1
            chunks_created += len(chunk_dicts)
            print(
                f"  [{name}] {rel_path} → {len(chunk_dicts)} chunks",
                file=sys.stderr,
            )

        # Rebuild FTS on first index only
        if is_first and files_indexed > 0:
            self.store.rebuild_fts()

        print(
            f"[{name}] Done: {files_indexed} files, {chunks_created} chunks",
            file=sys.stderr,
        )
        return files_indexed, chunks_created, stale

    def _chunk_file(
        self,
        content: str,
        file_path: str,
        collection: str,
        chunking: ChunkingConfig,
    ) -> list[dict]:
        """Chunk a file based on its strategy and collection type."""
        strategy = chunking.strategy

        if strategy == "markdown_header" or (
            strategy != "tree_sitter" and file_path.endswith(".md")
        ):
            md_chunks = chunk_markdown(
                content,
                max_tokens=chunking.max_tokens,
                overlap_tokens=chunking.overlap_tokens,
                split_headers=chunking.split_headers,
                file_path=file_path,
                reading_order_map=self.reading_order if collection == "docs" else None,
            )
            if collection == "docs":
                return [
                    {
                        "content": c.content,
                        "section_header": c.section_header,
                        "start_line": c.start_line,
                        "end_line": c.end_line,
                        "token_count": c.token_count,
                        "reading_order": c.reading_order,
                    }
                    for c in md_chunks
                ]
            else:
                return [
                    {
                        "content": c.content,
                        "language": "markdown",
                        "symbol_type": "section",
                        "symbol_name": c.section_header,
                        "parent_symbol": None,
                        "start_line": c.start_line,
                        "end_line": c.end_line,
                        "char_count": len(c.content),
                    }
                    for c in md_chunks
                ]

        # tree_sitter or other strategies for code
        code_chunks = chunk_code(
            content,
            file_path,
            max_chars=chunking.max_chars,
            language=chunking.language,
            language_map=chunking.languages,
        )
        return [
            {
                "content": c.content,
                "language": c.language,
                "symbol_type": c.symbol_type,
                "symbol_name": c.symbol_name,
                "parent_symbol": c.parent_symbol,
                "start_line": c.start_line,
                "end_line": c.end_line,
                "char_count": c.char_count,
            }
            for c in code_chunks
        ]

    def _is_first_index(self, collection: str) -> bool:
        """Check if this is the first index for a collection."""
        row = self.store.db.execute(
            "SELECT COUNT(*) as cnt FROM documents WHERE collection = ?",
            (collection,),
        ).fetchone()
        return row["cnt"] == 0
