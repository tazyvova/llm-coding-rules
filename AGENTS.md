# Agent Rules

@CODE_STYLE.md

See [CODE_STYLE.md](CODE_STYLE.md) for coding standards.

## Boundaries

⚠️ **Ask first:**
- Dependency updates
- Deleting files
- Schema/database changes

🚫 **Never:**
- Commit secrets or credentials
- Modify `.env` files with real values
- Force push or rewrite git history

## Directory Restrictions

- Use relative paths by default
- Ask before using `cd` or absolute paths — only if truly needed
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

## Progress Reporting

- Show tokens remaining during long tasks (use `/context` to check)

## Confirmation

After reading this file and full load [CODE_STYLE.md](CODE_STYLE.md), respond how many lines of rules are loaded
