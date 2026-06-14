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
  gh issue view <N> --json title,body,comments
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

## Implementation Retries

If `npm run compile && npm test` fails after implementation:
1. Read the error carefully — fix root cause directly.
2. Never skip `--noEmit`, loosen `tsconfig`, or modify test files to make tests pass.
3. Retry up to **5 attempts** total.
4. After 5 failures: stop. Post a comment on the issue summarising what was tried and what the blocker is. Add label `blocked` to the issue. Wait for architect input.

## Output

- Full JSONL is saved to `logs/codex/` automatically by `codex-run.sh`.
- Final response is posted as a comment on the issue automatically by `codex-run.sh`.
- Final response format: list of files changed + compile/test result only (one short paragraph). Do not repeat the spec or describe every line changed.

## Debugging

- `git log` — check recent changes first
- On compile error: fix root cause; never skip `--noEmit` or loosen `tsconfig` without asking

## Meta

- Repeated instruction → suggest rule
- Commit rules separately from code
- Respond with line count after loading
