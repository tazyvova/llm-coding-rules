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
- Assert the property that must hold, not the value that happens to hold now.
  Anything a tool or release process rewrites — versions, manifests, generated
  config — must be asserted by shape or by agreement with another file. A test
  pinning a literal current value passes when written and fails later, often
  blocking the process it guards.
- To assert an option is off, assert `=== false`, not absence. A missing key
  takes the library's default, which may be the opposite of the intent.

## VS Code Extension

**No web-extension constraints** unless the project explicitly targets VS Code for the Web — confirm supported platforms before restricting use of `child_process`, `fs`, or `path`. Typical targets: VS Code desktop, Remote SSH, Dev Containers, Codespaces.

**SCM inline button order:** VS Code sorts `scm/resourceState/context` inline buttons alphabetically by command name, ignoring declaration order in `package.json`. Use `"group": "inline@N"` to enforce position — lower N = leftmost. Destructive actions (Discard/Revert) get `@1`; commit actions (Stage/Add/Unstage) get `@2`.

## Git

Before commit: `git diff`, check imports, message focused on "why"
- Skip obvious actions; separate commits for unrelated changes
