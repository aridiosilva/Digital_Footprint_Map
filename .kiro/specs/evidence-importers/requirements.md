# Requirements — F-04: Evidence Importers (CSV / JSON)

## Introduction

Manual import pipeline that ingests evidence records from structured files
(JSON seed bundles and CSV exports from external tools such as Google Scholar
and Biblioteca Nacional) and returns typed `Evidence` objects ready for
database upsert.

---

## Glossary

| Term | Definition |
|---|---|
| Seed file | A JSON array of evidence dicts used for offline demo and initial data load |
| CSV import | A spreadsheet exported from an external tool and saved in `data/import/` |
| Kind | The `category` value assigned to all rows when importing from CSV |

---

## Requirements

### Requirement 1: JSON Seed Import

**User Story:** As a researcher, I want to load a JSON file containing
pre-validated evidence records, so that the database is pre-populated for
demonstrations or initial setup.

#### Acceptance Criteria

1. WHEN `from_json(path)` is called THEN it SHALL read the file at `path` as
   UTF-8 encoded JSON.
2. THE JSON content SHALL be a list of objects; each object SHALL be unpacked
   as `Evidence(**item)`.
3. WHEN a field in the JSON matches an `Evidence` field name THEN it SHALL be
   applied directly; unexpected fields SHALL raise `TypeError`.
4. THE function SHALL return a `list[Evidence]`.

### Requirement 2: CSV Import

**User Story:** As a researcher, I want to import a CSV file from Google
Scholar or Biblioteca Nacional, so that manually confirmed results are
included in the digital footprint map.

#### Acceptance Criteria

1. WHEN `from_csv(path, category)` is called THEN it SHALL read the file as
   UTF-8 with BOM-safe encoding (`utf-8-sig`).
2. THE CSV SHALL be read with `csv.DictReader`; column names are used as keys.
3. REQUIRED columns: `title`, `url`. OPTIONAL: `source`, `snippet`,
   `published_at`, `authors`, `identity_status`, `confidence`, `notes`.
4. WHEN `source` is absent or empty THEN the file stem (filename without
   extension) SHALL be used as the source.
5. THE `category` parameter SHALL override any category in the CSV row.
6. WHEN `authors` is present THEN it SHALL be split on `";"` and each element
   stripped; empty elements SHALL be discarded.
7. WHEN `confidence` is absent or empty THEN it SHALL default to `0.5`.
8. WHEN `identity_status` is absent or empty THEN it SHALL default to
   `"pending"`.
9. THE function SHALL return a `list[Evidence]`.

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-13 | Round-trip: `from_json(path_of(evidence.to_dict()))` produces equal Evidence |
| P-14 | `from_csv` with missing optional columns produces Evidence with correct defaults |
| P-15 | `authors` split: `"A; B ; C"` → `["A", "B", "C"]` |
| P-16 | All returned Evidence objects have non-empty `title`, `url`, `source` |
