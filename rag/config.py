"""YAML configuration loader for RAG knowledge base."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class EmbeddingConfig:
    model: str = "BAAI/bge-small-en-v1.5"
    dimensions: int = 384


@dataclass
class ChunkingConfig:
    strategy: str = "markdown_header"
    max_tokens: int = 512
    max_chars: int = 1500
    overlap_tokens: int = 256
    split_headers: list[str] = field(default_factory=lambda: ["h1", "h2", "h3"])
    language: str | None = None
    languages: dict[str, str] = field(default_factory=dict)


@dataclass
class SourceConfig:
    path: str = ""
    patterns: list[str] = field(default_factory=lambda: ["*.md"])
    recursive: bool = True
    chunking: ChunkingConfig | None = None


@dataclass
class CollectionConfig:
    description: str = ""
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    sources: list[SourceConfig] = field(default_factory=list)
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)


@dataclass
class SearchConfig:
    default_top_k: int = 5
    max_top_k: int = 10
    rrf_k: int = 60
    vector_candidates: int = 20
    fts_candidates: int = 20


@dataclass
class DatabaseConfig:
    path: str = ".rag/knowledge.db"


@dataclass
class ServerConfig:
    name: str = "rag-docs"
    transport: str = "stdio"


@dataclass
class SharedConfig:
    cache_dir: str = ".rag/models"


@dataclass
class RagConfig:
    project_name: str = ""
    collections: dict[str, CollectionConfig] = field(default_factory=dict)
    shared: SharedConfig = field(default_factory=SharedConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    _config_dir: str = field(default="", repr=False)

    def resolve_path(self, rel_path: str) -> str:
        """Resolve a path relative to the config file's directory."""
        if os.path.isabs(rel_path):
            return rel_path
        return os.path.normpath(os.path.join(self._config_dir, rel_path))


def _build_chunking(data: dict) -> ChunkingConfig:
    if not data:
        return ChunkingConfig()
    return ChunkingConfig(
        strategy=data.get("strategy", "markdown_header"),
        max_tokens=data.get("max_tokens", 512),
        max_chars=data.get("max_chars", 1500),
        overlap_tokens=data.get("overlap_tokens", 256),
        split_headers=data.get("split_headers", ["h1", "h2", "h3"]),
        language=data.get("language"),
        languages=data.get("languages", {}),
    )


def _build_source(data: dict) -> SourceConfig:
    chunking = None
    if "chunking" in data:
        chunking = _build_chunking(data["chunking"])
    return SourceConfig(
        path=data.get("path", ""),
        patterns=data.get("patterns", ["*.md"]),
        recursive=data.get("recursive", True),
        chunking=chunking,
    )


def _build_collection(data: dict) -> CollectionConfig:
    emb_data = data.get("embedding", {})
    embedding = EmbeddingConfig(
        model=emb_data.get("model", "BAAI/bge-small-en-v1.5"),
        dimensions=emb_data.get("dimensions", 384),
    )
    sources = [_build_source(s) for s in data.get("sources", [])]
    chunking = _build_chunking(data.get("chunking", {}))
    return CollectionConfig(
        description=data.get("description", ""),
        embedding=embedding,
        sources=sources,
        chunking=chunking,
    )


def load_config(path: str | None = None) -> RagConfig:
    """Load RAG configuration from YAML file.

    Resolution order: explicit path → RAG_CONFIG_PATH env → rag.config.yaml in cwd.
    Paths in config are resolved relative to the config file's directory.
    """
    if path is None:
        path = os.environ.get("RAG_CONFIG_PATH")
    if path is None:
        path = "rag.config.yaml"

    config_path = Path(path).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        raw = yaml.safe_load(f)

    if not raw:
        raise ValueError(f"Empty or invalid config file: {config_path}")

    config_dir = str(config_path.parent)

    # Build collections
    collections = {}
    for name, col_data in raw.get("collections", {}).items():
        collections[name] = _build_collection(col_data)

    # Build shared config
    shared_data = raw.get("shared", {})
    shared = SharedConfig(cache_dir=shared_data.get("cache_dir", ".rag/models"))

    # Build database config
    db_data = raw.get("database", {})
    database = DatabaseConfig(path=db_data.get("path", ".rag/knowledge.db"))

    # Build search config
    search_data = raw.get("search", {})
    search = SearchConfig(
        default_top_k=search_data.get("default_top_k", 5),
        max_top_k=search_data.get("max_top_k", 10),
        rrf_k=search_data.get("rrf_k", 60),
        vector_candidates=search_data.get("vector_candidates", 20),
        fts_candidates=search_data.get("fts_candidates", 20),
    )

    # Build server config
    server_data = raw.get("server", {})
    server = ServerConfig(
        name=server_data.get("name", "rag-docs"),
        transport=server_data.get("transport", "stdio"),
    )

    project_data = raw.get("project", {})

    return RagConfig(
        project_name=project_data.get("name", ""),
        collections=collections,
        shared=shared,
        database=database,
        search=search,
        server=server,
        _config_dir=config_dir,
    )
