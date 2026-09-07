#!/bin/bash
# Creates symlinks to .rules/ submodule files

ln -sf .rules/CLAUDE.md CLAUDE.md
ln -sf .rules/AGENTS.md AGENTS.md
ln -sf .rules/CODE_STYLE.md CODE_STYLE.md

# Skills are discovered from .claude/skills/; keep the single source in .rules/.
mkdir -p .claude
ln -sfn ../.rules/skills .claude/skills

# Hookify reads .claude/hookify.*.local.md; keep the single source in .rules/hooks/.
for hook in .rules/hooks/hookify.*.local.md; do
  [ -e "$hook" ] || continue
  ln -sf "../$hook" ".claude/$(basename "$hook")"
done

echo "Symlinks created"
