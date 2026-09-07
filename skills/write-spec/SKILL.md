---
name: write-spec
description: Write or revise a GitHub issue body as a lean spec for Codex delegation — AS IS / TO BE / Contracts / Files to Change / Test Cases. Use when opening an issue, turning a request or bug into a delegable task, filling in a spec, or when a QnA round exposes gaps that need the issue body rewritten.
---

# Write a Lean Spec

The architect writes the **contract**; Codex writes the tests and the code.

## Hard rule: no code in the spec

Issue bodies contain function signatures, behavior contracts, and file lists —
**not code blocks**. Writing ready-to-run code in the spec wastes tokens twice
(once here, once when Codex re-reads it) and duplicates Codex's job. Test cases
go in as descriptions ("invalid input → throws"), not written-out assertions.

## Body structure

```
## AS IS
## TO BE
## Contracts  (signatures + behavior, no code)
## Files to Change
## Test Cases  (descriptions only)
## Manual smoke-test  (populated in PR description before merge)
```

- **AS IS** — current behavior, one paragraph. Name the file and function that
  holds the current behavior so Codex does not have to search.
- **TO BE** — desired behavior, observable from outside. If a user-visible
  string, setting, or command id changes, spell it out exactly.
- **Contracts** — one entry per new/changed exported symbol: signature, what it
  returns, what it throws, and how it handles empty/null/boundary input. Types
  count as contracts.
- **Files to Change** — every file, including test files and `package.json`
  contributions. If a file is new, say which module it belongs to.
- **Test Cases** — descriptions only, one line each. Cover empty, null,
  boundaries, and error paths.
- **Manual smoke-test** — leave as a stub in the issue; it is filled in on the
  PR description before merge.

## Testability is a spec constraint

Plan all new code so it is testable from the outside. Pure functions with no
VS Code / framework dependency go in separate modules so they can be unit-tested
without the host environment.

**Pure helper placement — state this explicitly in the issue.** Any function or
type that a unit test imports must live in a module with **no top-level
host-framework imports**. Test runners execute outside VS Code and cannot
resolve `vscode`. If a helper is conceptually part of a host-dependent class but
tests need it, the spec must say: extract it to a pure module and import from
there. Existing pure modules in this repo: `outputParser.ts`, `sqlGenerator.ts`,
`explainPlan.ts`, `terminatorInjector.ts`, `formatter.ts`, `aliasUtils.ts`,
`identifierUtils.ts`.

Anything touching DB2 catalog data goes through `catalogQueries.ts`; anything
running a query goes through `odbcClient.ts`. Say which one in Files to Change.

## Writing the issue

```bash
python3 .rules/gh/gh_issue_create.py --title "feat: <title>" --body-file /tmp/body.md
python3 .rules/gh/gh_issue_edit.py <N> --body-file /tmp/body.md
```

Assign every issue to a milestone. Future work gets a **new** issue on a future
milestone — never append future work to an issue in the active milestone.

## Sizing

If the whole change is ≤40 lines across all files (hotfix, typo, config tweak),
implement it directly instead of writing a spec. Everything larger gets an issue
and goes to Codex.

Next step after the spec exists: `tdd-stubs`, then `issue-to-pr`.
