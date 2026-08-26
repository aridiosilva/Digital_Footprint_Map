# Tasks — F-01: Evidence Model & Fingerprint

## Status: ✅ Implemented (v1.0.0)

All tasks below are complete. Listed for traceability and regression reference.

---

- [x] 1. Define `Evidence` dataclass with all fields and correct defaults
  - `src/pegada/models.py`
  - Use `@dataclass(slots=True)`
  - Use `field(default_factory=...)` for mutable defaults
  - _Tests: test_models.py_

- [x] 2. Implement `utc_now()` helper returning ISO 8601 UTC string
  - Module-level function to allow test monkeypatching
  - `datetime.now(UTC).isoformat(timespec="seconds")`

- [x] 3. Implement `fingerprint` as a `@property`
  - SHA-256 of `url.strip().lower() | title.strip().lower() | category`
  - Return 64-char hex digest
  - _Tests: `test_fingerprint_is_stable`_

- [x] 4. Implement `to_dict()` method
  - Use `dataclasses.asdict()` then inject `fingerprint`
  - _Tests: `test_to_dict_contains_fingerprint`_

- [x] 5. Write unit tests in `tests/test_models.py`
  - `test_fingerprint_is_stable`: same normalised inputs → same fingerprint
  - `test_to_dict_contains_fingerprint`: result has 64-char fingerprint key
