# Design — F-05: Evidence Exporters

## Component

`src/pegada/exporters.py`

---

## Functions

### `export_json(rows: list[dict], path: Path) → None`

```python
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
```

### `export_csv(rows: list[dict], path: Path) → None`

```python
fields = ["title","url","source","category","snippet","published_at",
          "authors","identifiers","collected_at","identity_status","confidence","notes"]
writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
writer.writeheader()
for row in rows:
    writer.writerow({
        **row,
        "authors":     "; ".join(row.get("authors", [])),
        "identifiers": json.dumps(row.get("identifiers", {}), ensure_ascii=False),
    })
```

`extrasaction="ignore"` silently drops database-internal fields (`id`, etc.).

### `export_markdown(rows: list[dict], path: Path, subject: str = "Aridio Silva") → None`

Builds a list of strings then writes with `"\n".join(lines)`.

Structure:
```
# Mapa da Pegada Digital — {subject}

Evidências registradas: **N**

## Resumo por categoria
- category: count   (sorted)

## Evidências
### {title}
- Fonte / Categoria / URL / Identidade / Observação
```

Uses `collections.Counter` for category counts.

---

## Output File Map

| Function | Default output path |
|---|---|
| `export_json` | `output/evidencias.json` |
| `export_csv` | `output/evidencias.csv` |
| `export_markdown` | `output/mapa_pegada_digital.md` |

Paths are resolved by the CLI (`cmd_export`), not by the exporters themselves.

---

## Dependencies

- `csv`, `json`, `pathlib`, `collections.Counter` (stdlib)

No external dependencies.

---

## Design Decisions

| Decision | Rationale |
|---|---|
| `extrasaction="ignore"` in CSV | DB rows include `id`; no need to enumerate all exclusions |
| `ensure_ascii=False` | Preserves Portuguese characters and Unicode in all formats |
| `subject` parameter in Markdown | Makes the exporter reusable for other subjects without code changes |
| Line list then `join` | Easier to append sections without managing trailing newlines |
