#!/bin/bash
# Documentation Sync Check Hook
# Triggered on PostToolUse for Edit/Write operations
# Checks if modified files affect skills/references/templates/agents
# and reminds to update DESIGN-GUIDELINES.md and README.md

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only check Edit and Write tool operations
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Skip if the file being edited IS a doc file (avoid infinite loop)
if [[ "$FILE_PATH" == *"DESIGN-GUIDELINES.md" || "$FILE_PATH" == *"README.md" ]]; then
  exit 0
fi

# Check if the modified file matches documentation-affecting patterns
NEEDS_SYNC=false
AFFECTED=""

case "$FILE_PATH" in
  */skills/*/SKILL.md)
    NEEDS_SYNC=true
    AFFECTED="skill definition"
    ;;
  */skills/*/references/*.md)
    NEEDS_SYNC=true
    AFFECTED="reference file"
    ;;
  */skills/*/assets/templates/*.md)
    NEEDS_SYNC=true
    AFFECTED="output template"
    ;;
  */agents/*.md)
    NEEDS_SYNC=true
    AFFECTED="subagent definition"
    ;;
  */.claude/rules/*.md)
    NEEDS_SYNC=true
    AFFECTED="rule definition"
    ;;
esac

if [[ "$NEEDS_SYNC" == "true" ]]; then
  # Check if docs are potentially stale by comparing modification times
  DESIGN_GUIDELINES="DESIGN-GUIDELINES.md"
  README="README.md"

  STALE_DOCS=""
  if [[ -f "$DESIGN_GUIDELINES" ]]; then
    STALE_DOCS="DESIGN-GUIDELINES.md"
  fi
  if [[ -f "$README" ]]; then
    if [[ -n "$STALE_DOCS" ]]; then
      STALE_DOCS="$STALE_DOCS and README.md"
    else
      STALE_DOCS="README.md"
    fi
  fi

  if [[ -n "$STALE_DOCS" ]]; then
    echo "Documentation sync: A $AFFECTED was modified. Verify $STALE_DOCS still reflects current state."
  fi
fi

# Exit 0 intentional: this is a PostToolUse hook. PostToolUse is non-blocking — exit 2 has no effect.
# The hook's purpose is notification only; blocking execution would be incorrect here.
exit 0
