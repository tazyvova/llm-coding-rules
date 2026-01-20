# Agent Rules

See [CODE_STYLE.md](CODE_STYLE.md) for coding standards.

## Directory Restrictions

- Prefer relative paths over absolute paths
- Verify working directory before commands; use `cd` only if needed
- Stay within project folder only
- Access to other directories only after explicit agreement

## File Operations

- Use `git mv` for renaming/moving files — not copy+delete

## Task Management

- Check `.tasks/TODO.md` for pending tasks before starting new work
- After planning → save todos to `.tasks/TODO.md` (gitignored)
- Update after completing each step
- Follow TDD workflow if `TDD.md` exists in project root

## Debugging

- Check `git log` for recent changes before investigating issues

## Self-Improvement

- If an instruction is given twice → suggest adding it to rule files
- Commit rule file changes separately from code changes
