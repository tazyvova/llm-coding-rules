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

- Check `.tasks/TODO.md` before work
- Plan format: AS IS → TO BE → Files to Change
- Follow TDD if `TDD.md` exists

## Debugging

- `git log` — check recent changes first

## Meta

- Repeated instruction → suggest rule
- Commit rules separately from code
- Respond with line count after loading
