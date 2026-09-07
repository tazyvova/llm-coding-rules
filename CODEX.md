# Codex Rules

Rules that govern **Codex** running under `codex-run.sh`. Not applicable to
Claude sessions — `codex-run.sh` injects this file into the delegation prompt.

## Implementation Retries

If `npm run compile && npm test` fails after implementation:
1. Read the error carefully — fix root cause directly.
2. Never skip `--noEmit`, loosen `tsconfig`, or modify test files to make tests pass.
3. Retry up to **5 attempts** total.
4. After 5 failures: stop. Post a comment on the issue summarising what was tried
   and what the blocker is. Add label `blocked` to the issue. Wait for architect input.

## Output

- Full JSONL is saved to `logs/codex/` automatically by `codex-run.sh`.
- Final response is posted as a comment on the issue automatically by `codex-run.sh`.
- Final response format: list of files changed + one-line compile/test summary
  (e.g. "118 tests passing"). Do **not** paste test output, mocha logs, or
  individual ✔ lines — the full log is already saved to `logs/codex/`. Do not
  repeat the spec or describe every line changed.
- **On test failure:** paste only the failing test block(s) — the test name, the
  error message, and the diff/actual vs expected. Omit all passing test lines. If
  a fix requires updating a test (e.g. the function signature changed), include
  the test name and the specific assertion that no longer holds, then explain the
  fix in one sentence.
- **No narration during work:** do not announce what you are about to do, do not
  explain each function or each file change, do not restate the plan mid-run.
  Emit output only when something fails or when reporting the final result.
