from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


def export_json(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def export_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["title", "url", "source", "category", "snippet", "published_at",
              "authors", "identifiers", "collected_at", "identity_status", "confidence", "notes"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "authors": "; ".join(row.get("authors", [])),
                             "identifiers": json.dumps(row.get("identifiers", {}), ensure_ascii=False)})


def export_markdown(rows: list[dict], path: Path, subject: str = "Aridio Silva") -> None:
    counts = Counter(row["category"] for row in rows)
    lines = [f"# Mapa da Pegada Digital — {subject}", "", f"Evidências registradas: **{len(rows)}**", "",
             "## Resumo por categoria", ""]
    lines.extend(f"- {key}: {value}" for key, value in sorted(counts.items()))
    lines += ["", "## Evidências", ""]
    for row in rows:
        lines += [f"### {row['title']}", "", f"- Fonte: {row['source']}",
                  f"- Categoria: {row['category']}", f"- URL: {row['url']}",
                  f"- Identidade: {row['identity_status']} (confiança {row['confidence']:.0%})",
                  f"- Observação: {row.get('notes') or '—'}", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
