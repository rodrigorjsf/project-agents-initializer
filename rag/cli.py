"""CLI entry points for RAG knowledge base: index, init, search, serve."""

from __future__ import annotations

import argparse
import os
import sys


def cmd_index(args: argparse.Namespace) -> None:
    """Run the indexing pipeline."""
    from rag.config import load_config
    from rag.index import Indexer

    config = load_config(args.config)
    indexer = Indexer(config)
    indexer.index_all(collection=args.collection)


def cmd_search(args: argparse.Namespace) -> None:
    """Search the knowledge base."""
    from rag.config import load_config
    from rag.search import SearchEngine, format_results

    config = load_config(args.config)
    engine = SearchEngine(config)

    if args.collection:
        results = engine.search_collection(args.query, args.collection, args.top_k)
        print(format_results(results, args.collection))
    else:
        results = engine.search_all(args.query, args.top_k)
        print(format_results(results, "all"))


def cmd_serve(args: argparse.Namespace) -> None:
    """Start the MCP server."""
    # Set config path for the server to find
    if args.config:
        os.environ["RAG_CONFIG_PATH"] = args.config
    from rag.server import mcp
    mcp.run(transport="stdio")


def cmd_init(args: argparse.Namespace) -> None:
    """Scaffold a new RAG configuration for a project."""
    config_path = os.path.join(os.getcwd(), "rag.config.yaml")
    if os.path.exists(config_path) and not args.force:
        print(f"Config already exists: {config_path}", file=sys.stderr)
        print("Use --force to overwrite.", file=sys.stderr)
        sys.exit(1)

    template = '''# RAG Knowledge Base Configuration
# Edit this file to match your project structure.

project:
  name: "{project_name}"

collections:
  docs:
    description: "Project documentation"
    embedding:
      model: "BAAI/bge-small-en-v1.5"
      dimensions: 384
    sources:
      - path: "docs/"
        patterns: ["*.md"]
        recursive: true
    chunking:
      strategy: "markdown_header"
      max_tokens: 512
      overlap_tokens: 256
      split_headers: ["h1", "h2", "h3"]

shared:
  cache_dir: ".rag/models"

database:
  path: ".rag/knowledge.db"

search:
  default_top_k: 5
  max_top_k: 10
  rrf_k: 60
  vector_candidates: 20
  fts_candidates: 20
'''
    project_name = os.path.basename(os.getcwd())
    with open(config_path, "w") as f:
        f.write(template.format(project_name=project_name))

    # Create .rag directory
    os.makedirs(".rag", exist_ok=True)

    print(f"Created: {config_path}", file=sys.stderr)
    print("Created: .rag/", file=sys.stderr)
    print("\nNext steps:", file=sys.stderr)
    print("  1. Edit rag.config.yaml to match your project", file=sys.stderr)
    print("  2. Run: rag index", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="rag",
        description="Local RAG knowledge base with SQLite + sqlite-vec",
    )
    parser.add_argument(
        "--config", "-c",
        default=None,
        help="Path to rag.config.yaml (default: auto-detect)",
    )
    sub = parser.add_subparsers(dest="command")

    # index
    p_index = sub.add_parser("index", help="Index documents and code")
    p_index.add_argument(
        "--collection",
        choices=["docs", "code"],
        default=None,
        help="Index only a specific collection",
    )

    # search
    p_search = sub.add_parser("search", help="Search the knowledge base")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument(
        "--collection",
        choices=["docs", "code"],
        default=None,
        help="Search only a specific collection",
    )
    p_search.add_argument(
        "--top-k", "-k",
        type=int,
        default=5,
        dest="top_k",
        help="Number of results (default: 5)",
    )

    # serve
    sub.add_parser("serve", help="Start MCP server")

    # init
    p_init = sub.add_parser("init", help="Scaffold config for a new project")
    p_init.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing config",
    )

    args = parser.parse_args()

    if args.command == "index":
        cmd_index(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "serve":
        cmd_serve(args)
    elif args.command == "init":
        cmd_init(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
