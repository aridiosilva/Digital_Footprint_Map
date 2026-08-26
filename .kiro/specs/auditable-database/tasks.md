# Tasks — F-02: Auditable SQLite Database

## Status: ✅ Implemented (v1.0.0)

---

- [x] 1. Define `SCHEMA` constant with `evidence` and `runs` DDL statements
  - `src/pegada/db.py`
  - Use `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS`

- [x] 2. Implement `Repository.__init__` with auto directory creation
  - Accept `str | Path`; store as `Path`
  - Call `path.parent.mkdir(parents=True, exist_ok=True)`

- [x] 3. Implement `Repository.connect()` returning `sqlite3.Connection`
  - Set `connection.row_factory = sqlite3.Row`

- [x] 4. Implement `Repository.init()` executing the schema script
  - Use `con.executescript(SCHEMA)` — idempotent

- [x] 5. Implement `Repository.upsert(item: Evidence)`
  - Serialise `authors` → `authors_json`, `identifiers` → `identifiers_json`
  - Use INSERT … ON CONFLICT DO UPDATE with `MAX(confidence, excluded.confidence)`
  - _Tests: `test_upsert_deduplicates`_

- [x] 6. Implement `Repository.all() → list[dict]`
  - Call `init()` before querying
  - ORDER BY `category, title`
  - Deserialise JSON fields back to list/dict
  - _Tests: `test_upsert_deduplicates` (verifies snippet update)_

- [x] 7. Write unit tests in `tests/test_db.py`
  - Use `tmp_path` fixture for isolation
  - `test_upsert_deduplicates`: upsert same fingerprint twice → 1 row, snippet updated
