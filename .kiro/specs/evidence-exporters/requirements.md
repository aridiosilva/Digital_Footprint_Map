# Requirements — F-05: Evidence Exporters (JSON / CSV / Markdown)

## Introduction

Serialises the full evidence dataset to three machine-readable and
human-readable formats. All exporters accept a plain `list[dict]` (as returned
by `Repository.all()`) and write to a caller-specified `Path`.

---

## Glossary

| Term | Definition |
|---|---|
| Export | Writes the complete evidence list to a file in a specific format |
| Subject | The person whose digital footprint is being mapped (default: "Aridio Silva") |

---

## Requirements

### Requirement 1: JSON Export

**User Story:** As a developer or analyst, I want to export all evidence as
JSON, so that the data can be consumed by external tools or archived.

#### Acceptance Criteria

1. WHEN `export_json(rows, path)` is called THEN it SHALL write a UTF-8 JSON
   file at `path` containing all rows as a JSON array.
2. THE JSON SHALL be pretty-printed with `indent=2`.
3. THE JSON SHALL be written with `ensure_ascii=False` to preserve Unicode
   characters.
4. WHEN the parent directory of `path` does not exist THEN it SHALL be created
   automatically.

### Requirement 2: CSV Export

**User Story:** As an analyst, I want to export evidence to CSV, so that I can
open it in spreadsheet tools.

#### Acceptance Criteria

1. WHEN `export_csv(rows, path)` is called THEN it SHALL write a UTF-8 CSV
   file with a header row followed by one data row per evidence record.
2. THE column order SHALL be: `title`, `url`, `source`, `category`, `snippet`,
   `published_at`, `authors`, `identifiers`, `collected_at`,
   `identity_status`, `confidence`, `notes`.
3. THE `authors` list SHALL be serialised as a `"; "`-joined string.
4. THE `identifiers` dict SHALL be serialised as a compact JSON string.
5. WHEN the parent directory does not exist THEN it SHALL be created.

### Requirement 3: Markdown Export

**User Story:** As a researcher, I want to export evidence to Markdown, so
that I can publish or review it as a human-readable document.

#### Acceptance Criteria

1. WHEN `export_markdown(rows, path)` is called THEN it SHALL produce a
   Markdown document with: a title heading, total evidence count, a summary
   table by category, and a section per evidence.
2. THE document title SHALL be `# Mapa da Pegada Digital — {subject}`.
3. THE summary section SHALL list each category and its count, sorted
   alphabetically.
4. EACH evidence section SHALL include: title (H3), source, category, URL,
   identity status with confidence percentage, and notes.
5. WHEN the parent directory does not exist THEN it SHALL be created.

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-17 | `export_json` output is valid JSON and round-trips without data loss |
| P-18 | `export_csv` row count equals `len(rows) + 1` (header) |
| P-19 | `export_markdown` document contains each evidence title exactly once |
| P-20 | All three exporters create the parent directory if it does not exist |
