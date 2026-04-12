#!/usr/bin/env bash
# Codex delegation helper — runs a QnA or implement turn and filters output.
#
# Usage:
#   .rules/codex-run.sh qna
#   .rules/codex-run.sh impl
#
# Full JSONL saved to logs/codex/; terminal shows only Codex reasoning text.

set -euo pipefail

MODE="${1:-}"
LOGDIR="logs/codex"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
FILTER='grep '"'"'^{'"'"' | jq -r '"'"'select(.type == "item.completed" and .item.type == "agent_message") | .item.text'"'"

mkdir -p "$LOGDIR"

case "$MODE" in
  qna)
    LOGFILE="$LOGDIR/${TIMESTAMP}-qna.jsonl"
    codex exec -s danger-full-access --json \
      "Read PLAN.md. Before writing any code: list ambiguities, missing cases, or concerns about the plan AND about the tests already written in src/test/. Do not touch any files yet." \
      2>&1 | tee "$LOGFILE" | eval "$FILTER"
    ;;
  impl)
    LOGFILE="$LOGDIR/${TIMESTAMP}-impl.jsonl"
    codex exec resume --last --dangerously-bypass-approvals-and-sandbox --json \
      "Plan and tests updated. Implement per PLAN.md — do not modify test files, only make them pass. Run npm run compile && npm test." \
      2>&1 | tee "$LOGFILE" | eval "$FILTER"
    ;;
  *)
    echo "Usage: $0 qna|impl" >&2
    exit 1
    ;;
esac
