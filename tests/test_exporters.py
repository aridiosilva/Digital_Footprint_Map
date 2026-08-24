import json

from pegada.exporters import export_csv, export_json, export_markdown


def test_exports(tmp_path):
    rows = [{"title":"A","url":"urn:a","source":"x","category":"book","snippet":"s",
             "published_at":None,"authors":[],"identifiers":{},"collected_at":"now",
             "identity_status":"reviewed","confidence":.9,"notes":""}]
    export_json(rows, tmp_path / "a.json")
    export_csv(rows, tmp_path / "a.csv")
    export_markdown(rows, tmp_path / "a.md")
    assert json.loads((tmp_path / "a.json").read_text())[0]["title"] == "A"
    assert "Mapa da Pegada" in (tmp_path / "a.md").read_text()
