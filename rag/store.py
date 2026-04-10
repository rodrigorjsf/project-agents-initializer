"""SQLite + sqlite-vec + FTS5 dual-collection storage layer."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import sqlite_vec


class Store:
    """Manages the RAG knowledge base SQLite database.

    Uses sqlite-vec for vector KNN search, FTS5 for full-text search,
    WAL journal mode for concurrent read/write access.
    """

    def __init__(self, db_path: str) -> None:
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA busy_timeout=5000")
        self.db.enable_load_extension(True)
        sqlite_vec.load(self.db)
        self.db.enable_load_extension(False)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.db.cursor()

        # Shared documents table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                file_path TEXT UNIQUE NOT NULL,
                collection TEXT NOT NULL,
                title TEXT,
                category TEXT,
                file_hash TEXT NOT NULL,
                chunk_count INTEGER DEFAULT 0,
                indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Doc chunks with denormalized file_path for FTS5
        cur.execute("""
            CREATE TABLE IF NOT EXISTS doc_chunks (
                id INTEGER PRIMARY KEY,
                document_id INTEGER NOT NULL REFERENCES documents(id),
                chunk_index INTEGER NOT NULL,
                section_header TEXT,
                content TEXT NOT NULL,
                file_path TEXT NOT NULL,
                start_line INTEGER,
                end_line INTEGER,
                token_count INTEGER,
                reading_order INTEGER
            )
        """)

        # Code chunks with denormalized file_path for FTS5
        cur.execute("""
            CREATE TABLE IF NOT EXISTS code_chunks (
                id INTEGER PRIMARY KEY,
                document_id INTEGER NOT NULL REFERENCES documents(id),
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                file_path TEXT NOT NULL,
                language TEXT,
                symbol_type TEXT,
                symbol_name TEXT,
                parent_symbol TEXT,
                start_line INTEGER,
                end_line INTEGER,
                char_count INTEGER
            )
        """)

        # Vec0 virtual tables for vector KNN
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_docs USING vec0(
                embedding float[384],
                +chunk_id INTEGER
            )
        """)
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_code USING vec0(
                embedding float[768],
                +chunk_id INTEGER
            )
        """)

        # FTS5 external content tables
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
                content,
                section_header,
                file_path,
                content='doc_chunks',
                content_rowid='id'
            )
        """)
        cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS code_fts USING fts5(
                content,
                symbol_name,
                file_path,
                language,
                content='code_chunks',
                content_rowid='id'
            )
        """)

        self.db.commit()
        self._create_fts_triggers()

    def _create_fts_triggers(self) -> None:
        """Create INSERT/DELETE/UPDATE triggers for FTS5 external content sync."""
        cur = self.db.cursor()

        # Doc chunks triggers
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS doc_chunks_ai AFTER INSERT ON doc_chunks BEGIN
                INSERT INTO docs_fts(rowid, content, section_header, file_path)
                VALUES (new.id, new.content, new.section_header, new.file_path);
            END
        """)
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS doc_chunks_ad AFTER DELETE ON doc_chunks BEGIN
                INSERT INTO docs_fts(docs_fts, rowid, content, section_header, file_path)
                VALUES ('delete', old.id, old.content, old.section_header, old.file_path);
            END
        """)
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS doc_chunks_au AFTER UPDATE ON doc_chunks BEGIN
                INSERT INTO docs_fts(docs_fts, rowid, content, section_header, file_path)
                VALUES ('delete', old.id, old.content, old.section_header, old.file_path);
                INSERT INTO docs_fts(rowid, content, section_header, file_path)
                VALUES (new.id, new.content, new.section_header, new.file_path);
            END
        """)

        # Code chunks triggers
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS code_chunks_ai AFTER INSERT ON code_chunks BEGIN
                INSERT INTO code_fts(rowid, content, symbol_name, file_path, language)
                VALUES (new.id, new.content, new.symbol_name, new.file_path, new.language);
            END
        """)
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS code_chunks_ad AFTER DELETE ON code_chunks BEGIN
                INSERT INTO code_fts(code_fts, rowid, content, symbol_name, file_path, language)
                VALUES ('delete', old.id, old.content, old.symbol_name, old.file_path, old.language);
            END
        """)
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS code_chunks_au AFTER UPDATE ON code_chunks BEGIN
                INSERT INTO code_fts(code_fts, rowid, content, symbol_name, file_path, language)
                VALUES ('delete', old.id, old.content, old.symbol_name, old.file_path, old.language);
                INSERT INTO code_fts(rowid, content, symbol_name, file_path, language)
                VALUES (new.id, new.content, new.symbol_name, new.file_path, new.language);
            END
        """)

        self.db.commit()

    def upsert_document(
        self,
        file_path: str,
        collection: str,
        title: str,
        category: str,
        file_hash: str,
    ) -> int:
        """Insert or update a document record. Returns the document ID."""
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO documents (file_path, collection, title, category, file_hash, indexed_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(file_path) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                file_hash = excluded.file_hash,
                indexed_at = CURRENT_TIMESTAMP
            """,
            (file_path, collection, title, category, file_hash),
        )
        self.db.commit()
        row = cur.execute(
            "SELECT id FROM documents WHERE file_path = ?", (file_path,)
        ).fetchone()
        return row["id"]

    def insert_doc_chunks(
        self,
        doc_id: int,
        chunks: list[dict],
        embeddings: list[list[float]],
        file_path: str,
    ) -> None:
        """Bulk insert doc chunks and their embeddings."""
        cur = self.db.cursor()
        cur.execute("BEGIN")
        try:
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                cur.execute(
                    """
                    INSERT INTO doc_chunks
                        (document_id, chunk_index, section_header, content, file_path,
                         start_line, end_line, token_count, reading_order)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        doc_id, i, chunk.get("section_header", ""),
                        chunk["content"], file_path,
                        chunk.get("start_line"), chunk.get("end_line"),
                        chunk.get("token_count"), chunk.get("reading_order"),
                    ),
                )
                chunk_id = cur.lastrowid
                cur.execute(
                    "INSERT INTO vec_docs (embedding, chunk_id) VALUES (?, ?)",
                    (sqlite_vec.serialize_float32(embedding), chunk_id),
                )
            cur.execute(
                "UPDATE documents SET chunk_count = ? WHERE id = ?",
                (len(chunks), doc_id),
            )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def insert_code_chunks(
        self,
        doc_id: int,
        chunks: list[dict],
        embeddings: list[list[float]],
        file_path: str,
    ) -> None:
        """Bulk insert code chunks and their embeddings."""
        cur = self.db.cursor()
        cur.execute("BEGIN")
        try:
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                cur.execute(
                    """
                    INSERT INTO code_chunks
                        (document_id, chunk_index, content, file_path, language,
                         symbol_type, symbol_name, parent_symbol,
                         start_line, end_line, char_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        doc_id, i, chunk["content"], file_path,
                        chunk.get("language"), chunk.get("symbol_type"),
                        chunk.get("symbol_name"), chunk.get("parent_symbol"),
                        chunk.get("start_line"), chunk.get("end_line"),
                        chunk.get("char_count"),
                    ),
                )
                chunk_id = cur.lastrowid
                cur.execute(
                    "INSERT INTO vec_code (embedding, chunk_id) VALUES (?, ?)",
                    (sqlite_vec.serialize_float32(embedding), chunk_id),
                )
            cur.execute(
                "UPDATE documents SET chunk_count = ? WHERE id = ?",
                (len(chunks), doc_id),
            )
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def get_document_hash(self, file_path: str) -> str | None:
        """Get stored hash for a file, or None if not indexed."""
        row = self.db.execute(
            "SELECT file_hash FROM documents WHERE file_path = ?", (file_path,)
        ).fetchone()
        return row["file_hash"] if row else None

    def delete_document_chunks(self, doc_id: int, collection: str) -> None:
        """Delete all chunks, vec rows, and FTS entries for a document.

        FTS cleanup is handled by triggers on chunk deletion.
        Vec0 tables do NOT support triggers — explicit deletion required.
        """
        cur = self.db.cursor()
        if collection == "docs":
            # Delete vec rows explicitly (no trigger support)
            cur.execute(
                "DELETE FROM vec_docs WHERE chunk_id IN "
                "(SELECT id FROM doc_chunks WHERE document_id = ?)",
                (doc_id,),
            )
            # Delete chunks (triggers handle FTS cleanup)
            cur.execute("DELETE FROM doc_chunks WHERE document_id = ?", (doc_id,))
        else:
            cur.execute(
                "DELETE FROM vec_code WHERE chunk_id IN "
                "(SELECT id FROM code_chunks WHERE document_id = ?)",
                (doc_id,),
            )
            cur.execute("DELETE FROM code_chunks WHERE document_id = ?", (doc_id,))
        self.db.commit()

    def delete_stale_documents(
        self, collection: str, current_file_paths: set[str]
    ) -> int:
        """Remove documents that no longer exist on disk. Returns count removed."""
        rows = self.db.execute(
            "SELECT id, file_path FROM documents WHERE collection = ?",
            (collection,),
        ).fetchall()

        removed = 0
        for row in rows:
            if row["file_path"] not in current_file_paths:
                self.delete_document_chunks(row["id"], collection)
                self.db.execute("DELETE FROM documents WHERE id = ?", (row["id"],))
                removed += 1
        if removed:
            self.db.commit()
        return removed

    def vector_search(
        self, collection: str, embedding: list[float], top_k: int
    ) -> list[dict]:
        """KNN vector search on a collection's vec0 table."""
        table = "vec_docs" if collection == "docs" else "vec_code"
        chunk_table = "doc_chunks" if collection == "docs" else "code_chunks"

        query_bytes = sqlite_vec.serialize_float32(embedding)
        # vec0 KNN must be a standalone query — no JOINs or subqueries
        knn_rows = self.db.execute(
            f"SELECT chunk_id, distance FROM {table} "
            "WHERE embedding MATCH ? AND k = ?",
            (query_bytes, top_k),
        ).fetchall()

        if not knn_rows:
            return []

        # Fetch chunk metadata in a second query
        chunk_ids = [r["chunk_id"] for r in knn_rows]
        distances = {r["chunk_id"]: r["distance"] for r in knn_rows}
        placeholders = ",".join("?" for _ in chunk_ids)
        rows = self.db.execute(
            f"SELECT * FROM {chunk_table} WHERE id IN ({placeholders})",
            chunk_ids,
        ).fetchall()

        results = []
        for r in rows:
            d = dict(r)
            d["distance"] = distances.get(d["id"], 0.0)
            results.append(d)

        # Sort by distance (ascending — closer is better)
        results.sort(key=lambda x: x["distance"])
        return results

    def fts_search(
        self, collection: str, query: str, top_k: int
    ) -> list[dict]:
        """FTS5 BM25 full-text search on a collection."""
        fts_table = "docs_fts" if collection == "docs" else "code_fts"
        chunk_table = "doc_chunks" if collection == "docs" else "code_chunks"

        try:
            rows = self.db.execute(
                f"""
                SELECT c.*, rank
                FROM {fts_table} f
                JOIN {chunk_table} c ON c.id = f.rowid
                WHERE {fts_table} MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (query, top_k),
            ).fetchall()
        except sqlite3.OperationalError:
            # Invalid FTS query syntax
            return []

        return [dict(r) for r in rows]

    def get_all_documents(self, collection: str | None = None) -> list[dict]:
        """Get all indexed documents, optionally filtered by collection."""
        if collection:
            rows = self.db.execute(
                "SELECT * FROM documents WHERE collection = ? ORDER BY file_path",
                (collection,),
            ).fetchall()
        else:
            rows = self.db.execute(
                "SELECT * FROM documents ORDER BY collection, file_path"
            ).fetchall()
        return [dict(r) for r in rows]

    def get_chunks_by_file(self, file_path: str) -> list[dict]:
        """Get all chunks for a specific file path."""
        doc = self.db.execute(
            "SELECT id, collection FROM documents WHERE file_path = ?",
            (file_path,),
        ).fetchone()
        if not doc:
            return []

        table = "doc_chunks" if doc["collection"] == "docs" else "code_chunks"
        rows = self.db.execute(
            f"SELECT * FROM {table} WHERE document_id = ? ORDER BY chunk_index",
            (doc["id"],),
        ).fetchall()
        return [dict(r) for r in rows]

    def rebuild_fts(self) -> None:
        """Rebuild FTS5 indexes. Use only on first index or as repair."""
        self.db.execute("INSERT INTO docs_fts(docs_fts) VALUES('rebuild')")
        self.db.execute("INSERT INTO code_fts(code_fts) VALUES('rebuild')")
        self.db.commit()

    def close(self) -> None:
        self.db.close()
