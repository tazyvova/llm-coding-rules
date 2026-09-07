---
name: warn-test-contract-edit
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: src/test/.*\.ts$
---

⚠️ **Editing a test file — check which phase you are in.**

Tests define the contract and are written **before** delegation.

**Allowed:** writing new failing stubs for an issue's Contracts section
(`tdd-stubs` skill), then `git commit -m "test: failing stubs for #N" && git push`.

**Not allowed:** relaxing an assertion, deleting a case, or changing a signature
so an implementation passes. If the implementation cannot satisfy the test, the
spec is wrong — fix the issue body and re-delegate, do not edit the test.

Reminder: `npm test` runs compiled JS from `out/`. `rm -rf out` before trusting
a test count.
