# Design — F-0007: Notion Sync

## Component

`src/pegada/notion_sync.py`

---

## Public API

```python
sync(
    rows: list[dict],
    *,
    dry_run: bool = False,
    client: Any | None = None,        # injectable for testing
    data_source_id: str | None = None # injectable for testing
) → SyncResult
```

---

## Data Classes

```python
@dataclass(frozen=True, slots=True)
class SyncResult:
    created: int = 0
    updated: int = 0
    skipped: int = 0

    @property
    def total(self) -> int: ...
```

---

## Required Schema Constant

```python
REQUIRED_SCHEMA = {
    "Nome": "title", "URL": "rich_text", "Categoria": "select",
    "Fonte": "rich_text", "Confiança": "number", "Status": "select",
    "Fingerprint": "rich_text", "Trecho": "rich_text",
    "Autores": "multi_select", "Coletado em": "date", "Notas": "rich_text",
}
```

---

## Internal Functions

### `_text(value, limit=2000) → list[dict]`
Converts a value to a Notion rich_text array. Truncates to `limit` characters.
Returns `[]` for empty/None values.

### `_properties(row: dict) → dict`
Builds the full Notion properties payload from a row dict.
All field values pass through `_text()` for safe truncation.

### `_resolve_data_source_id(client, explicit_id, database_id) → str`
Priority: explicit_id → auto-resolve from database_id → RuntimeError.
If database has ≠ 1 data source, raises with instruction to set explicit ID.

### `_validate_schema(client, data_source_id) → None`
Calls `client.data_sources.retrieve()`. Compares against `REQUIRED_SCHEMA`.
Raises `RuntimeError` listing all mismatched columns.

### `_existing_pages(client, data_source_id) → dict[str, str]`
Paginates through all pages in the data source.
Returns `{fingerprint → page_id}` for all pages that have a non-empty Fingerprint property.

---

## sync() Execution Flow

```
1. Resolve client (env token or injected)
2. _resolve_data_source_id(...)
3. _validate_schema(...)         ← fails loudly if schema wrong
4. _existing_pages(...)          ← build fingerprint→page_id map
5. For each row:
   ├── dry_run=True  → count only, skip API calls
   └── dry_run=False →
       ├── fingerprint not in existing → client.pages.create(...)
       └── fingerprint in existing    → client.pages.update(page_id, ...)
6. Return SyncResult(created, updated)
```

---

## Testability

The `client` and `data_source_id` parameters make the sync fully testable
without network access. The test suite uses `FakeDataSources` and `FakePages`
objects (see `tests/test_notion_sync.py`).

---

## Dependencies

- `notion-client >=3.1,<4` (optional extra `[notion]`)
- `os`, `json`, `dataclasses` (stdlib)

---

## Design Decisions

| Decision | Rationale |
|---|---|
| Injectable `client` param | Enables unit testing without mocking `os.getenv` or `import` |
| Schema validation first | Fails before any writes — safe and loud |
| Pagination in `_existing_pages` | Data sources can have >100 pages; cursor loop handles all |
| `frozen=True` SyncResult | Result is read-only; prevents accidental mutation |
| Notion API version `2026-03-11` | Pinned to tested version; avoids silent breaking changes |
