@echo off
:: Creates symlinks to .rules\ submodule files
:: Run as Administrator

mklink CLAUDE.md .rules\CLAUDE.md
mklink AGENTS.md .rules\AGENTS.md
mklink CODE_STYLE.md .rules\CODE_STYLE.md

:: Skills are discovered from .claude\skills; keep the single source in .rules\.
if not exist .claude mkdir .claude
mklink /D .claude\skills ..\.rules\skills

:: Hookify reads .claude\hookify.*.local.md; keep the single source in .rules\hooks\.
for %%f in (.rules\hooks\hookify.*.local.md) do mklink .claude\%%~nxf ..\.rules\hooks\%%~nxf

echo Symlinks created
