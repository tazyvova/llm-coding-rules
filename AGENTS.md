# Agent Rules

@CODE_STYLE.md | [CODE_STYLE.md](CODE_STYLE.md)

## Boundaries

**Ask first:** dependency updates, file deletion, schema changes

**Never:** commit secrets, modify `.env` with real values, force push

## Paths & Files

- Relative paths default; `git -C` for submodules
- `git mv` for rename/move
- Stay within project; ask before accessing other dirs

## Tasks

- Read the assigned issue for the current task spec:
  ```
  python3 .rules/gh/gh_issue_view.py <N>
  ```
  Do not ask for re-explanation of anything already in the issue body or its comments.
- Issue body format: AS IS → TO BE → Contracts → Files to Change → Test Cases
- **Never modify existing test files** unless the delegation prompt explicitly says so. Tests are written before delegation to define the contract — rewriting them defeats TDD.
- After changes: run `npm run compile && npm test`; report result and files changed only.

## Commits

- Message format: `type: description (#N)` where N is the issue number.
  - `feat: add cvsStatus type annotations (#2)`
  - `fix: handle empty rlog output (#3)`
  - `chore: add mocha setup (#3)`
- One logical change per commit; do not batch unrelated changes.
- **Push after every commit:** run `git push` immediately after `git commit`. CI runs on push — commits that are not pushed are invisible to CI and to the architect.

## Implementation Retries

If `npm run compile && npm test` fails after implementation:
1. Read the error carefully — fix root cause directly.
2. Never skip `--noEmit`, loosen `tsconfig`, or modify test files to make tests pass.
3. Retry up to **5 attempts** total.
4. After 5 failures: stop. Post a comment on the issue summarising what was tried and what the blocker is. Add label `blocked` to the issue. Wait for architect input.

## Output

- Full JSONL is saved to `logs/codex/` automatically by `codex-run.sh`.
- Final response is posted as a comment on the issue automatically by `codex-run.sh`.
- Final response format: list of files changed + one-line compile/test summary (e.g. "118 tests passing"). Do **not** paste test output, mocha logs, or individual ✔ lines — the full log is already saved to `logs/codex/`. Do not repeat the spec or describe every line changed.
- **On test failure:** paste only the failing test block(s) — the test name, the error message, and the diff/actual vs expected. Omit all passing test lines. If a fix requires updating a test (e.g. the function signature changed), include the test name and the specific assertion that no longer holds, then explain the fix in one sentence.
- **No narration during work:** do not announce what you are about to do, do not explain each function or each file change, do not restate the plan mid-run. Emit output only when something fails or when reporting the final result.

## VS Code API conventions

_Project-specific VS Code API gotchas go here — add to this section on the project branch._

## Debugging

- `git log` — check recent changes first
- On compile error: fix root cause; never skip `--noEmit` or loosen `tsconfig` without asking

## Meta

- Repeated instruction → suggest rule
- Commit rules separately from code
- Do not narrate setup steps (loading rules, fetching issues, reading files) — only report if something fails or is missing
