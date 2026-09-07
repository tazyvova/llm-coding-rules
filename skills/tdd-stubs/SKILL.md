---
name: tdd-stubs
description: Write the failing test stubs that define the contract before delegating an issue to Codex — pure-module placement, ODBC availability guard, no hardcoded paths, and the "test: failing stubs for #N" commit. Use after a spec is written and before calling codex-run.sh qna, or when a test file needs new failing cases to pin a contract.
---

# Failing Test Stubs

Tests are written **before** delegation and define the public API. The compile
failure is intentional — it is the contract Codex implements against. Codex is
forbidden from modifying existing test files, so whatever is written here is
what gets built.

## Sequence

1. Read the issue: `python3 .rules/gh/gh_issue_view.py <N>`
2. For every symbol in the issue's **Contracts** section, add a failing import
   and test cases to the matching test file under `src/test/`.
3. Compile — it must fail on the missing exports. That failure is the deliverable.
4. Commit and push:
   ```bash
   git commit -m "test: failing stubs for #N"
   git push
   ```
5. Only then call `.rules/codex-run.sh qna <N>`.

## Placement — the rule that breaks builds

A function or type that a unit test imports must live in a module with **no
top-level `vscode` (or other host-framework) import**. `npm test` runs mocha
outside VS Code; the `vscode` module does not resolve there, and the failure is
a module-load error, not an assertion failure.

- New pure logic → its own module, or an existing pure one: `outputParser.ts`,
  `sqlGenerator.ts`, `explainPlan.ts`, `terminatorInjector.ts`, `formatter.ts`,
  `aliasUtils.ts`, `identifierUtils.ts`.
- A helper that belongs to a webview panel or provider but is needed by tests →
  extract to a pure module; the host class imports it from there.
- If the spec did not call this out, fix the issue body before writing stubs.

## Test split

- `npm test` — unit tests, pure modules only. Guarded by
  `scripts/mocha-odbc-availability.cjs`, which **skips** the suite when ODBC is
  unavailable. A skipped suite is not a passing suite — check the count.
- `npm run test:behavior` — integration tests, require a live DB2 ODBC
  connection.

New stubs for pure logic go in the unit suite. Anything needing a real
connection goes in the behavior suite, never the unit suite.

Single file after compiling:
```bash
npx mocha --require ./scripts/mocha-odbc-availability.cjs 'out/test/<file>.test.js'
```

## Conventions

- **Never hardcode user-specific paths.** Use runtime-resolved paths
  (`os.homedir()`, `path.join`). Hardcoded paths silently pass for the author
  and fail for every other runtime user.
- **`npm test` runs compiled JS from `out/`.** A stale `out/` makes deleted or
  renamed tests keep passing. `rm -rf out` before trusting a test count.
- Cover empty, null, boundary, and error inputs — the issue's Test Cases section
  lists them; every listed case gets a stub.
- Do not write the implementation. Do not write assertions that pass against
  nothing.

## Handing off

After the stubs are pushed, the branch is ready for `qna`. See `issue-to-pr`.
