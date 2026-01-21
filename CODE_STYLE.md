# Code Style

## General

- Catch exceptions only when there's a recovery strategy (fallback, retry, default value)
- No catch-and-reraise without logging — let errors bubble up
- Prefer explicit arguments over default parameter values
- Self-documenting code: good names > comments
- Comments should be short and simple; small functions need no docstrings
- Complete only what task requests — don't fix unrelated issues
- Leave `TODO` for legacy concerns or uncertain decisions
- Group 3+ related parameters into object/dict

## Imports

- All imports at top of file — no inline imports inside functions
- Exception: circular import avoidance (must add comment explaining why)

## Organization

- Check existing utils before creating new functions
- Modify existing code instead of adding similar new functions
- Inline single-use code — extract to function only if reused or part of public API
- Keep related functions in same module
- Functions >200 lines or deep nesting → suggest refactoring
- 3+ related functions → suggest separate module
- Magic constants → suggest moving to config file
- SQL statements → separate `.sql` files

## Refactoring

- Inline single-use wrapper functions
- Check for unused functions
- Check for duplicate implementations across files
- Consolidate similar functions into parameterized version if it doesn't increase nesting
- Suggest updating rule files if patterns emerged
- Run imports check before committing

## Testing

- Always suggest edge case tests (empty, null, boundaries, errors)

## Git

- Commit messages: short, focus on "why" not "what"
- Skip obvious actions (rename, delete, move) — git shows these
- Check all changes before creating commit message
- Suggest separate commits if changes are unrelated
