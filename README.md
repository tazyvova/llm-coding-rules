# llm-coding-rules

Shared coding rules and guidelines for AI coding assistants.

## Files

- `CODE_STYLE.md` — Universal coding standards
- `AGENTS.md` — AI-specific behavior rules (AGENTS.md standard)
- `CLAUDE.md` — Claude Code entry point

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
