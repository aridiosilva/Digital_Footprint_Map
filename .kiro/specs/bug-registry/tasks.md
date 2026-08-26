# Tasks — BUG-REGISTRY: Bug Documentation Standard

## Status: ✅ Implemented

---

- [x] 1. Create `docs/bugs/BUG_REGISTRY.md` with master index table
  - Header: ID | Title | Component | Severity | Status | Fixed in
  - Initial row: BUG-00001

- [x] 2. Create `docs/bugs/BUG-00001.md` — whitespace confidence parsing bug
  - Component: `src/pegada/importers.py` (F-0004)
  - Severity: Medium
  - Status: Verified
  - Describe: input `" "`, exception `ValueError`, root cause, fix, test reference

- [x] 3. Update `SPEC.md` to reference the bug registry
  - Add "Bug Registry" section pointing to `docs/bugs/BUG_REGISTRY.md`

