# Requirements — F-0007: Notion Sync

## Introduction

Explicit, idempotent synchronisation of reviewed evidence records to a Notion
Data Source. Uses the `Fingerprint` property to detect and update existing
pages rather than creating duplicates. A `--dry-run` mode lets operators
preview changes without writing to Notion.

---

## Glossary

| Term | Definition |
|---|---|
| Data Source | A Notion database configured with the required schema columns |
| Fingerprint | SHA-256 property used as a stable unique key in Notion pages |
| Idempotent | Re-running sync produces the same Notion state without duplicates |
| Dry run | Execution that counts changes without writing anything to Notion |
| Schema validation | Checking that the remote Data Source has all required columns before writing |

---

## Requirements

### Requirement 1: Schema Validation

**User Story:** As an operator, I want the sync to fail loudly if the Notion
schema is wrong, so that I don't silently lose data.

#### Acceptance Criteria

1. BEFORE writing any page WHEN `sync()` is called THEN it SHALL retrieve the
   remote schema and compare it against `REQUIRED_SCHEMA`.
2. IF any required column is absent or has the wrong type THEN `sync()` SHALL
   raise `RuntimeError` listing the offending columns.
3. THE required columns and their types SHALL be: `Nome` (title), `URL`
   (rich_text), `Categoria` (select), `Fonte` (rich_text), `Confiança`
   (number), `Status` (select), `Fingerprint` (rich_text), `Trecho`
   (rich_text), `Autores` (multi_select), `Coletado em` (date), `Notas`
   (rich_text).

### Requirement 2: Idempotent Create / Update

**User Story:** As an operator, I want re-running sync to update existing
pages instead of duplicating them, so that the Notion database stays clean.

#### Acceptance Criteria

1. WHEN `sync(rows)` is called THEN it SHALL query the Data Source and build a
   map of `{fingerprint → page_id}` for all existing pages.
2. IF a row's fingerprint is NOT in the existing map THEN a new page SHALL be
   created with `parent={"data_source_id": source_id}`.
3. IF a row's fingerprint IS in the existing map THEN the existing page SHALL
   be updated via `pages.update`.
4. NO duplicate pages SHALL ever be created for the same fingerprint.
5. THE function SHALL return a `SyncResult` with `created`, `updated`, and
   `skipped` counts.

### Requirement 3: Dry-Run Mode

**User Story:** As an operator, I want to preview what would be synced without
writing anything, so that I can verify the plan before modifying Notion.

#### Acceptance Criteria

1. WHEN `sync(rows, dry_run=True)` is called THEN NO pages SHALL be created or
   updated in Notion.
2. THE returned `SyncResult` SHALL still reflect the counts of what would have
   been created and updated.

### Requirement 4: Data Source Resolution

**User Story:** As an operator, I want to configure the target Data Source via
environment variables, so that no credentials are hardcoded.

#### Acceptance Criteria

1. WHEN `NOTION_DATA_SOURCE_ID` is set THEN it SHALL be used directly.
2. WHEN only `NOTION_DATABASE_ID` is set THEN the system SHALL retrieve the
   database, find the single Data Source, and use its ID.
3. IF neither variable is set THEN `sync()` SHALL raise `RuntimeError` with a
   descriptive message.
4. IF `NOTION_DATABASE_ID` points to a database with more than one Data Source
   THEN `sync()` SHALL raise `RuntimeError` asking the operator to set
   `NOTION_DATA_SOURCE_ID` explicitly.

### Requirement 5: Missing `notion-client` Dependency

**User Story:** As a developer, I want a clear error when the optional Notion
package is not installed.

#### Acceptance Criteria

1. WHEN `notion-client` is not installed and `sync()` is called without a
   mock client THEN a `RuntimeError` SHALL be raised with an install hint
   (`pip install -e '.[notion]'`).

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-24 | `sync([row])` with no existing pages → `result.created == 1, result.updated == 0` |
| P-25 | `sync([row])` with `row.fingerprint` already existing → `result.updated == 1, result.created == 0` |
| P-26 | `sync([row], dry_run=True)` → `fake_client.pages.created == []` and `fake_client.pages.updated == []` |
| P-27 | `sync` with wrong schema → raises `RuntimeError` matching "esquema esperado" |
| P-28 | `sync` with empty list → `SyncResult(created=0, updated=0, skipped=0)` |
