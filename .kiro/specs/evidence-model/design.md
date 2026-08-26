# Design — F-01: Evidence Model & Fingerprint

## Component

`src/pegada/models.py`

---

## Data Model

```
Evidence (dataclass, slots=True)
├── title:           str               # required
├── url:             str               # required
├── source:          str               # required
├── category:        str = "web"
├── snippet:         str = ""
├── published_at:    str | None = None
├── authors:         list[str] = []
├── identifiers:     dict[str,str] = {}
├── collected_at:    str = utc_now()
├── identity_status: str = "pending"
├── confidence:      float = 0.5
├── notes:           str = ""
└── fingerprint:     @property → str   # computed, not stored
```

---

## Fingerprint Algorithm

```python
raw = f"{url.strip().lower()}|{title.strip().lower()}|{category}"
fingerprint = sha256(raw.encode("utf-8")).hexdigest()  # 64 hex chars
```

Collision resistance relies on SHA-256; for deduplication purposes within a
single dataset this is sufficient — birthday attack probability is negligible.

---

## Serialisation (`to_dict`)

Uses `dataclasses.asdict()` (deep copy) then injects the computed `fingerprint`.
Result is a plain `dict[str, Any]` safe for JSON serialisation.

---

## Dependencies

- `dataclasses` (stdlib)
- `datetime` (stdlib)
- `hashlib` (stdlib)

No external dependencies.

---

## Interface consumed by other features

| Feature | How it uses Evidence |
|---|---|
| F-02 auditable-database | `Repository.upsert(item: Evidence)` |
| F-03 evidence-collectors | Collectors return `list[Evidence]` |
| F-04 evidence-importers | Importers return `list[Evidence]` |
| F-05 evidence-exporters | Exporters receive `list[dict]` from `repo.all()` |
| F-06 pdf-report | Report receives `list[dict]` |
| F-07 notion-sync | Sync receives `list[dict]` |

---

## Design Decisions

| Decision | Rationale |
|---|---|
| `slots=True` | Reduces per-instance memory; model is instantiated thousands of times |
| Fingerprint as `@property` | Not stored → computed fresh; avoids stale cached values |
| `field(default_factory=list/dict)` | Prevents mutable default sharing between instances |
| `asdict()` in `to_dict()` | Deep-copies nested structures; avoids aliasing bugs |
| `utc_now()` as module-level function | Enables monkeypatching in tests |
