# Agent Rules

@CODE_STYLE.md

See [CODE_STYLE.md](CODE_STYLE.md) for coding standards.

## Boundaries

**YOU MUST ask first:**
- Dependency updates
- Deleting files
- Schema/database changes

**NEVER do:**
- Commit secrets or credentials
- Modify `.env` files with real values
- Force push or rewrite git history

## Paths

**YOU MUST:**
- Use relative paths by default
- Use `git -C path` for submodules — not `cd`
- Stay within project folder only
- Access to other directories only after explicit agreement

## File Operations

**YOU MUST:**
- Use `git mv` for renaming/moving — not copy+delete

## Task Management

**Before starting work:**
1. Check `.tasks/TODO.md` for pending tasks

**When planning:**
- Use "AS IS / TO BE" format:
  - **AS IS** — current state
  - **TO BE** — desired state
  - **Files to Change** — list with brief description
- Save todos to `.tasks/TODO.md` (gitignored)
- Update after completing each step
- Follow TDD workflow if `TDD.md` exists in project root

## Debugging

**Before investigating issues:**
1. `git log` — check recent changes first

## Self-Improvement

- Instruction given twice → suggest adding to rules
- **Commit rules separately from code**

## Progress Reporting

- Show tokens via `/context` during long tasks

## Confirmation

After loading rules, respond with line count
