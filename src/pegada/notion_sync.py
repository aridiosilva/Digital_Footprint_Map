from __future__ import annotations

import os


def sync(rows: list[dict]) -> int:
    token, database_id = os.getenv("NOTION_TOKEN"), os.getenv("NOTION_DATABASE_ID")
    if not token or not database_id:
        raise RuntimeError("Defina NOTION_TOKEN e NOTION_DATABASE_ID antes da sincronização.")
    try:
        from notion_client import Client
    except ImportError as exc:
        raise RuntimeError("Instale o extra: pip install -e '.[notion]'") from exc
    client = Client(auth=token)
    for row in rows:
        client.pages.create(parent={"database_id": database_id}, properties={
            "Nome": {"title": [{"text": {"content": row["title"][:2000]}}]},
            "URL": {"url": row["url"]},
            "Categoria": {"select": {"name": row["category"]}},
            "Fonte": {"rich_text": [{"text": {"content": row["source"][:2000]}}]},
            "Confiança": {"number": row["confidence"]},
            "Status": {"select": {"name": row["identity_status"]}},
        })
    return len(rows)
