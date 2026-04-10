#!/bin/bash
# RAG Re-index Hook
# Triggered on PostToolUse for Edit/Create operations
# Re-indexes changed files in the RAG knowledge base

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only trigger on Edit and Create
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Create" ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Check if file matches configured source patterns
MATCHES=false
case "$FILE_PATH" in
  docs/*.md|docs/**/*.md)
    MATCHES=true
    ;;
  plugins/*.md|plugins/**/*.md)
    MATCHES=true
    ;;
  plugins/*.yaml|plugins/**/*.yaml)
    MATCHES=true
    ;;
  plugins/*.yml|plugins/**/*.yml)
    MATCHES=true
    ;;
  skills/*.md|skills/**/*.md)
    MATCHES=true
    ;;
  skills/*.yaml|skills/**/*.yaml)
    MATCHES=true
    ;;
  .claude/hooks/*.sh)
    MATCHES=true
    ;;
  plugins/**/*.py|plugins/**/*.sh)
    MATCHES=true
    ;;
esac

if [[ "$MATCHES" != "true" ]]; then
  exit 0
fi

# Skip if RAG is not initialized
if [[ ! -f ".rag/knowledge.db" ]]; then
  exit 0
fi

# Debounce: skip if another reindex is running
LOCK_FILE=".rag/reindex.lock"
DIRTY_FLAG=".rag/reindex.dirty"

if [[ -f "$LOCK_FILE" ]]; then
  touch "$DIRTY_FLAG"
  exit 0
fi

# Run reindex in background
(
  trap 'rm -f "$LOCK_FILE"' EXIT
  touch "$LOCK_FILE"

  uv run --project rag python -m rag index --config rag.config.yaml > .rag/reindex.log 2>&1

  # If dirty flag was set during our run, reindex again
  if [[ -f "$DIRTY_FLAG" ]]; then
    rm -f "$DIRTY_FLAG"
    uv run --project rag python -m rag index --config rag.config.yaml >> .rag/reindex.log 2>&1
  fi
) &

echo "🔄 RAG index updating for: $FILE_PATH"
exit 0
