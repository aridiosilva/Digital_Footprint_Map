# Tasks — F-08: CLI Interface

## Status: ✅ Implemented (v1.0.0)

---

- [x] 1. Register `pegada` entry point in `pyproject.toml`
  - `[project.scripts] pegada = "pegada.cli:main"`

- [x] 2. Implement `repository()` helper returning `Repository(db_path())`

- [x] 3. Implement `build_parser()` with all 7 subcommands
  - Use `sub.add_parser` for each; set `func` via `set_defaults`

- [x] 4. Implement `cmd_init`
  - Call `repo.init()` and `output_path().mkdir()`
  - Print database path

- [x] 5. Implement `cmd_import_seed(args)`
  - Call `from_json(args.path)`; upsert each; print count

- [x] 6. Implement `cmd_import_csv(args)`
  - Call `from_csv(args.path, args.kind)`; upsert each; print count

- [x] 7. Implement `cmd_collect(args)`
  - Load config; build collector per `source["type"]`
  - Wrap each collector in try/except; print per-source result
  - Print total at end

- [x] 8. Implement `cmd_export(args)`
  - Always write JSON; add CSV + Markdown when `--all`
  - Print output directory

- [x] 9. Implement `cmd_report`
  - Call `build_pdf`; print output path

- [x] 10. Implement `cmd_notion(args)`
  - `load_dotenv()`; filter by identity_status if `--only-reviewed`
  - Call `sync(rows, dry_run=args.dry_run)`
  - Print mode and counts

- [x] 11. Implement `main()` dispatching via `args.func(args)`

- [ ] 12. Write CLI integration tests
  - Test `init` idempotency; `import-seed` count; `export` file creation
  - _Note: not yet in test suite — add in next iteration_
