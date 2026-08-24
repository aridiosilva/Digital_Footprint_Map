from pegada.db import Repository
from pegada.models import Evidence


def test_upsert_deduplicates(tmp_path):
    repo = Repository(tmp_path / "test.sqlite3")
    repo.init()
    repo.upsert(Evidence(title="A", url="urn:a", source="x"))
    repo.upsert(Evidence(title="A", url="urn:a", source="y", snippet="novo"))
    rows = repo.all()
    assert len(rows) == 1
    assert rows[0]["snippet"] == "novo"
