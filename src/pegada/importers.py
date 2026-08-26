from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import Evidence


def from_json(path: Path) -> list[Evidence]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Evidence(**item) for item in raw]


def from_csv(path: Path, category: str) -> list[Evidence]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        return [Evidence(title=r["title"], url=r["url"], source=r.get("source") or path.stem,
                         category=category, snippet=r.get("snippet", ""),
                         published_at=r.get("published_at") or None,
                         authors=[x.strip() for x in r.get("authors", "").split(";") if x.strip()],
                         identity_status=r.get("identity_status") or "pending",
                         confidence=float(r.get("confidence", "").strip() or 0.5), notes=r.get("notes", ""))
                for r in rows]

