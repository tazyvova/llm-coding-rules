---
name: issue-to-pr
description: Drive an issue from branch to merged PR — branch naming, the test-stub commit, codex-run.sh qna/impl turns, PR body format, conflict rebase, merge, and the in-progress/blocked label lifecycle. Use when starting work on an issue, delegating to Codex, opening or updating a PR, resolving a PR conflict, or closing out a milestone.
---

# Issue → PR

## 1. Branch

```bash
git checkout -b feat/#N-short-slug   # or fix/ or chore/
git push -u origin feat/#N-short-slug
```
Add label `in-progress` to the issue when the branch is created.

## 2. Test-first commit

Failing stubs for every contracted function, committed to the branch. The
compile failure is intentional. **Do not call `qna` before tests exist.** See
the `tdd-stubs` skill.

```bash
git commit -m "test: failing stubs for #N"
git push
```

## 3. Q&A turn

```bash
.rules/codex-run.sh qna <N>
```
Codex's response is posted as a comment on the issue. Review it; update the
issue body and/or the stubs if it exposes gaps. One round minimum. If the QnA
reveals a fundamental spec problem, fix the spec first, then call `qna` again.

## 4. Implement turn

```bash
.rules/codex-run.sh impl <N>
```
The script refuses to run if the branch is not based on current `origin/<default>`
— rebase first. It posts Codex's summary, then runs its own host-side
`npm run compile && npm test`; on failure it labels the issue `blocked` and
exits non-zero. Codex self-reports are not trusted.

If Codex escalates after 5 failed attempts, decide: fix directly (≤40 lines) or
revise the spec and re-delegate.

## 5. PR

After `npm run compile && npm test` passes locally:

- **Title:** mirrors the issue title
- **Base:** `main`
- **Body:**
  ```
  Closes #N

  ## Summary
  <one paragraph>

  ## Manual smoke-test
  - [ ] <item>
  - [ ] <item>
  ```
- **Pre-tick behavior-covered items.** Mark `[x]` any smoke-test item already
  covered by an automated test and name the test. This separates "needs manual
  verification" from "already proven by CI".
- Remove label `in-progress`.

```bash
python3 .rules/gh/gh_pr_create.py --title "feat: foo (#42)" --body-file /tmp/pr-body.md
```

## 6. Conflicts

```bash
git fetch origin main
git rebase origin/main
git push --force-with-lease
```
Commits already in main (same content, different SHA — normal after a squash
merge) are skipped automatically. Verify tests pass before force-pushing.

**Check PR state before any push to a feature branch:**
`python3 .rules/gh/gh_pr_view.py`. Rebase-merge rewrites SHAs, so `git log`
will not show that the PR merged; pushing to a merged branch creates orphaned
commits that must be cherry-picked to a new branch.

## 7. Merge

Rebase-and-merge — fast-forward, linear history, no merge commits. Squash only
for noisy WIP branches, and agree with the developer first. Head branches are
deleted automatically on merge; no cleanup needed.

## Labels

- `in-progress` — added when the branch is created, removed when the PR opens
- `blocked` — added when Codex escalates after 5 impl failures, removed when unblocked

Create a label before first use: `gh label create "name" --color "hex"`.

## Issue completion checklist

1. `npm run compile && npm test` pass.
2. Documentation updated — new features, settings, commands.
3. Manual smoke-test populated in the PR description.
4. PR merged with `Closes #N`.

## Milestone completion checklist

1. All issues in the milestone are closed.
2. Review what worked and what did not — propose concrete changes to `CLAUDE.md`,
   `AGENTS.md`, or `CODE_STYLE.md` as a new issue or comment.
3. Close the milestone on GitHub.

New milestone = new stage: one issue per task, never carried forward from a
closed milestone.

## gh wrappers

Prefer these over raw `gh` — plain-text output, native `--body-file`, no
permission-prompt edge cases.

| Command | Purpose |
|---|---|
| `python3 .rules/gh/gh_issue_view.py <N>` | title, state, labels, milestone, body, comments |
| `python3 .rules/gh/gh_issue_list.py --milestone "Stage 6" --state open` | compact issue table |
| `python3 .rules/gh/gh_issue_create.py --title T --body-file F` | create issue |
| `python3 .rules/gh/gh_issue_edit.py <N> --body-file F --add-label in-progress` | edit body/title/labels |
| `python3 .rules/gh/gh_issue_comment.py <N> --body-file F` | post comment |
| `python3 .rules/gh/gh_pr_view.py [N]` | PR number, title, state, URL (defaults to current branch) |
| `python3 .rules/gh/gh_pr_create.py --title T --body-file F` | create PR |

Fall back to raw `gh` only for what the wrappers do not cover (`gh label create`,
`gh pr merge`).

New executable scripts: `git add <file>` then
`git update-index --chmod=+x <file>` — plain `chmod +x` may need a session
restart to take effect.
