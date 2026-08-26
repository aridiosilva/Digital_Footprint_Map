# Design — F-08: CLI Interface

## Component

`src/pegada/cli.py`

---

## Entry Point

```
pyproject.toml: [project.scripts]
pegada = "pegada.cli:main"
```

`main()` calls `build_parser().parse_args()` then dispatches to the
appropriate `cmd_*` function via `args.func(args)`.

---

## Argument Parser Structure

```
ArgumentParser(prog="pegada")
└── subparsers (required=True)
    ├── init          → cmd_init
    ├── import-seed   → cmd_import_seed  (positional: path)
    ├── import-csv    → cmd_import_csv   (positional: path, --kind required)
    ├── collect       → cmd_collect      (--config, default: "config/collector.toml")
    ├── export        → cmd_export       (--all flag)
    ├── report        → cmd_report       (--format choices=["pdf"], default="pdf")
    └── notion-sync   → cmd_notion       (--dry-run, --only-reviewed)
```

---

## Command Implementations

### `cmd_init`
```python
repository().init()
output_path().mkdir(parents=True, exist_ok=True)
print(f"Banco inicializado: {db_path()}")
```

### `cmd_import_seed(args)`
```python
items = from_json(args.path)
for item in items: repo.upsert(item)
print(f"{len(items)} evidências importadas.")
```

### `cmd_import_csv(args)`
```python
items = from_csv(args.path, args.kind)
for item in items: repo.upsert(item)
print(f"{len(items)} evidências importadas.")
```

### `cmd_collect(args)`
```python
cfg = load_config(args.config)
for source in cfg["sources"]:
    if not source["enabled"]: continue
    collector = <factory based on source["type"]>
    try:
        items = collector.collect()
        for item in items: repo.upsert(item)
        total += len(items)
    except (HTTPError, JSONDecodeError, KeyError, OSError, TypeError, URLError) as exc:
        print(f"{source['name']}: falhou ({exc})")
print(f"Total coletado/atualizado: {total}")
```

### `cmd_export(args)`
```python
rows = repo.all()
export_json(rows, out / "evidencias.json")
if args.all:
    export_csv(rows, out / "evidencias.csv")
    export_markdown(rows, out / "mapa_pegada_digital.md")
print(f"Exportação concluída em {out}")
```

### `cmd_report`
```python
build_pdf(repo.all(), path)
print(f"Relatório gerado: {path}")
```

### `cmd_notion(args)`
```python
load_dotenv()
rows = repo.all()
if args.only_reviewed:
    rows = [r for r in rows if r["identity_status"] == "reviewed"]
result = sync(rows, dry_run=args.dry_run)
mode = "Simulação" if args.dry_run else "Sincronização"
print(f"{mode} concluída: {result.created} novos, {result.updated} atualizados.")
```

---

## Helper

```python
def repository() -> Repository:
    return Repository(db_path())
```

---

## Configuration Resolution

`db_path()` and `output_path()` in `config.py` read from env vars with defaults:
- `PEGADA_DB` → `data/pegada.sqlite3`
- `PEGADA_OUTPUT` → `output`

`load_dotenv()` is called only in `cmd_notion` (Notion token needed).
Other commands do not require `.env` loading.

---

## Error Isolation in `collect`

Each source collector is wrapped in a broad except block.
Caught exceptions: `HTTPError, JSONDecodeError, KeyError, OSError, TypeError, URLError`.
Uncaught exceptions propagate (programmer errors, not runtime failures).

---

## Dependencies

- `argparse`, `os`, `pathlib`, `json` (stdlib)
- `dotenv.load_dotenv`
- All `pegada.*` modules
