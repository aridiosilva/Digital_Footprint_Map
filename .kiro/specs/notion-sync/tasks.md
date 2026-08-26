# Tasks — F-07: Notion Sync

## Status: ✅ Implemented (v1.0.0)

---

- [x] 1. Define `REQUIRED_SCHEMA` constant with all 11 column name→type pairs
  - `src/pegada/notion_sync.py`

- [x] 2. Implement `SyncResult` frozen dataclass with `created`, `updated`, `skipped`, `total`

- [x] 3. Implement `_text(value, limit=2000)` helper
  - Returns Notion rich_text array; empty list for empty/None

- [x] 4. Implement `_properties(row)` building full Notion properties payload
  - All fields pass through `_text()` for truncation
  - `Autores` → `multi_select`; `Confiança` → `number`; `Coletado em` → `date`

- [x] 5. Implement `_resolve_data_source_id(client, explicit_id, database_id)`
  - Priority: explicit → auto-resolve → RuntimeError

- [x] 6. Implement `_validate_schema(client, data_source_id)`
  - Raise `RuntimeError` listing all mismatched columns

- [x] 7. Implement `_existing_pages(client, data_source_id) → dict[str, str]`
  - Paginate with cursor; build fingerprint→page_id map

- [x] 8. Implement `sync(rows, *, dry_run, client, data_source_id)`
  - Full flow: resolve → validate → existing → create/update loop
  - Return `SyncResult`

- [x] 9. Wire `sync` into CLI `notion-sync` command (`cmd_notion`)
  - Support `--dry-run` and `--only-reviewed` flags
  - Load `.env` before calling sync

- [x] 10. Write unit tests in `tests/test_notion_sync.py`
  - `test_properties_keep_urn_as_text`
  - `test_sync_creates_new_page`
  - `test_sync_updates_existing_page`
  - `test_dry_run_writes_nothing`
  - `test_schema_is_validated`
