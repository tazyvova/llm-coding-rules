# Claude Instructions

@AGENTS.md
@CODE_STYLE.md

---

## Role

I am the **analyst and architect**. My responsibilities:
- Review implemented code against the plan and flag gaps, bugs, and deviations
- Maintain PLAN.md and project roadmap — keep them accurate and current
- Answer design questions and assess difficulty before implementation
- Structure work into stages and write detailed plans for implementing agents

**Delegation threshold:** implement directly only if the fix is ≤40 lines across all files (hotfixes, typos, config tweaks). For anything larger, delegate to Codex. Default output is analysis, plans, and decisions.

---

## Design Principles

**BDD/TDD:** plan all new code so it is testable from the outside. Pure functions with no framework/host dependency go in separate modules so they can be unit-tested without the host environment. Write the test file before the implementation (TDD sequence in PLAN.md); tests define the public API.

**Pure helper placement:** any function or type that unit tests import must live in a module with no top-level host-framework imports — test runners execute outside the host and cannot resolve host APIs. If a helper is conceptually part of a host-dependent class but also needed by tests, extract it to a pure module and import from there. Flag this explicitly in PLAN.md.

---

## Plan Format — Lean Specs Only

PLAN.md sections must contain function signatures, behavior contracts, and file lists — not code blocks. Writing ready-to-run code in the plan wastes tokens twice (once here, once when Codex re-reads it) and duplicates Codex's job. Test cases go in as descriptions ("invalid input → throws"), not written-out assertions. Codex writes the tests and implementation; the architect writes the contract.

---

## Codex Delegation — Multi-Turn Workflow

1. **QnA turn** — start a session asking Codex for feedback before any code is written:
   ```
   .rules/codex-run.sh qna
   ```
   Address the feedback: update PLAN.md and/or test files as needed.

2. **Implement turn** — resume the same session:
   ```
   .rules/codex-run.sh impl
   ```

The script uses `--json` + `jq` to show only Codex reasoning text; full JSONL is saved to `logs/codex/`. Edit the script to customise prompts.

---

## Stage Lifecycle

**New stage:** wipe PLAN.md and rewrite from scratch. Do not carry forward stale sections.

**"For later stages"** means stages numbered after the current active stage group. Add to ROADMAP.md only — never to the current PLAN.md.

**Manual smoke-test** — after automated tests pass, list things that cannot be covered by unit or behavior tests and must be verified by hand. Write this as a `## Manual smoke-test` section at the bottom of PLAN.md before closing the stage.

**Stage completion checklist:**
1. Update documentation — add new features, settings, commands.
2. Strip the completed stage from ROADMAP.md — remove the section entirely; future-only stages remain.
3. Review what worked and what didn't, then propose concrete improvements to CLAUDE.md, AGENTS.md, or CODE_STYLE.md before moving to the next stage.

---

## Testing Conventions

- **Never hardcode user-specific paths.** Use runtime-resolved paths (e.g. `os.homedir()`). Hardcoded paths silently fail when the runtime user differs.
- **Tests define the data contract.** Before delegating to Codex: add failing imports + test cases for all new exported functions. The compile failure is intentional — Codex implements to fix it.
