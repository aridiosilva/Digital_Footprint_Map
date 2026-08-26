# Design — F-0002: Auditable SQLite Database

## Component

`src/pegada/db.py`

---

## Schema

```sql
CREATE TABLE IF NOT EXISTS evidence (
  id               INTEGER PRIMARY KEY,
  fingerprint      TEXT    NOT NULL UNIQUE,
  title            TEXT    NOT NULL,
  url              TEXT    NOT NULL,
  source           TEXT    NOT NULL,
  category         TEXT    NOT NULL,
  snippet          TEXT,
  published_at     TEXT,
  authors_json     TEXT    NOT NULL,
  identifiers_json TEXT    NOT NULL,
  collected_at     TEXT    NOT NULL,
  identity_status  TEXT    NOT NULL,
  confidence       REAL    NOT NULL,
  notes            TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_evidence_category ON evidence(category);
CREATE INDEX IF NOT EXISTS idx_evidence_identity  ON evidence(identity_status);

CREATE TABLE IF NOT EXISTS runs (
  id          INTEGER PRIMARY KEY,
  started_at  TEXT NOT NULL,
  finished_at TEXT,
  collector   TEXT NOT NULL,
  status      TEXT NOT NULL,
  details     TEXT NOT NULL DEFAULT ''
);
```

---

## Class Design

```
Repository
├── __init__(path: str | Path)
│   └── Stores path; creates parent directories
├── connect() → sqlite3.Connection
│   └── row_factory = sqlite3.Row
├── init() → None
│   └── executescript(SCHEMA)  — idempotent (IF NOT EXISTS)
├── upsert(item: Evidence) → None
│   └── INSERT … ON CONFLICT(fingerprint) DO UPDATE
└── all() → list[dict]
    └── SELECT * ORDER BY category, title → deserialise JSON fields
```

---

## Upsert Strategy

```sql
INSERT INTO evidence (fingerprint, …)
VALUES (:fingerprint, …)
ON CONFLICT(fingerprint) DO UPDATE SET
  snippet      = excluded.snippet,
  collected_at = excluded.collected_at,
  confidence   = MAX(confidence, excluded.confidence),
  notes        = excluded.notes
```

Fields NOT updated on conflict: `title`, `url`, `source`, `category`,
`published_at`, `authors_json`, `identifiers_json`, `identity_status`.
This preserves human-reviewed identity status and original metadata.

---

## JSON Serialisation Strategy

`authors` (list) and `identifiers` (dict) are stored as JSON strings in
`authors_json` / `identifiers_json` columns. On read they are parsed back:

```python
item["authors"]     = json.loads(item.pop("authors_json"))
item["identifiers"] = json.loads(item.pop("identifiers_json"))
```

---

## Dependencies

- `sqlite3` (stdlib)
- `json` (stdlib)
- `pathlib` (stdlib)
- `pegada.models.Evidence`

---

## Design Decisions

| Decision | Rationale |
|---|---|
| No ORM | Keeps the dependency list minimal; queries are simple |
| `sqlite3.Row` as row_factory | Dict-like access without extra mapping code |
| `executescript` for schema | Single transaction; safe for `IF NOT EXISTS` multi-statement DDL |
| `MAX(confidence, excluded)` in upsert | Confidence is monotonically non-decreasing — reviewed items stay reviewed |
| Parent dir auto-created in `__init__` | Allows fresh clone → `pegada init` without manual `mkdir` |
