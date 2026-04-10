"""AST-based code chunker using tree-sitter-language-pack."""

from __future__ import annotations

import os
from dataclasses import dataclass

from tree_sitter_language_pack import detect_language, process, ProcessConfig

from rag.chunker import chunk_markdown, ChunkResult


@dataclass
class CodeChunkResult:
    content: str
    language: str
    symbol_type: str | None
    symbol_name: str | None
    parent_symbol: str | None
    start_line: int
    end_line: int
    char_count: int


# Extensions that should be chunked as markdown, not code
MARKDOWN_EXTENSIONS = {".md", ".markdown", ".mdx"}

# Extensions that don't parse well with tree-sitter
PLAIN_TEXT_EXTENSIONS = {".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".txt"}


def _fixed_size_split(
    source: str, max_chars: int, file_path: str, language: str
) -> list[CodeChunkResult]:
    """Fallback: split by line boundaries up to max_chars."""
    lines = source.split("\n")
    chunks: list[CodeChunkResult] = []
    current_lines: list[str] = []
    current_chars = 0
    start_line = 1

    for i, line in enumerate(lines, 1):
        line_len = len(line) + 1  # +1 for newline
        if current_chars + line_len > max_chars and current_lines:
            content = "\n".join(current_lines)
            chunks.append(CodeChunkResult(
                content=content,
                language=language,
                symbol_type=None,
                symbol_name=None,
                parent_symbol=None,
                start_line=start_line,
                end_line=i - 1,
                char_count=len(content),
            ))
            current_lines = [line]
            current_chars = line_len
            start_line = i
        else:
            current_lines.append(line)
            current_chars += line_len

    if current_lines:
        content = "\n".join(current_lines)
        chunks.append(CodeChunkResult(
            content=content,
            language=language,
            symbol_type=None,
            symbol_name=None,
            parent_symbol=None,
            start_line=start_line,
            end_line=len(lines),
            char_count=len(content),
        ))

    return chunks


def _find_symbol_for_chunk(
    structure: list | None, start_line: int, end_line: int
) -> tuple[str | None, str | None, str | None]:
    """Walk the structure tree to find the best matching symbol for a chunk's line range.

    Returns (symbol_type, symbol_name, parent_symbol).
    """
    if not structure:
        return None, None, None

    best_match: tuple[str | None, str | None, str | None] = (None, None, None)

    def walk(nodes: list, parent_name: str | None = None) -> None:
        nonlocal best_match
        for node in nodes:
            node_start = node.get("start_line", 0)
            node_end = node.get("end_line", 0)
            # Check if this node overlaps with the chunk
            if node_start <= end_line and node_end >= start_line:
                sym_type = node.get("type")
                sym_name = node.get("name")
                if sym_name:
                    best_match = (sym_type, sym_name, parent_name)
                children = node.get("children", [])
                if children:
                    walk(children, sym_name or parent_name)

    walk(structure)
    return best_match


def chunk_code(
    source: str,
    file_path: str,
    max_chars: int = 1500,
    language: str | None = None,
    language_map: dict[str, str] | None = None,
) -> list[CodeChunkResult]:
    """Chunk source code using tree-sitter-language-pack's process() API.

    Args:
        source: Source code text
        file_path: File path for language detection
        max_chars: Maximum characters per chunk
        language: Explicit language override
        language_map: Extension-to-language mapping from config
    """
    if not source.strip():
        return []

    ext = os.path.splitext(file_path)[1].lower()

    # Markdown files delegate to markdown chunker
    if ext in MARKDOWN_EXTENSIONS:
        md_chunks = chunk_markdown(source, max_tokens=max_chars // 5, file_path=file_path)
        return [
            CodeChunkResult(
                content=c.content,
                language="markdown",
                symbol_type="section",
                symbol_name=c.section_header or None,
                parent_symbol=None,
                start_line=c.start_line,
                end_line=c.end_line,
                char_count=len(c.content),
            )
            for c in md_chunks
        ]

    # Resolve language
    resolved_lang = language
    if not resolved_lang and language_map:
        resolved_lang = language_map.get(ext)
    if not resolved_lang:
        try:
            resolved_lang = detect_language(file_path)
        except Exception:
            resolved_lang = None

    # Plain text files or undetected languages: fixed-size split
    if ext in PLAIN_TEXT_EXTENSIONS or not resolved_lang:
        return _fixed_size_split(source, max_chars, file_path, resolved_lang or "text")

    # Use tree-sitter-language-pack process() API
    try:
        config = ProcessConfig(
            language=resolved_lang,
            chunk_max_size=max_chars,
            structure=True,
            docstrings=True,
        )
        result = process(source, config)
    except Exception:
        return _fixed_size_split(source, max_chars, file_path, resolved_lang)

    raw_chunks = result.get("chunks", [])
    structure = result.get("structure")

    if not raw_chunks:
        return _fixed_size_split(source, max_chars, file_path, resolved_lang)

    chunks: list[CodeChunkResult] = []
    for raw in raw_chunks:
        content = raw.get("content", "")
        metadata = raw.get("metadata", {})
        start_line = metadata.get("start_line", 1)
        end_line = metadata.get("end_line", start_line)

        sym_type, sym_name, parent_sym = _find_symbol_for_chunk(
            structure, start_line, end_line
        )

        chunks.append(CodeChunkResult(
            content=content,
            language=resolved_lang,
            symbol_type=sym_type,
            symbol_name=sym_name,
            parent_symbol=parent_sym,
            start_line=start_line,
            end_line=end_line,
            char_count=len(content),
        ))

    return chunks
