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

- Read `PLAN.md` for the current stage spec — do not ask for re-explanation of anything already in PLAN.md
- Plan format: AS IS → TO BE → Files to Change
- **Never modify existing test files** unless the delegation prompt explicitly says so. Tests are written before delegation to define the contract — rewriting them defeats TDD.
- After changes: run `npm run compile && npm test`; report result and files changed only

## Output

- Log full implementation details to `logs/codex/session.txt` (append, not overwrite)
- Final response: list of files changed + compile/test result only (one short paragraph)
- Do not repeat the plan or describe every line changed

## Debugging

- `git log` — check recent changes first
- On compile error: fix root cause; never skip `--noEmit` or loosen `tsconfig` without asking

## Meta

- Repeated instruction → suggest rule
- Commit rules separately from code
- Respond with line count after loading
