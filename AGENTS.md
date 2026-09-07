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
  - `feat: add schema browser filter (#2)`
  - `fix: handle null column names in DDL (#3)`
  - `chore: add mocha setup (#3)`
- One logical change per commit; do not batch unrelated changes.
- **Push after every commit:** run `git push` immediately after `git commit`. CI runs on push — commits that are not pushed are invisible to CI and to the architect.

## Codex-only rules

Implementation retries and output format for delegated Codex runs live in
[CODEX.md](CODEX.md); `codex-run.sh` injects that file into the delegation
prompt. Claude sessions do not load it.

## VS Code API conventions

_Project-specific VS Code API gotchas go here._

## Debugging

- `git log` — check recent changes first
- On compile error: fix root cause; never skip `--noEmit` or loosen `tsconfig` without asking
- **CI/API acting up for no reason → check https://www.githubstatus.com before debugging locally.** Symptom pattern: `gh api`/Actions calls return an HTML "Unicorn" 503 page instead of JSON, workflow steps that call the GitHub API (e.g. `release-please-action`) fail in ~10s with that same HTML in the error, and it's inconsistent across endpoints (some `gh` commands work, others don't) — none of that is a local config, token, or workflow-file problem; it's GitHub-side. Confirm via the status page, then just wait and retry — don't chase phantom fixes (rotating tokens, editing workflow YAML, etc.) for an incident that isn't yours to fix.

## Meta

- Repeated instruction → suggest rule
- Commit rules separately from code
- Do not narrate setup steps (loading rules, fetching issues, reading files) — only report if something fails or is missing
