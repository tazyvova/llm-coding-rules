# Code Style

## General

- Catch exceptions only with recovery strategy; no catch-reraise without logging
- Explicit args over defaults; group 3+ params into dict
- Good names > comments; small functions need no docstrings
- Complete only requested task; `TODO` for legacy/uncertain

## Imports

- All imports at file top
- Inline only for circular deps (with comment)

## Organization

- Check utils before new functions; modify existing > add similar
- Inline single-use code; extract only if reused or public API
- Related functions same module; 3+ related → separate module
- >200 lines or deep nesting → refactor
- Magic constants → config; SQL → `.sql` files

## Refactoring

- Inline single-use wrappers; remove unused/duplicate
- Keep original order

## Testing

- Suggest edge cases: empty, null, boundaries, errors

## Git

Before commit: `git diff`, check imports, message focused on "why"
- Skip obvious actions; separate commits for unrelated changes
