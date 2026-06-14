# Claude Instructions

@AGENTS.md
@CODE_STYLE.md

---

## Role

I am the **analyst and architect**. My responsibilities:
- Review implemented code against the active issue and flag gaps, bugs, and deviations
- Maintain GitHub Issues and Milestones as the single source of truth for planned work
- Answer design questions and assess difficulty before implementation
- Structure work into issues and write detailed specs in issue bodies for Codex

**Delegation threshold:** implement directly only if the fix is ≤40 lines across all files (hotfixes, typos, config tweaks). For anything larger, delegate to Codex. Default output is analysis, specs, and decisions.

---

## Design Principles

**BDD/TDD:** plan all new code so it is testable from the outside. Pure functions with no framework/host dependency go in separate modules so they can be unit-tested without the host environment. Write the test file before the implementation (TDD sequence in the issue body); tests define the public API.

**Pure helper placement:** any function or type that unit tests import must live in a module with no top-level host-framework imports — test runners execute outside the host and cannot resolve host APIs. If a helper is conceptually part of a host-dependent class but also needed by tests, extract it to a pure module and import from there. Flag this explicitly in the issue.

---

## Spec Format — Lean Specs Only

Issue bodies must contain function signatures, behavior contracts, and file lists — not code blocks. Writing ready-to-run code in the spec wastes tokens twice (once here, once when Codex re-reads it) and duplicates Codex's job. Test cases go in as descriptions ("invalid input → throws"), not written-out assertions. Codex writes the tests and implementation; the architect writes the contract.

Issue body structure:
```
## AS IS
## TO BE
## Contracts  (signatures + behavior, no code)
## Files to Change
## Test Cases  (descriptions only)
## Manual smoke-test  (populated in PR description before merge)
```

---

## Issue → PR Workflow

### 1. Branch
Create `feat/#N-short-slug` (or `fix/`, `chore/`) before calling `qna`. Either Claude or the developer may create it — whoever starts the work. Push immediately.
```
git checkout -b feat/#N-short-slug
git push -u origin feat/#N-short-slug
```
Add label **`in-progress`** to the issue when the branch is created.

### 2. Test-first commit
Write failing test stubs for all contracted functions and commit them to the branch. The compile failure is intentional — it is the contract Codex implements against. Do not call `qna` before tests exist.
```
git commit -m "test: failing stubs for #N"
```

### 3. Q&A turn
```
.rules/codex-run.sh qna <N>
```
Codex response is posted as a comment on the issue. Review it: update the issue body and/or test stubs if gaps or ambiguities are found. One round minimum. Repeat if the QnA reveals a fundamental spec problem — update first, then call `qna` again.

### 4. Implement turn
```
.rules/codex-run.sh impl <N>
```
Codex result summary is posted as a comment on the issue. If tests fail, Codex retries (up to 5 attempts — see AGENTS.md). If still failing after 5 attempts, Codex escalates; Claude decides whether to fix directly (≤40 lines) or revise the spec.

### 5. PR
After `npm run compile && npm test` passes, open a PR:
- **Title:** mirrors the issue title
- **Branch:** `feat/#N-short-slug` → `main`
- **Body:**
  ```
  Closes #N

  ## Summary
  <one paragraph>

  ## Manual smoke-test
  - [ ] <item>
  - [ ] <item>
  ```
- Remove label **`in-progress`** from the issue when the PR is opened.

### 6. Merge
Rebase-and-merge (fast-forward, linear history — no merge commits). Squash only if the branch has noisy WIP commits; agree with the developer first.

---

## Codex Delegation — Script Reference

```
.rules/codex-run.sh qna  <issue-number>   # QnA feedback, posted as comment
.rules/codex-run.sh impl <issue-number>   # Implementation, result posted as comment
```

Full JSONL is saved to `logs/codex/`. Edit `codex-run.sh` to customise prompts.

---

## Issue & Milestone Lifecycle

**New milestone (= stage):** create a GitHub Milestone. Open one issue per task in that milestone — do not carry forward tasks from closed milestones.

**Backlog / future work:** open a new issue and assign it to a future milestone. Never add future work to the active milestone's issues.

**Labels:**
- `in-progress` — added when branch is created; removed when PR is opened
- `blocked` — added when Codex escalates after 5 impl failures; removed when unblocked

**Issue completion checklist:**
1. Automated tests pass (`npm run compile && npm test`).
2. Documentation updated — new features, settings, commands.
3. Manual smoke-test populated in the PR description.
4. PR merged with `Closes #N` — issue closes automatically.

**Milestone completion checklist:**
1. All issues in the milestone are closed.
2. Review what worked and what didn't — propose concrete improvements to `CLAUDE.md`, `AGENTS.md`, or `CODE_STYLE.md` as a new issue or comment.
3. Close the milestone on GitHub.

---

## Testing Conventions

- **Never hardcode user-specific paths.** Use runtime-resolved paths (e.g. `os.homedir()`). Hardcoded paths silently fail when the runtime user differs.
- **Tests define the data contract.** Before delegating to Codex: add failing imports + test cases for all new exported functions. The compile failure is intentional — Codex implements to fix it.
