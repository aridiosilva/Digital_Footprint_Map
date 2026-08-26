# Tasks — F-05: Evidence Exporters

## Status: ✅ Implemented (v1.0.0)

---

- [x] 1. Implement `export_json(rows, path)`
  - `src/pegada/exporters.py`
  - `json.dumps` with `ensure_ascii=False, indent=2`
  - Auto-create parent directory

- [x] 2. Implement `export_csv(rows, path)`
  - Fixed field order; `extrasaction="ignore"`
  - Serialise `authors` as `"; "`-joined string
  - Serialise `identifiers` as compact JSON

- [x] 3. Implement `export_markdown(rows, path, subject="Aridio Silva")`
  - Title, count, category summary (sorted), per-evidence sections
  - Use `collections.Counter` for category counts

- [x] 4. Wire exporters into CLI `export` command
  - `cmd_export`: always writes JSON; adds CSV + Markdown when `--all`

- [x] 5. Write unit tests in `tests/test_exporters.py`
  - `test_exports`: create sample rows, call all three exporters
  - Verify JSON round-trip; Markdown contains expected heading
