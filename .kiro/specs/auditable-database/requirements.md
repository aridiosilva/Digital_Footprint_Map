# Requirements — F-0002: Auditable SQLite Database

## Introduction

Provides durable, deduplicated persistence for `Evidence` records using SQLite.
Deduplication is enforced at the database level via the `fingerprint` unique
constraint. An additional `runs` table stores the audit trail of collector
executions.

---

## Glossary

| Term | Definition |
|---|---|
| Repository | The class that wraps the SQLite connection and exposes CRUD operations |
| Upsert | INSERT … ON CONFLICT DO UPDATE — creates if new, updates if existing |
| Audit trail | The `runs` table that records when and how data was collected |

---

## Requirements

### Requirement 1: Schema Initialisation

**User Story:** As a system operator, I want the database schema to be
created automatically on first use, so that no manual setup step is needed.

#### Acceptance Criteria

1. WHEN `Repository.init()` is called THEN the `evidence` and `runs` tables
   SHALL be created if they do not already exist.
2. WHEN `Repository.init()` is called on an already-initialised database THEN
   no error SHALL occur and existing data SHALL be preserved.
3. THE `evidence` table SHALL have indices on `category` and `identity_status`
   columns.
4. WHEN the parent directory of the database path does not exist THEN
   `Repository.__init__` SHALL create it automatically.

### Requirement 2: Idempotent Upsert

**User Story:** As a developer, I want re-collecting the same URL to update
the record rather than creating a duplicate, so that the database reflects the
latest state without duplication.

#### Acceptance Criteria

1. WHEN `upsert(item)` is called with an `Evidence` whose fingerprint already
   exists THEN the existing row SHALL be updated, not duplicated.
2. WHEN updating an existing record THEN `snippet`, `collected_at`, and `notes`
   SHALL be replaced with the new values.
3. WHEN updating an existing record THEN `confidence` SHALL be set to
   `MAX(existing, incoming)` — confidence never decreases.
4. WHEN `upsert(item)` is called with a new fingerprint THEN a new row SHALL
   be inserted.
5. THE `authors` and `identifiers` fields SHALL be serialised as JSON strings
   in the database and deserialised back to Python objects when read.

### Requirement 3: Full Retrieval

**User Story:** As an exporter or report generator, I want to retrieve all
evidence records as a list of plain dicts, so that I can process them without
depending on the `Evidence` class.

#### Acceptance Criteria

1. WHEN `Repository.all()` is called THEN it SHALL return all rows ordered by
   `category` then `title`.
2. EACH returned dict SHALL have `authors` as a Python list and `identifiers`
   as a Python dict (not raw JSON strings).
3. WHEN the database has not been initialised yet THEN `all()` SHALL call
   `init()` before querying.

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-05 | Upsert N times the same Evidence → `len(repo.all()) == 1` |
| P-06 | `confidence` after N upserts ≥ max confidence of all upserted values |
| P-07 | `all()` result is sorted by `(category, title)` |
| P-08 | `authors` and `identifiers` round-trip through the database unchanged |
