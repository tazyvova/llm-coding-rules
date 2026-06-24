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
  gh issue view <N> --json title,body,comments
  ```
  Do not ask for re-explanation of anything already in the issue body or its comments.
- Issue body format: AS IS → TO BE → Contracts → Files to Change → Test Cases
- **Never modify existing test files** unless the delegation prompt explicitly says so. Tests are written before delegation to define the contract — rewriting them defeats TDD.
- After changes: run `npm run compile && npm test`; report result and files changed only.

## Commits

- Message format: `type: description (#N)` where N is the issue number.
  - `feat: add cvsStatus type annotations (#2)`
  - `fix: handle empty rlog output (#3)`
  - `chore: add mocha setup (#3)`
- One logical change per commit; do not batch unrelated changes.
- **Push after every commit:** run `git push` immediately after `git commit`. CI runs on push — commits that are not pushed are invisible to CI and to the architect.

## Implementation Retries

If `npm run compile && npm test` fails after implementation:
1. Read the error carefully — fix root cause directly.
2. Never skip `--noEmit`, loosen `tsconfig`, or modify test files to make tests pass.
3. Retry up to **5 attempts** total.
4. After 5 failures: stop. Post a comment on the issue summarising what was tried and what the blocker is. Add label `blocked` to the issue. Wait for architect input.

## Output

- Full JSONL is saved to `logs/codex/` automatically by `codex-run.sh`.
- Final response is posted as a comment on the issue automatically by `codex-run.sh`.
- Final response format: list of files changed + compile/test result only (one short paragraph). Do not repeat the spec or describe every line changed.
- **No narration during work:** do not announce what you are about to do, do not explain each function or each file change, do not restate the plan mid-run. Emit output only when something fails or when reporting the final result.

## CVS client conventions

- **Use `spawn` not `execFile`/`execFileAsync` for commands with potentially large output** (`cvs -qn update`, `cvs log`, `cvs rlog`). `execFile` buffers all output before resolving — any fixed `maxBuffer` can be exceeded on large repos. Use `spawn` with incremental line collection (separate `outPartial`/`errPartial` buffers, flush on `close`); no ceiling required.
- **`.cvsignore` applies only to untracked files and new unchecked-out directories — never to tracked files.** P/U (Needs Patch), NM (Needs Merge), and C (Conflict) status entries are for files already tracked in CVS; CVS updates them regardless of `.cvsignore`. Filtering these through `.cvsignore` hides legitimate incoming changes. Only filter: `?` untracked entries, and new directory entries (trailing `/` in `cvs -qn update` output).
- **CVS/Entries revision `'0'` means locally added (scheduled for addition, never committed).** `cvs update -r <rev>` refuses to operate on a file whose Entries line has revision `'0'` — it treats it as "added independently" and aborts. When you need to advance such a file to a server revision, remove its `/filename/0/…` line from `CVS/Entries` first, then run the update; CVS will create a fresh Entries line at the correct revision.

## VS Code API conventions

- **`_open.mergeEditor` requires `input1.uri ≠ output`.** When the local file must be the Current (Left) side, do **not** pass `vscode.Uri.file(localPath)` as both `input1.uri` and `output` — VS Code cannot distinguish the snapshot from the live output and "Accept All Current" writes empty content. Use `CvsDiffProvider.localUri(workDir, filePath)` instead: it returns a virtual `cvs:` scheme URI that serves the file from disk, keeping `input1` and `output` as distinct URIs.

- **Brand-new server files (U lines) are invisible to `cvs status`.** `cvs status` only reports files already in local `CVS/Entries`. Files committed by others but never checked out locally appear in `cvs -qn update -d` output as `U` lines but are absent from `CVS/Entries` and thus silently omitted by `cvs status`. Track them separately (e.g. `_newServerFiles`) and re-inject them into the incoming group on every `refresh()` call; drop each entry when `fs.existsSync` confirms it has been checked out.

## Debugging

- `git log` — check recent changes first
- On compile error: fix root cause; never skip `--noEmit` or loosen `tsconfig` without asking

## Meta

- Repeated instruction → suggest rule
- Commit rules separately from code
- Do not narrate setup steps (loading rules, fetching issues, reading files) — only report if something fails or is missing
