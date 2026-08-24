from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

REQUIRED_SCHEMA = {
    "Nome": "title", "URL": "rich_text", "Categoria": "select",
    "Fonte": "rich_text", "Confiança": "number", "Status": "select",
    "Fingerprint": "rich_text", "Trecho": "rich_text", "Autores": "multi_select",
    "Coletado em": "date", "Notas": "rich_text",
}


@dataclass(frozen=True, slots=True)
class SyncResult:
    created: int = 0
    updated: int = 0
    skipped: int = 0

    @property
    def total(self) -> int:
        return self.created + self.updated + self.skipped


def _text(value: Any, limit: int = 2000) -> list[dict]:
    content = str(value or "")[:limit]
    return [{"type": "text", "text": {"content": content}}] if content else []


def _properties(row: dict) -> dict:
    collected_at = row.get("collected_at")
    return {
        "Nome": {"title": _text(row.get("title"))},
        "URL": {"rich_text": _text(row.get("url"))},
        "Categoria": {"select": {"name": str(row.get("category") or "web")[:100]}},
        "Fonte": {"rich_text": _text(row.get("source"))},
        "Confiança": {"number": float(row.get("confidence") or 0)},
        "Status": {"select": {"name": str(row.get("identity_status") or "pending")[:100]}},
        "Fingerprint": {"rich_text": _text(row.get("fingerprint"))},
        "Trecho": {"rich_text": _text(row.get("snippet"))},
        "Autores": {"multi_select": [
            {"name": str(author)[:100]} for author in row.get("authors", [])[:100]
        ]},
        "Coletado em": {"date": {"start": collected_at} if collected_at else None},
        "Notas": {"rich_text": _text(row.get("notes"))},
    }


def _resolve_data_source_id(client: Any, explicit_id: str | None, database_id: str | None) -> str:
    if explicit_id:
        return explicit_id
    if not database_id:
        raise RuntimeError("Defina NOTION_DATA_SOURCE_ID (recomendado) ou NOTION_DATABASE_ID.")
    database = client.databases.retrieve(database_id=database_id)
    sources = database.get("data_sources", [])
    if len(sources) != 1:
        raise RuntimeError(
            "O database do Notion deve ter exatamente uma fonte de dados; "
            "defina NOTION_DATA_SOURCE_ID para escolher explicitamente."
        )
    return sources[0]["id"]


def _validate_schema(client: Any, data_source_id: str) -> None:
    actual = client.data_sources.retrieve(data_source_id=data_source_id).get("properties", {})
    problems = []
    for name, expected_type in REQUIRED_SCHEMA.items():
        received = actual.get(name, {}).get("type")
        if received != expected_type:
            problems.append(f"{name} ({expected_type}; encontrado: {received or 'ausente'})")
    if problems:
        raise RuntimeError("A fonte de dados do Notion não possui o esquema esperado: " + ", ".join(problems))


def _existing_pages(client: Any, data_source_id: str) -> dict[str, str]:
    pages: dict[str, str] = {}
    cursor = None
    while True:
        request = {"data_source_id": data_source_id, "page_size": 100}
        if cursor:
            request["start_cursor"] = cursor
        response = client.data_sources.query(**request)
        for page in response.get("results", []):
            rich_text = page.get("properties", {}).get("Fingerprint", {}).get("rich_text", [])
            fingerprint = "".join(part.get("plain_text", "") for part in rich_text)
            if fingerprint:
                pages[fingerprint] = page["id"]
        if not response.get("has_more"):
            return pages
        cursor = response.get("next_cursor")


def sync(
    rows: list[dict], *, dry_run: bool = False, client: Any | None = None,
    data_source_id: str | None = None,
) -> SyncResult:
    token = os.getenv("NOTION_TOKEN")
    if client is None:
        if not token:
            raise RuntimeError("Defina NOTION_TOKEN antes da sincronização.")
        try:
            from notion_client import Client
        except ImportError as exc:
            raise RuntimeError("Instale a integração: pip install -e '.[notion]'") from exc
        client = Client(auth=token, notion_version="2026-03-11")

    source_id = _resolve_data_source_id(
        client, data_source_id or os.getenv("NOTION_DATA_SOURCE_ID"),
        os.getenv("NOTION_DATABASE_ID"),
    )
    _validate_schema(client, source_id)
    existing = _existing_pages(client, source_id)
    created = updated = 0

    for row in rows:
        fingerprint = row.get("fingerprint")
        if not fingerprint:
            raise RuntimeError("Uma evidência sem fingerprint não pode ser sincronizada.")
        page_id = existing.get(fingerprint)
        if dry_run:
            created += int(not page_id); updated += int(bool(page_id))
            continue
        properties = _properties(row)
        if page_id:
            client.pages.update(page_id=page_id, properties=properties); updated += 1
        else:
            client.pages.create(parent={"data_source_id": source_id}, properties=properties)
            created += 1

    return SyncResult(created=created, updated=updated)


def expected_schema_json() -> str:
    return json.dumps(REQUIRED_SCHEMA, ensure_ascii=False, indent=2)
