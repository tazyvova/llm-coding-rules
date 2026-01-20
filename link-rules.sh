#!/bin/bash
# Creates symlinks to .rules/ submodule files

ln -sf .rules/CLAUDE.md CLAUDE.md
ln -sf .rules/AGENTS.md AGENTS.md
ln -sf .rules/CODE_STYLE.md CODE_STYLE.md

echo "Symlinks created"
