# Design — F-0004: Evidence Importers

## Component

`src/pegada/importers.py`

---

## Functions

### `from_json(path: Path) → list[Evidence]`

```python
raw = json.loads(path.read_text(encoding="utf-8"))
return [Evidence(**item) for item in raw]
```

Pure function. Raises `JSONDecodeError` on invalid JSON.
Raises `TypeError` on unexpected fields (dataclass strict init).

---

### `from_csv(path: Path, category: str) → list[Evidence]`

```python
with path.open(encoding="utf-8-sig", newline="") as handle:
    rows = csv.DictReader(handle)
    return [Evidence(
        title           = r["title"],
        url             = r["url"],
        source          = r.get("source") or path.stem,
        category        = category,             # caller-provided
        snippet         = r.get("snippet", ""),
        published_at    = r.get("published_at") or None,
        authors         = [x.strip() for x in r.get("authors","").split(";") if x.strip()],
        identity_status = r.get("identity_status") or "pending",
        confidence      = float(r.get("confidence") or 0.5),
        notes           = r.get("notes", ""),
    ) for r in rows]
```

`utf-8-sig` silently strips the BOM emitted by Excel/LibreOffice.

---

## CSV Column Mapping

| CSV Column | Evidence Field | Default if absent/empty |
|---|---|---|
| `title` | `title` | — (required) |
| `url` | `url` | — (required) |
| `source` | `source` | `path.stem` |
| `snippet` | `snippet` | `""` |
| `published_at` | `published_at` | `None` |
| `authors` | `authors` | `[]` |
| `identity_status` | `identity_status` | `"pending"` |
| `confidence` | `confidence` | `0.5` |
| `notes` | `notes` | `""` |

`category` is always the caller-supplied parameter, never read from CSV.

---

## Sample CSV Format

```csv
title,url,source,snippet,published_at,authors,identity_status,confidence,notes
Tecnologia de Objetos,https://exemplo.org/livro,Revan,,2003,Aridio Silva,reviewed,0.95,
```

---

## Dependencies

- `csv`, `json`, `pathlib` (stdlib)
- `pegada.models.Evidence`

---

## Design Decisions

| Decision | Rationale |
|---|---|
| `utf-8-sig` encoding | Handles BOM from Excel without extra stripping logic |
| `category` as parameter, not CSV column | Prevents accidental category override; caller knows the source type |
| `path.stem` as fallback source | Gives a meaningful source name when column is missing |
| `or "pending"` / `or 0.5` | Treats empty CSV cells the same as absent — consistent with Evidence defaults |
