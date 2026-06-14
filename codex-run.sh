#!/usr/bin/env bash
# Codex delegation helper — GitHub Issues edition.
#
# Usage:
#   .rules/codex-run.sh qna  <issue-number>
#   .rules/codex-run.sh impl <issue-number>
#
# QnA  — fetches the issue spec, asks Codex for feedback, posts the response
#         as a comment on the issue. No files are touched.
# Impl — resumes the same session, implements, posts the result summary as a
#         comment. Full JSONL saved to logs/codex/.
#
# Requires: gh (GitHub CLI), jq, codex

set -euo pipefail

MODE="${1:-}"
ISSUE="${2:-}"

if [[ -z "$MODE" || -z "$ISSUE" ]]; then
  echo "Usage: $0 qna|impl <issue-number>" >&2
  exit 1
fi

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
LOGDIR="logs/codex"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
FILTER='grep '"'"'^{'"'"' | jq -r '"'"'select(.type == "item.completed" and .item.type == "agent_message") | .item.text'"'"

mkdir -p "$LOGDIR"

# Fetch issue body + all existing comments so Codex sees the full discussion.
SPEC=$(gh issue view "$ISSUE" --repo "$REPO" --json title,body,comments -q '
  "# " + .title + "\n\n" + .body +
  (if (.comments | length) > 0 then
    "\n\n---\n## Discussion so far\n\n" +
    (.comments | map("**@" + .author.login + ":**\n" + .body) | join("\n\n"))
  else "" end)
')

post_comment() {
  local header="$1"
  local body_file="$2"
  if [[ -s "$body_file" ]]; then
    gh issue comment "$ISSUE" --repo "$REPO" \
      --body "### ${header}

$(cat "$body_file")"
  fi
}

case "$MODE" in
  qna)
    LOGFILE="$LOGDIR/${TIMESTAMP}-qna-issue${ISSUE}.jsonl"
    TMPOUT=$(mktemp)
    codex exec -s danger-full-access --json \
"GitHub Issue #${ISSUE} spec:

${SPEC}

Before writing any code: list ambiguities, missing cases, or concerns about \
the plan AND about any tests already written in src/test/. Do not touch any \
files yet." \
      2>&1 | tee "$LOGFILE" | eval "$FILTER" | tee "$TMPOUT"
    post_comment "Codex QnA — Issue #${ISSUE}" "$TMPOUT"
    rm -f "$TMPOUT"
    ;;

  impl)
    LOGFILE="$LOGDIR/${TIMESTAMP}-impl-issue${ISSUE}.jsonl"
    TMPOUT=$(mktemp)
    codex exec resume --last --dangerously-bypass-approvals-and-sandbox --json \
"Plan and tests updated. Implement per Issue #${ISSUE}. Do not modify test \
files — only make them pass. Run npm run compile && npm test." \
      2>&1 | tee "$LOGFILE" | eval "$FILTER" | tee "$TMPOUT"
    post_comment "Codex Implementation Result — Issue #${ISSUE}" "$TMPOUT"
    rm -f "$TMPOUT"
    ;;

  *)
    echo "Usage: $0 qna|impl <issue-number>" >&2
    exit 1
    ;;
esac
