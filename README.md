# llm-coding-rules

Shared coding rules and guidelines for AI coding assistants.

## Files

- `CODE_STYLE.md` — Universal coding standards
- `AGENTS.md` — AI-specific behavior rules (AGENTS.md standard)
- `CLAUDE.md` — Claude Code entry point
- `CODEX.md` — rules for Codex under `codex-run.sh`; injected into the delegation prompt, never loaded by Claude
- `skills/` — on-demand Claude Code skills (see below)
- `hooks/` — hookify rule files, symlinked into `.claude/` by `link-rules.sh`
- `gh/` — Python wrappers for the `gh` CLI (plain-text output, no JSON parsing needed)

## Usage

### Git Submodule

```bash
git submodule add https://github.com/tazyvova/llm-coding-rules .rules
```

Then create symlinks:

**Linux/Mac/Dev Containers:**
```bash
.rules/link-rules.sh
```

**Windows (run as Administrator):**
```bat
.rules\link-rules.bat
```

**Dev Container (devcontainer.json):**
```json
{
  "postCreateCommand": ".rules/link-rules.sh"
}
```

`link-rules.sh` also links `.claude/skills` → `.rules/skills` and each
`.rules/hooks/hookify.*.local.md` into `.claude/`, so skills and hook rules are
version-controlled here once instead of duplicated per repo. The `.claude/`
entries are generated — gitignore them in the consuming repo.

### Direct Copy

Copy the files you need to your project root.

## gh/ — Python GitHub CLI wrappers

Plain-text wrappers around `gh` for use in LLM agent workflows. No JSON parsing, no temp-file workarounds for multiline bodies.

| Script | Purpose |
|--------|---------|
| `gh/gh_issue_view.py <N>` | Print title, state, labels, milestone, body, and comments |
| `gh/gh_issue_list.py` | Compact table of issues (`--milestone`, `--label`, `--state`) |
| `gh/gh_issue_create.py` | Create issue; body from `--body-file` or stdin |
| `gh/gh_issue_edit.py <N>` | Update body/title/labels; body from `--body-file` or stdin |
| `gh/gh_issue_comment.py <N>` | Post a comment; body from `--body-file` or stdin |
| `gh/gh_pr_view.py [N]` | Print PR number, title, state, URL |
| `gh/gh_pr_create.py` | Create PR; body from `--body-file` or stdin |

All scripts: stdlib + subprocess only, `--repo owner/repo` optional (defaults to `git remote`), exit code mirrors `gh`.

**Usage example (when submoduled as `.rules/`):**
```bash
python3 .rules/gh/gh_issue_view.py 42
python3 .rules/gh/gh_issue_list.py --milestone "Stage 6" --state open
python3 .rules/gh/gh_issue_create.py --title "feat: foo" --body-file /tmp/body.md
python3 .rules/gh/gh_issue_edit.py 42 --body-file /tmp/body.md --add-label in-progress
python3 .rules/gh/gh_issue_comment.py 42 --body-file /tmp/comment.md
python3 .rules/gh/gh_pr_view.py
python3 .rules/gh/gh_pr_create.py --title "feat: foo (#42)" --body-file /tmp/pr-body.md
```

## skills/ — on-demand workflow skills

Workflow detail that is only relevant during one step is packaged as skills
instead of living in `CLAUDE.md`, where it would load into every session.

| Skill | Covers |
|-------|---------|
| `write-spec` | Lean spec format, AS IS/TO BE/Contracts template, pure-helper placement, issue sizing |
| `tdd-stubs` | Failing stubs from a spec's Contracts, pure-module placement, test-suite split, `test: failing stubs for #N` |
| `issue-to-pr` | Branch → stubs → qna → impl → PR → conflict → merge, gh wrappers, label and milestone lifecycle |

Discovery is via the `.claude/skills` symlink created by `link-rules.sh`. Adding
a skill = adding `skills/<name>/SKILL.md`; no per-repo wiring.

## hooks/ — hookify rules

Rules for the [hookify](https://github.com/anthropics/claude-plugins-official)
plugin, which reads `.claude/hookify.*.local.md` at every tool use.

| Rule | Event | Action |
|------|-------|--------|
| `warn-test-contract-edit` | Edit/Write under `src/test/*.ts` | warn — stubs are allowed, weakening a test to make an impl pass is not |
| `warn-push-after-commit` | Bash `git commit` | warn — push immediately; check the PR is not already merged |

Both warn rather than block: writing failing stubs is a legitimate edit to
`src/test/`, and only a human can tell that from an implementation-driven
rewrite. Codex runs outside Claude Code and is not covered by these hooks — its
equivalent rule lives in `CODEX.md`.
