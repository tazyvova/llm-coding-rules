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

## VS Code Extension

**No web-extension constraints** unless the project explicitly targets VS Code for the Web — confirm supported platforms before restricting use of `child_process`, `fs`, or `path`. Typical targets: VS Code desktop, Remote SSH, Dev Containers, Codespaces.

**SCM inline button order:** VS Code sorts `scm/resourceState/context` inline buttons alphabetically by command name, ignoring declaration order in `package.json`. Use `"group": "inline@N"` to enforce position — lower N = leftmost. Destructive actions (Discard/Revert) get `@1`; commit actions (Stage/Add/Unstage) get `@2`.

**Mirror commands across SCM and Explorer context menus.** When a project exposes both an `scm/resourceState/context` menu and an `explorer/context`-style menu for the same underlying commands, add every new file-acting command to both surfaces at the same time (same PR), not just the one you happened to be working in. Command icons only render when a menu item is shown as a button (title bar, inline group) — never in a dropdown/context-menu popup — so don't rely on icons for discoverability there; `when`-clause gating (e.g. hiding "Add" for already-tracked files) is the only way to keep a dropdown menu accurate per-item. If per-item dynamic gating by resource state is needed and the platform doesn't expose a built-in `when`-clause key for it, check whether a custom context key updated via `setContext`, combined with the `in`/`not in` membership operator against the specific resource's identifying key, is available before concluding it can't be done.

## Git

Before commit: `git diff`, check imports, message focused on "why"
- Skip obvious actions; separate commits for unrelated changes
