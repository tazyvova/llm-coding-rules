# Code Style

## General

- No unnecessary `try-except` — let errors bubble up with stack trace
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
- After refactoring → suggest updating rule files if patterns emerged

## Testing

- Always suggest edge case tests (empty, null, boundaries, errors)

## Git

- Commit and PR messages: short and simple
