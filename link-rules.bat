@echo off
:: Creates symlinks to .rules\ submodule files
:: Run as Administrator

mklink CLAUDE.md .rules\CLAUDE.md
mklink AGENTS.md .rules\AGENTS.md
mklink CODE_STYLE.md .rules\CODE_STYLE.md

echo Symlinks created
