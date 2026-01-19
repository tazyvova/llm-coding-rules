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

## Organization

- Check existing utils before creating new functions
- Modify existing code instead of adding similar new functions
- Keep related functions in same module
- Functions >200 lines or deep nesting → suggest refactoring
- 3+ related functions → suggest separate module
- Magic constants → suggest moving to config file
- SQL statements → separate `.sql` files

## Refactoring

- After refactoring → run imports check
- After refactoring → check and suggest list of unused functions
- After refactoring → suggest updating rule files if patterns emerged

## Testing

- Always suggest edge case tests (empty, null, boundaries, errors)

## Git

- Commit and PR messages: short and simple
