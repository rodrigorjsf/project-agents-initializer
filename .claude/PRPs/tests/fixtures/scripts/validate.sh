#!/bin/bash
# VIOLATION 6: [PLANTED] No exit 2 path — validation failures are not blocking (hook never blocks execution)
# VIOLATION 7: [PLANTED] Incorrectly assumes PostToolUse hook can block (exit 2 is non-blocking on PostToolUse)

FILE_PATH="${1:-}"

if [[ -z "$FILE_PATH" ]]; then
  echo "No file path provided" >&2
  exit 0
fi

if [[ ! -f "$FILE_PATH" ]]; then
  echo "File not found: $FILE_PATH" >&2
  exit 0
fi

echo "Validated: $FILE_PATH"
exit 0
