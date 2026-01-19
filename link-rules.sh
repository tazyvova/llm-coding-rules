#!/bin/bash
# Creates symlinks to .rules/ submodule files

ln -sf .rules/CLAUDE.md CLAUDE.md
ln -sf .rules/AGENT.md AGENT.md
ln -sf .rules/CODE_STYLE.md CODE_STYLE.md
ln -sf .rules/GEMINI.md GEMINI.md
ln -sf .rules/CODEX.md CODEX.md

echo "Symlinks created"
