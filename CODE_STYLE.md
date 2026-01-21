# Code Style

## General

**YOU MUST:**
- Catch exceptions only when there's a recovery strategy (fallback, retry, default value)
- No catch-and-reraise without logging — let errors bubble up
- Prefer explicit arguments over default parameter values
- Self-documenting code: good names > comments
- Comments should be short and simple; small functions need no docstrings
- Complete only what task requests — don't fix unrelated issues
- Leave `TODO` for legacy concerns or uncertain decisions
- Group 3+ related parameters into object/dict

## Imports

**YOU MUST:**
- All imports at top of file — no inline imports inside functions
- Exception: circular import avoidance (must add comment explaining why)

## Organization

**YOU MUST:**
- Check existing utils before creating new functions
- Modify existing code instead of adding similar new functions
- Inline single-use code — extract to function only if reused or part of public API
- Keep related functions in same module
- Functions >200 lines or deep nesting → suggest refactoring
- 3+ related functions → suggest separate module
- Magic constants → suggest moving to config file
- SQL statements → separate `.sql` files

## Refactoring

**YOU MUST:**
- Inline single-use wrapper functions
- Check for unused functions
- Check for duplicate implementations across files
- Consolidate similar functions into parameterized version if it doesn't increase nesting
- Suggest updating rule files if patterns emerged
- Keep original order — don't reorder unless required

## Testing

**YOU MUST:**
- Always suggest edge case tests (empty, null, boundaries, errors)

## Git

**YOU MUST do this before every commit:**
1. `git diff` — review all changes
2. `python -c "from module import *"` — check imports
3. Write short message focused on "why"

- Skip obvious actions (rename, delete, move) — git shows these
- Suggest separate commits if changes are unrelated
