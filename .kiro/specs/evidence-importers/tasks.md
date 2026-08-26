# Tasks — F-04: Evidence Importers

## Status: ✅ Implemented (v1.0.0)

---

- [x] 1. Implement `from_json(path: Path) → list[Evidence]`
  - `src/pegada/importers.py`
  - Read UTF-8 JSON; unpack each dict as `Evidence(**item)`

- [x] 2. Implement `from_csv(path: Path, category: str) → list[Evidence]`
  - Open with `utf-8-sig` encoding and `newline=""`
  - Use `csv.DictReader`
  - Apply defaults for all optional columns
  - Split `authors` on `";"`, strip, discard empty

- [x] 3. Wire importers into CLI commands `import-seed` and `import-csv`
  - `cmd_import_seed`: calls `from_json`, then `repo.upsert` per item
  - `cmd_import_csv`: calls `from_csv(path, args.kind)`, then `repo.upsert` per item

- [ ] 4. Write unit tests for importers
  - `test_from_json_round_trip`: write JSON, read back, compare fields
  - `test_from_csv_defaults`: minimal CSV (title + url), verify defaults
  - `test_from_csv_authors_split`: verify `"A; B"` → `["A", "B"]`
  - _Note: not yet in test suite — add in next iteration_
