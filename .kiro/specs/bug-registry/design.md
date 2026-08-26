# Design — BUG-REGISTRY: Bug Documentation Standard

## Artifacts

### `docs/bugs/BUG_REGISTRY.md`
Master index table. Updated manually by the developer who fixes or discovers
a bug. Lives in `docs/bugs/` alongside the individual reports.

### `docs/bugs/BUG-XXXXX.md`
One file per bug. Named with zero-padded 5-digit sequential ID.

---

## Bug Report Template Structure

```markdown
# BUG-XXXXX — [Short title]

| Field | Value |
|---|---|
| ID | BUG-XXXXX |
| Date found | YYYY-MM-DD |
| Date fixed | YYYY-MM-DD or — |
| Affected component | module name / feature ID |
| Severity | Critical / High / Medium / Low |
| Status | Open / Fixed / Verified / Wontfix |

## Description
[What the bug does to the user or system]

## Root Cause
[Why it happens — the technical explanation]

## Steps to Reproduce
1. ...

## Fix Applied
[Code change description]

## Tests Added
[Test names that cover this bug]

## Related PRs
- PR #N — [title]
```

---

## Severity Definitions

| Level | Definition |
|---|---|
| Critical | Data loss, security breach, or complete failure of a core feature |
| High | A feature is broken or produces incorrect results |
| Medium | A feature behaves incorrectly in an edge case |
| Low | Minor cosmetic or UX issue with a workaround |

---

## Registry Table Format

```markdown
| ID | Title | Component | Severity | Status | Fixed in |
|---|---|---|---|---|---|
| BUG-00001 | ... | ... | Medium | Verified | PR #7 |
```

---

## ID Assignment Rules

- Always use the next available sequential number
- Never reuse or skip IDs
- Counter is maintained by reading the last row of `BUG_REGISTRY.md`
