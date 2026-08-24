from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import Evidence

SCHEMA = """
CREATE TABLE IF NOT EXISTS evidence (
 id INTEGER PRIMARY KEY, fingerprint TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
 url TEXT NOT NULL, source TEXT NOT NULL, category TEXT NOT NULL, snippet TEXT,
 published_at TEXT, authors_json TEXT NOT NULL, identifiers_json TEXT NOT NULL,
 collected_at TEXT NOT NULL, identity_status TEXT NOT NULL, confidence REAL NOT NULL,
 notes TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_evidence_category ON evidence(category);
CREATE INDEX IF NOT EXISTS idx_evidence_identity ON evidence(identity_status);
CREATE TABLE IF NOT EXISTS runs (
 id INTEGER PRIMARY KEY, started_at TEXT NOT NULL, finished_at TEXT,
 collector TEXT NOT NULL, status TEXT NOT NULL, details TEXT NOT NULL DEFAULT ''
);
"""


class Repository:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def init(self) -> None:
        with self.connect() as con:
            con.executescript(SCHEMA)

    def upsert(self, item: Evidence) -> None:
        row = item.to_dict()
        with self.connect() as con:
            con.execute(
                """INSERT INTO evidence
                (fingerprint,title,url,source,category,snippet,published_at,authors_json,
                 identifiers_json,collected_at,identity_status,confidence,notes)
                VALUES (:fingerprint,:title,:url,:source,:category,:snippet,:published_at,
                 :authors_json,:identifiers_json,:collected_at,:identity_status,:confidence,:notes)
                ON CONFLICT(fingerprint) DO UPDATE SET snippet=excluded.snippet,
                 collected_at=excluded.collected_at, confidence=MAX(confidence, excluded.confidence),
                 notes=excluded.notes""",
                {**row, "authors_json": json.dumps(item.authors, ensure_ascii=False),
                 "identifiers_json": json.dumps(item.identifiers, ensure_ascii=False)},
            )

    def all(self) -> list[dict]:
        self.init()
        with self.connect() as con:
            rows = con.execute("SELECT * FROM evidence ORDER BY category,title").fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["authors"] = json.loads(item.pop("authors_json"))
            item["identifiers"] = json.loads(item.pop("identifiers_json"))
            result.append(item)
        return result
