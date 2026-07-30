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

## External processes (CLI tools, subprocesses)

**Non-empty output is not success.** Whenever stderr is merged into stdout — a `2>&1` redirect, or a `spawn` whose handler concatenates both streams — an error message *is* output. So `if (!output) throw` inverts into "any failure is a success": the tool prints a diagnostic, the guard sees a non-empty string, and a total failure is reported to the user as a silent no-op. Detect the tool's actual failure markers in the output, and prefer the exit code where the call style exposes one. Emptiness is the weakest possible signal and should never be the only check.

**A single bad argument can fail every other argument in the same call.** Do not assume a CLI applies itself per-argument and reports per-argument. Some tools abort the whole invocation on the first unusable argument, so batching N paths into one call means one bad path silently discards the other N-1 — and batching is often introduced precisely on the assumption that "this operation has no per-item branching". Verify that assumption against the real binary before batching, and check the abort behavior is not order-dependent (a bad argument last is not safer than first).

**When a batch does abort, the fix is usually structural, not "stop batching".** If arguments fail because of a missing prerequisite (a parent directory not yet fetched, a resource not yet created), the right shape is to satisfy the prerequisite as its own single command and let it cover its whole subtree, then batch what remains. That is normally *fewer* calls than the naive batch, not more — one recursive fetch of a parent replaces one failed call per leaf beneath it. Group work by the tree/dependency structure the tool actually operates on, deduplicating to the shallowest prerequisite so nested cases don't each get their own command.

**Log lines are for humans and may not reflect the real invocation.** A display string built by joining an argv array on spaces is not the command that ran — arguments containing spaces appear indistinguishable from separate arguments, which sends debugging after a quoting bug that does not exist. When a logged command is used as evidence, confirm the execution path (`spawn`/`execFile` with an array vs. a shell string) before trusting it, and prefer a display that quotes arguments needing it.

## VS Code Extension

**No web-extension constraints** unless the project explicitly targets VS Code for the Web — confirm supported platforms before restricting use of `child_process`, `fs`, or `path`. Typical targets: VS Code desktop, Remote SSH, Dev Containers, Codespaces.

**SCM inline button order:** VS Code sorts `scm/resourceState/context` inline buttons alphabetically by command name, ignoring declaration order in `package.json`. Use `"group": "inline@N"` to enforce position — lower N = leftmost. Destructive actions (Discard/Revert) get `@1`; commit actions (Stage/Add/Unstage) get `@2`.

**Mirror commands across SCM and Explorer context menus.** When a project exposes both an `scm/resourceState/context` menu and an `explorer/context`-style menu for the same underlying commands, add every new file-acting command to both surfaces at the same time (same PR), not just the one you happened to be working in. Command icons only render when a menu item is shown as a button (title bar, inline group) — never in a dropdown/context-menu popup — so don't rely on icons for discoverability there; `when`-clause gating (e.g. hiding "Add" for already-tracked files) is the only way to keep a dropdown menu accurate per-item. If per-item dynamic gating by resource state is needed and the platform doesn't expose a built-in `when`-clause key for it, check whether a custom context key updated via `setContext`, combined with the `in`/`not in` membership operator against the specific resource's identifying key, is available before concluding it can't be done.

## Git

Before commit: `git diff`, check imports, message focused on "why"
- Skip obvious actions; separate commits for unrelated changes
