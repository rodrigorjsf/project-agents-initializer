#!/usr/bin/env bash
set -euo pipefail

STATE_MARKER="<!-- copilot-review-fix-loop -->"

log() {
  echo "[copilot-review-fix-loop] $*"
}

warn() {
  echo "::warning::$*"
}

fail() {
  echo "::error::$*"
  exit 1
}

summary_line() {
  if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
    printf '%s\n' "$1" >>"$GITHUB_STEP_SUMMARY"
  fi
}

single_line() {
  tr '\n' ' ' <<<"$1" | sed 's/[[:space:]]\+/ /g'
}

read_state_field() {
  local body="$1"
  local field="$2"

  awk -F': ' -v key="$field" '$1 == key { print substr($0, length($1) + 3) }' <<<"$body" | head -n1
}

resolve_copilot_bin() {
  local workspace_dir
  local local_bin

  if [[ -n "${COPILOT_BIN:-}" ]]; then
    if [[ "$COPILOT_BIN" == */* ]]; then
      [[ -x "$COPILOT_BIN" ]] || fail "Configured COPILOT_BIN is not executable: $COPILOT_BIN"
      return
    fi

    command -v "$COPILOT_BIN" >/dev/null 2>&1 || fail "Configured COPILOT_BIN is not available on PATH: $COPILOT_BIN"
    return
  fi

  workspace_dir="${GITHUB_WORKSPACE:-$(pwd)}"
  local_bin="$workspace_dir/.github/copilot-review-fix-loop/node_modules/.bin/copilot"

  if [[ -x "$local_bin" ]]; then
    COPILOT_BIN="$local_bin"
    return
  fi

  COPILOT_BIN=$(command -v copilot || true)
  [[ -n "$COPILOT_BIN" ]] || fail "GitHub Copilot CLI is not installed. Expected cached dependency at .github/copilot-review-fix-loop or copilot on PATH."
}

is_copilot_review() {
  local login="${1,,}"
  [[ -n "$login" && "$login" == *copilot* ]]
}

load_state() {
  local state_json

  state_json=$(
    gh api "repos/$REPO/issues/$PR/comments?per_page=100" --paginate |
      jq -sc --arg marker "$STATE_MARKER" 'add | map(select(.body | contains($marker))) | sort_by(.updated_at) | last // {}'
  )

  STATE_COMMENT_ID=$(jq -r '.id // empty' <<<"$state_json")
  STATE_BODY=$(jq -r '.body // empty' <<<"$state_json")
  CURRENT_ITERATION=$(read_state_field "$STATE_BODY" "iteration")
  LAST_REVIEW_ID=$(read_state_field "$STATE_BODY" "last_review_id")

  [[ -n "$CURRENT_ITERATION" ]] || CURRENT_ITERATION=0
  [[ -n "$LAST_REVIEW_ID" ]] || LAST_REVIEW_ID=0
}

upsert_state() {
  local status="$1"
  local iteration="$2"
  local review_id="$3"
  local head_sha="$4"
  local message="$5"
  local body

  body=$(
    cat <<EOF
$STATE_MARKER
status: $status
iteration: $iteration
max_iterations: $MAX_ITERATIONS
last_review_id: $review_id
head_sha: $head_sha
updated_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
summary: $(single_line "$message")
EOF
  )

  if [[ -n "$STATE_COMMENT_ID" ]]; then
    gh api -X PATCH "repos/$REPO/issues/comments/$STATE_COMMENT_ID" -f body="$body" >/dev/null
    return
  fi

  STATE_COMMENT_ID=$(
    gh api -X POST "repos/$REPO/issues/$PR/comments" -f body="$body" --jq '.id'
  )
}

resolve_manual_pr() {
  local pr_json

  [[ -n "${WORKFLOW_PR_NUMBER:-}" ]] || fail "workflow_dispatch requires WORKFLOW_PR_NUMBER."
  PR="$WORKFLOW_PR_NUMBER"

  pr_json=$(gh api "repos/$REPO/pulls/$PR")
  HEAD_REF=$(jq -r '.head.ref // empty' <<<"$pr_json")
  HEAD_SHA=$(jq -r '.head.sha // empty' <<<"$pr_json")
  HEAD_REPO=$(jq -r '.head.repo.full_name // empty' <<<"$pr_json")

  [[ -n "$HEAD_REF" && -n "$HEAD_REPO" ]] || fail "Unable to resolve PR #$PR branch details."
}

resolve_event_pr() {
  PR=$(jq -r '.pull_request.number // empty' "$GITHUB_EVENT_PATH")
  REVIEW_ID=$(jq -r '.review.id // empty' "$GITHUB_EVENT_PATH")
  REVIEW_LOGIN=$(jq -r '.review.user.login // empty' "$GITHUB_EVENT_PATH")
  HEAD_REF=$(jq -r '.pull_request.head.ref // empty' "$GITHUB_EVENT_PATH")
  HEAD_SHA=$(jq -r '.pull_request.head.sha // empty' "$GITHUB_EVENT_PATH")
  HEAD_REPO=$(jq -r '.pull_request.head.repo.full_name // empty' "$GITHUB_EVENT_PATH")

  [[ -n "$PR" && -n "$HEAD_REF" && -n "$HEAD_REPO" ]] || fail "Unable to resolve pull_request_review payload."
}

resolve_manual_review() {
  local reviews_json

  if [[ -n "${WORKFLOW_REVIEW_ID:-}" && ! "${WORKFLOW_REVIEW_ID}" =~ ^[0-9]+$ ]]; then
    fail "WORKFLOW_REVIEW_ID must be numeric."
  fi

  reviews_json=$(
    gh api "repos/$REPO/pulls/$PR/reviews?per_page=100" --paginate |
      jq -sc 'add'
  )

  if [[ -n "${WORKFLOW_REVIEW_ID:-}" ]]; then
    REVIEW_ID="$WORKFLOW_REVIEW_ID"
    REVIEW_LOGIN=$(
      jq -r --argjson review_id "$REVIEW_ID" '.[] | select(.id == $review_id) | .user.login // empty' <<<"$reviews_json" | head -n1
    )
    return
  fi

  REVIEW_ID=$(
    jq -r --argjson last_review_id "$LAST_REVIEW_ID" '
      [ .[] | select(.id > $last_review_id) | select((.user.login // "" | ascii_downcase | contains("copilot"))) ]
      | sort_by(.submitted_at // .id)
      | last
      | .id // empty
    ' <<<"$reviews_json"
  )

  REVIEW_LOGIN=$(
    jq -r --argjson review_id "$REVIEW_ID" '.[] | select(.id == $review_id) | .user.login // empty' <<<"$reviews_json" | head -n1
  )
}

count_review_comments() {
  REVIEW_COMMENT_COUNT=$(
    gh api "repos/$REPO/pulls/$PR/reviews/$REVIEW_ID/comments?per_page=100" --paginate |
      jq -sc 'add | length'
  )
}

fail_on_uncommitted_changes() {
  if [[ -z "$(git status --porcelain)" ]]; then
    return
  fi

  git status --short
  fail "Copilot left uncommitted changes. receiving-code-review must create its own atomic commits."
}

run_copilot() {
  local prompt
  local skill_argument="${PR}:${REVIEW_ID}"
  local -a command=(
    "$COPILOT_BIN"
    -p
    ""
    -s
    --autopilot
    --max-autopilot-continues=12
    --no-ask-user
    --allow-tool=shell,write
    --allow-all-paths
  )

  prompt=$(
    cat <<EOF
Use the /receiving-code-review skill with argument ${skill_argument}.

Context:
- GitHub Actions non-interactive run.
- Repository: ${REPO}
- Pull request: #${PR}
- Review id: ${REVIEW_ID}
- Current loop iteration: ${CURRENT_ITERATION} of max ${MAX_ITERATIONS}
- Work only in the current checkout of PR branch ${HEAD_REF}

Execution rules:
- Scope your analysis to review ${REVIEW_ID}; do not reprocess older reviews.
- Apply only technically sound fixes for actionable review comments.
- If a comment needs human judgment in this non-interactive run, skip it with a factual reason instead of waiting for clarification.
- If the pr-comment-resolver agent is unavailable, perform its reply and thread-resolution work inline.
- If you make changes, create local git commit(s) that follow the repository commit conventions.
- Do not push; the workflow will push after you finish.
- Leave the working tree clean when you exit.
EOF
  )

  command[2]="$prompt"

  if [[ -n "$MODEL" ]]; then
    command+=(--model "$MODEL")
  fi

  "${command[@]}"
}

main() {
  REPO="${GITHUB_REPOSITORY:?Missing GITHUB_REPOSITORY.}"
  MODEL="${WORKFLOW_MODEL:-${REPO_DEFAULT_MODEL:-}}"
  MAX_ITERATIONS="${WORKFLOW_MAX_ITERATIONS:-${REPO_DEFAULT_MAX_ITERATIONS:-5}}"
  GITHUB_EVENT_NAME="${GITHUB_EVENT_NAME:?Missing GITHUB_EVENT_NAME.}"
  GITHUB_EVENT_PATH="${GITHUB_EVENT_PATH:?Missing GITHUB_EVENT_PATH.}"

  [[ "$MAX_ITERATIONS" =~ ^[0-9]+$ ]] || fail "MAX_ITERATIONS must be numeric."
  resolve_copilot_bin

  if [[ "$GITHUB_EVENT_NAME" == "workflow_dispatch" ]]; then
    resolve_manual_pr
  else
    resolve_event_pr
  fi

  if [[ "$HEAD_REPO" != "$REPO" ]]; then
    log "Skipping PR #$PR from forked repository $HEAD_REPO."
    summary_line "- Skipped fork PR #$PR from $HEAD_REPO."
    exit 0
  fi

  load_state

  if [[ "$GITHUB_EVENT_NAME" == "workflow_dispatch" ]]; then
    resolve_manual_review
  fi

  if [[ -z "$REVIEW_ID" ]]; then
    if [[ "$GITHUB_EVENT_NAME" == "workflow_dispatch" ]]; then
      log "No new Copilot review found for PR #$PR."
      summary_line "- No new Copilot review found for PR #$PR."
      exit 0
    fi

    fail "Unable to determine a Copilot review to process."
  fi

  if ! is_copilot_review "${REVIEW_LOGIN:-}"; then
    log "Skipping non-Copilot review $REVIEW_ID by ${REVIEW_LOGIN:-unknown reviewer}."
    summary_line "- Skipped non-Copilot review $REVIEW_ID."
    exit 0
  fi

  if [[ -z "${WORKFLOW_REVIEW_ID:-}" ]] && (( REVIEW_ID <= LAST_REVIEW_ID )); then
    log "Review $REVIEW_ID already processed."
    summary_line "- Review $REVIEW_ID already processed."
    exit 0
  fi

  count_review_comments

  if (( REVIEW_COMMENT_COUNT == 0 )); then
    log "Copilot review $REVIEW_ID has no inline comments."
    upsert_state "no-comments" "$CURRENT_ITERATION" "$REVIEW_ID" "$HEAD_SHA" "Copilot review $REVIEW_ID had no inline comments."
    summary_line "- Copilot review $REVIEW_ID had no inline comments."
    exit 0
  fi

  if (( CURRENT_ITERATION >= MAX_ITERATIONS )); then
    warn "Max iterations reached for PR #$PR."
    upsert_state "maxed" "$CURRENT_ITERATION" "$LAST_REVIEW_ID" "$HEAD_SHA" "Skipped Copilot review $REVIEW_ID because max iterations ($MAX_ITERATIONS) was reached."
    summary_line "- Max iterations reached for PR #$PR. Review $REVIEW_ID was not processed."
    exit 0
  fi

  INITIAL_HEAD=$(git rev-parse HEAD)

  log "Running Copilot CLI for PR #$PR review $REVIEW_ID."
  run_copilot
  fail_on_uncommitted_changes

  FINAL_HEAD=$(git rev-parse HEAD)

  if [[ "$FINAL_HEAD" == "$INITIAL_HEAD" ]]; then
    log "No new commits were created."
    upsert_state "noop" "$CURRENT_ITERATION" "$REVIEW_ID" "$HEAD_SHA" "Review $REVIEW_ID produced no changes."
    summary_line "- Review $REVIEW_ID produced no local commits."
    exit 0
  fi

  PUSHED_COMMITS=$(git rev-list --count "${INITIAL_HEAD}..${FINAL_HEAD}")
  git push origin "HEAD:${HEAD_REF}"

  NEW_ITERATION=$((CURRENT_ITERATION + 1))
  upsert_state "applied" "$NEW_ITERATION" "$REVIEW_ID" "$FINAL_HEAD" "Applied review $REVIEW_ID with $PUSHED_COMMITS new commit(s)."

  summary_line "## Copilot review fix loop"
  summary_line "- PR: #$PR"
  summary_line "- Review: $REVIEW_ID"
  summary_line "- Commits pushed: $PUSHED_COMMITS"
  summary_line "- Iteration: $NEW_ITERATION / $MAX_ITERATIONS"
}

main "$@"
