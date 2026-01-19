@echo off
:: Creates symlinks to .rules\ submodule files
:: Run as Administrator

mklink CLAUDE.md .rules\CLAUDE.md
mklink AGENT.md .rules\AGENT.md
mklink CODE_STYLE.md .rules\CODE_STYLE.md
mklink GEMINI.md .rules\GEMINI.md
mklink CODEX.md .rules\CODEX.md

echo Symlinks created
