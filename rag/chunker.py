"""Markdown-aware document chunker with header-based splitting."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ChunkResult:
    content: str
    section_header: str
    start_line: int
    end_line: int
    token_count: int
    reading_order: int | None = None


# Header level patterns
HEADER_PATTERNS = {
    "h1": re.compile(r"^# "),
    "h2": re.compile(r"^## "),
    "h3": re.compile(r"^### "),
    "h4": re.compile(r"^#### "),
}


def _estimate_tokens(text: str) -> int:
    """Rough token estimate (~75% accurate, sufficient for chunking)."""
    return len(text.split())


def _is_header(line: str, split_headers: list[str]) -> tuple[bool, str, int]:
    """Check if line is a header at configured split levels.

    Returns (is_header, header_text, level).
    """
    for level_name in split_headers:
        pattern = HEADER_PATTERNS.get(level_name)
        if pattern and pattern.match(line):
            level = int(level_name[1])
            return True, line.strip().lstrip("#").strip(), level
    return False, "", 0


def _split_into_sections(
    text: str, split_headers: list[str]
) -> list[dict]:
    """Split text into sections based on header boundaries.

    Returns list of {header, header_hierarchy, content, start_line, end_line}.
    """
    lines = text.split("\n")
    sections: list[dict] = []
    current_content: list[str] = []
    current_header = ""
    current_start = 1
    header_stack: list[tuple[int, str]] = []

    for i, line in enumerate(lines, 1):
        is_hdr, hdr_text, level = _is_header(line, split_headers)
        if is_hdr and current_content:
            # Save previous section
            sections.append({
                "header": current_header,
                "header_hierarchy": _build_hierarchy(header_stack),
                "content": "\n".join(current_content),
                "start_line": current_start,
                "end_line": i - 1,
            })
            current_content = [line]
            current_header = hdr_text
            current_start = i
            # Update header stack
            while header_stack and header_stack[-1][0] >= level:
                header_stack.pop()
            header_stack.append((level, hdr_text))
        elif is_hdr:
            current_content.append(line)
            current_header = hdr_text
            current_start = i if not current_content or len(current_content) == 1 else current_start
            while header_stack and header_stack[-1][0] >= level:
                header_stack.pop()
            header_stack.append((level, hdr_text))
        else:
            current_content.append(line)

    if current_content:
        sections.append({
            "header": current_header,
            "header_hierarchy": _build_hierarchy(header_stack),
            "content": "\n".join(current_content),
            "start_line": current_start,
            "end_line": len(lines),
        })

    return sections if sections else [{
        "header": "",
        "header_hierarchy": "",
        "content": text,
        "start_line": 1,
        "end_line": len(lines),
    }]


def _build_hierarchy(stack: list[tuple[int, str]]) -> str:
    """Build a hierarchical header path like 'H1 > H2 > H3'."""
    if not stack:
        return ""
    return " > ".join(name for _, name in stack)


def _is_inside_block(lines: list[str], start: int, end: int) -> bool:
    """Check if a range is inside a fenced code block or table."""
    fence_count = 0
    for i in range(start):
        if lines[i].strip().startswith("```"):
            fence_count += 1
    return fence_count % 2 == 1


def _recursive_split(
    text: str, max_tokens: int, overlap_tokens: int
) -> list[str]:
    """Split text that exceeds max_tokens using paragraph/sentence boundaries."""
    if _estimate_tokens(text) <= max_tokens:
        return [text]

    # Try splitting by double newline (paragraph)
    paragraphs = re.split(r"\n\n+", text)
    if len(paragraphs) > 1:
        return _merge_splits(paragraphs, max_tokens, overlap_tokens, "\n\n")

    # Try splitting by single newline
    lines = text.split("\n")
    if len(lines) > 1:
        return _merge_splits(lines, max_tokens, overlap_tokens, "\n")

    # Last resort: split by words
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i : i + max_tokens]
        chunks.append(" ".join(chunk_words))
        i += max(1, max_tokens - overlap_tokens)
    return chunks


def _merge_splits(
    parts: list[str], max_tokens: int, overlap_tokens: int, separator: str
) -> list[str]:
    """Merge split parts back together up to max_tokens, with overlap."""
    chunks = []
    current_parts: list[str] = []
    current_tokens = 0

    for part in parts:
        part_tokens = _estimate_tokens(part)
        if current_tokens + part_tokens > max_tokens and current_parts:
            chunks.append(separator.join(current_parts))
            # Overlap: keep last parts that fit within overlap_tokens
            overlap_parts: list[str] = []
            overlap_count = 0
            for p in reversed(current_parts):
                pt = _estimate_tokens(p)
                if overlap_count + pt > overlap_tokens:
                    break
                overlap_parts.insert(0, p)
                overlap_count += pt
            current_parts = overlap_parts
            current_tokens = overlap_count

        current_parts.append(part)
        current_tokens += part_tokens

    if current_parts:
        chunks.append(separator.join(current_parts))

    return chunks


def _protect_atomic_blocks(text: str) -> tuple[str, dict[str, str]]:
    """Replace fenced code blocks and tables with placeholders to prevent splitting them.

    Placeholders preserve the original newline count so that line-based metadata
    (line_start/line_end) remains accurate for content after the block.
    """
    placeholders: dict[str, str] = {}
    counter = 0

    # Protect fenced code blocks
    def replace_fence(match: re.Match) -> str:
        nonlocal counter
        key = f"__ATOMIC_BLOCK_{counter}__"
        placeholders[key] = match.group(0)
        counter += 1
        # Pad with the same number of newlines as the original block minus the key line
        newline_count = match.group(0).count("\n")
        return key + "\n" * newline_count

    text = re.sub(r"```[\s\S]*?```", replace_fence, text)

    # Protect tables (consecutive lines starting with |)
    def replace_table(match: re.Match) -> str:
        nonlocal counter
        key = f"__ATOMIC_BLOCK_{counter}__"
        placeholders[key] = match.group(0)
        counter += 1
        newline_count = match.group(0).count("\n")
        return key + "\n" * newline_count

    text = re.sub(r"(?:^\|.*\|$\n?){2,}", replace_table, text, flags=re.MULTILINE)

    return text, placeholders


def _restore_atomic_blocks(text: str, placeholders: dict[str, str]) -> str:
    """Restore atomic blocks from placeholders, stripping the newline padding."""
    for key, value in placeholders.items():
        newline_count = value.count("\n")
        text = text.replace(key + "\n" * newline_count, value)
    return text


def chunk_markdown(
    text: str,
    max_tokens: int = 512,
    overlap_tokens: int = 256,
    split_headers: list[str] | None = None,
    file_path: str = "",
    reading_order_map: dict[str, int] | None = None,
) -> list[ChunkResult]:
    """Chunk a markdown document by headers, keeping tables and code blocks atomic.

    Args:
        text: Full markdown document text
        max_tokens: Maximum tokens per chunk
        overlap_tokens: Overlap between consecutive chunks
        split_headers: Header levels to split on (default: h1, h2, h3)
        file_path: Source file path for reading_order lookup
        reading_order_map: Mapping of file_path -> reading_order position
    """
    if not text.strip():
        return []

    if split_headers is None:
        split_headers = ["h1", "h2", "h3"]

    reading_order = None
    if reading_order_map and file_path:
        reading_order = reading_order_map.get(file_path)

    # Protect atomic blocks before splitting
    protected_text, placeholders = _protect_atomic_blocks(text)

    sections = _split_into_sections(protected_text, split_headers)
    chunks: list[ChunkResult] = []

    for section in sections:
        content = _restore_atomic_blocks(section["content"], placeholders)
        header = section["header_hierarchy"] or section["header"]
        tokens = _estimate_tokens(content)

        if tokens <= max_tokens:
            chunks.append(ChunkResult(
                content=content.strip(),
                section_header=header,
                start_line=section["start_line"],
                end_line=section["end_line"],
                token_count=tokens,
                reading_order=reading_order,
            ))
        else:
            # Recursive split for oversized sections
            sub_chunks = _recursive_split(content, max_tokens, overlap_tokens)
            lines = content.split("\n")
            line_offset = section["start_line"]
            char_pos = 0
            for sub in sub_chunks:
                sub_restored = _restore_atomic_blocks(sub, placeholders)
                sub_lines = sub_restored.count("\n") + 1
                start = line_offset
                end = start + sub_lines - 1
                chunks.append(ChunkResult(
                    content=sub_restored.strip(),
                    section_header=header,
                    start_line=start,
                    end_line=min(end, section["end_line"]),
                    token_count=_estimate_tokens(sub_restored),
                    reading_order=reading_order,
                ))
                line_offset = end + 1

    return chunks


def extract_reading_order(docs_readme_path: str) -> dict[str, int]:
    """Parse docs/README.md 'Reading Order by Task' to build {file_path: position} map."""
    try:
        with open(docs_readme_path) as f:
            content = f.read()
    except FileNotFoundError:
        return {}

    order_map: dict[str, int] = {}
    in_section = False
    position = 0

    for line in content.split("\n"):
        if "Reading Order by Task" in line:
            in_section = True
            continue
        if in_section and line.startswith("#"):
            break
        if in_section:
            # Extract file paths from backtick references
            paths = re.findall(r"`([^`]+\.md)`", line)
            for path in paths:
                position += 1
                # Normalize: ensure docs/ prefix
                if not path.startswith("docs/"):
                    path = f"docs/{path}"
                order_map[path] = position

    return order_map
