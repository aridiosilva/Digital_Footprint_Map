from types import SimpleNamespace

import pytest

from pegada.notion_sync import REQUIRED_SCHEMA, _properties, sync


class FakeDataSources:
    def __init__(self, pages=None, schema=None):
        self.pages = pages or []
        self.schema = schema if schema is not None else {
            name: {"type": kind} for name, kind in REQUIRED_SCHEMA.items()
        }

    def retrieve(self, **_):
        return {"properties": self.schema}

    def query(self, **_):
        return {"results": self.pages, "has_more": False, "next_cursor": None}


class FakePages:
    def __init__(self):
        self.created = []
        self.updated = []

    def create(self, **kwargs):
        self.created.append(kwargs)

    def update(self, **kwargs):
        self.updated.append(kwargs)


def client(existing=None, schema=None):
    return SimpleNamespace(
        data_sources=FakeDataSources(existing, schema), pages=FakePages()
    )


def row(fingerprint="abc"):
    return {
        "title": "Livro", "url": "urn:isbn:1", "source": "Revan",
        "category": "book", "confidence": 0.9, "identity_status": "reviewed",
        "fingerprint": fingerprint, "authors": ["Aridio Silva"],
        "collected_at": "2026-08-24T12:00:00+00:00", "snippet": "Trecho", "notes": "",
    }


def test_properties_keep_urn_as_text():
    assert _properties(row())["URL"]["rich_text"][0]["text"]["content"] == "urn:isbn:1"


def test_sync_creates_new_page():
    fake = client()
    result = sync([row()], client=fake, data_source_id="source")
    assert result.created == 1
    assert fake.pages.created[0]["parent"] == {"data_source_id": "source"}


def test_sync_updates_existing_page():
    existing = [{"id": "page-1", "properties": {
        "Fingerprint": {"rich_text": [{"plain_text": "abc"}]}
    }}]
    fake = client(existing)
    result = sync([row()], client=fake, data_source_id="source")
    assert result.updated == 1
    assert fake.pages.updated[0]["page_id"] == "page-1"


def test_dry_run_writes_nothing():
    fake = client()
    result = sync([row()], dry_run=True, client=fake, data_source_id="source")
    assert result.created == 1
    assert not fake.pages.created


def test_schema_is_validated():
    fake = client(schema={})
    with pytest.raises(RuntimeError, match="esquema esperado"):
        sync([row()], client=fake, data_source_id="source")
