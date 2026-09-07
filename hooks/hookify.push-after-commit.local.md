---
name: warn-push-after-commit
enabled: true
event: bash
pattern: git\s+commit
---

⚠️ **Push immediately after this commit.**

`git push` right after `git commit` — CI runs on push, and unpushed commits are
invisible to CI and to the architect.

Before pushing to a feature branch, check the PR is not already merged:
`python3 .rules/gh/gh_pr_view.py`. Rebase-merge rewrites SHAs, so `git log` will
not show the merge; pushing to a merged branch creates orphaned commits.
