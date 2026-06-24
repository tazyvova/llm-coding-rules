# llm-coding-rules

Shared coding rules and guidelines for AI coding assistants.

## Files

- `CODE_STYLE.md` — Universal coding standards
- `AGENTS.md` — AI-specific behavior rules (AGENTS.md standard)
- `CLAUDE.md` — Claude Code entry point
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
