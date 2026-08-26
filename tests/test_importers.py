from __future__ import annotations

import json
from pathlib import Path

import pytest

from pegada.importers import from_csv, from_json
from pegada.models import Evidence

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_json(path: Path, records: list[dict]) -> Path:
    path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    return path


def _write_csv(path: Path, rows: list[str], header: str) -> Path:
    path.write_text("\n".join([header] + rows), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# from_json
# ---------------------------------------------------------------------------

def test_from_json_returns_evidence_list(tmp_path):
    data = [{"title": "Livro A", "url": "urn:isbn:1", "source": "Revan"}]
    items = from_json(_write_json(tmp_path / "seed.json", data))
    assert len(items) == 1
    assert isinstance(items[0], Evidence)


def test_from_json_round_trip(tmp_path):
    """Serialise an Evidence to dict, write to JSON, read back — fields match."""
    original = Evidence(
        title="Dominando OO",
        url="urn:isbn:2",
        source="Book Express",
        category="book",
        snippet="Trecho",
        published_at="2002",
        authors=["Aridio Silva"],
        identifiers={"isbn": "000"},
        identity_status="reviewed",
        confidence=0.9,
        notes="ok",
    )
    # Strip keys not accepted by Evidence.__init__ (e.g. fingerprint, collected_at
    # that differs) — we only compare the fields we control.
    d = original.to_dict()
    d.pop("fingerprint")
    _write_json(tmp_path / "seed.json", [d])
    [loaded] = from_json(tmp_path / "seed.json")

    assert loaded.title == original.title
    assert loaded.url == original.url
    assert loaded.source == original.source
    assert loaded.category == original.category
    assert loaded.snippet == original.snippet
    assert loaded.published_at == original.published_at
    assert loaded.authors == original.authors
    assert loaded.identifiers == original.identifiers
    assert loaded.identity_status == original.identity_status
    assert loaded.confidence == original.confidence
    assert loaded.notes == original.notes


def test_from_json_multiple_records(tmp_path):
    data = [
        {"title": "A", "url": "urn:a", "source": "x"},
        {"title": "B", "url": "urn:b", "source": "y"},
    ]
    items = from_json(_write_json(tmp_path / "seed.json", data))
    assert len(items) == 2
    assert {i.title for i in items} == {"A", "B"}


def test_from_json_fingerprint_is_stable(tmp_path):
    """Loaded evidence produces the same fingerprint as a directly created one."""
    data = [{"title": "Teste", "url": "https://example.com", "source": "x"}]
    [loaded] = from_json(_write_json(tmp_path / "seed.json", data))
    direct = Evidence(title="Teste", url="https://example.com", source="x")
    assert loaded.fingerprint == direct.fingerprint


# ---------------------------------------------------------------------------
# from_csv — defaults
# ---------------------------------------------------------------------------

def test_from_csv_minimal_columns(tmp_path):
    """CSV with only title and url must produce Evidence with correct defaults."""
    path = _write_csv(
        tmp_path / "import.csv",
        rows=["Título Mínimo,urn:min"],
        header="title,url",
    )
    [item] = from_csv(path, "citation")
    assert item.title == "Título Mínimo"
    assert item.url == "urn:min"
    assert item.category == "citation"          # caller-supplied kind
    assert item.source == "import"              # fallback to file stem
    assert item.snippet == ""
    assert item.published_at is None
    assert item.authors == []
    assert item.identity_status == "pending"
    assert item.confidence == 0.5
    assert item.notes == ""


def test_from_csv_source_fallback_uses_stem(tmp_path):
    path = _write_csv(
        tmp_path / "google_scholar.csv",
        rows=["Artigo,urn:1"],
        header="title,url",
    )
    [item] = from_csv(path, "citation")
    assert item.source == "google_scholar"


def test_from_csv_explicit_source_overrides_stem(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["Artigo,urn:1,Fonte Explícita"],
        header="title,url,source",
    )
    [item] = from_csv(path, "citation")
    assert item.source == "Fonte Explícita"


def test_from_csv_category_always_from_parameter(tmp_path):
    """The category column (if present) is ignored; caller's kind wins."""
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["Artigo,urn:1,src,web"],     # 4th col would be ignored by DictReader
        header="title,url,source,category",
    )
    [item] = from_csv(path, "book")
    assert item.category == "book"


# ---------------------------------------------------------------------------
# from_csv — authors splitting
# ---------------------------------------------------------------------------

def test_from_csv_authors_split_semicolon(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["Livro,urn:1,,,,2002,Aridio Silva; Coautor B"],
        header="title,url,source,snippet,notes,published_at,authors",
    )
    [item] = from_csv(path, "book")
    assert item.authors == ["Aridio Silva", "Coautor B"]


def test_from_csv_authors_strips_whitespace(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["Livro,urn:1,,,,,  Alice ;  Bob  ; Charlie  "],
        header="title,url,source,snippet,notes,published_at,authors",
    )
    [item] = from_csv(path, "book")
    assert item.authors == ["Alice", "Bob", "Charlie"]


def test_from_csv_authors_empty_string_produces_empty_list(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["Livro,urn:1,,,,, "],
        header="title,url,source,snippet,notes,published_at,authors",
    )
    [item] = from_csv(path, "book")
    assert item.authors == []


def test_from_csv_authors_absent_column_produces_empty_list(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["Livro,urn:1"],
        header="title,url",
    )
    [item] = from_csv(path, "book")
    assert item.authors == []


# ---------------------------------------------------------------------------
# from_csv — optional numeric / status fields
# ---------------------------------------------------------------------------

def test_from_csv_confidence_parsed_correctly(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["A,urn:1,src,,,,,,reviewed,0.75"],
        header="title,url,source,snippet,published_at,authors,notes,x,identity_status,confidence",
    )
    [item] = from_csv(path, "citation")
    assert item.confidence == pytest.approx(0.75)
    assert item.identity_status == "reviewed"


def test_from_csv_empty_confidence_defaults_to_half(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["A,urn:1,src,,,,,,,"],
        header="title,url,source,snippet,published_at,authors,notes,x,identity_status,confidence",
    )
    [item] = from_csv(path, "citation")
    assert item.confidence == pytest.approx(0.5)


def test_from_csv_empty_identity_status_defaults_to_pending(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["A,urn:1,src,,,,,,, "],
        header="title,url,source,snippet,published_at,authors,notes,x,identity_status,confidence",
    )
    [item] = from_csv(path, "citation")
    assert item.identity_status == "pending"


# ---------------------------------------------------------------------------
# from_csv — BOM handling
# ---------------------------------------------------------------------------

def test_from_csv_handles_bom(tmp_path):
    """Excel/LibreOffice CSVs often include a UTF-8 BOM — must be stripped."""
    path = tmp_path / "bom.csv"
    content = "title,url\nLivro BOM,urn:bom\n"
    path.write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))
    [item] = from_csv(path, "book")
    assert item.title == "Livro BOM"


# ---------------------------------------------------------------------------
# from_csv — multiple rows
# ---------------------------------------------------------------------------

def test_from_csv_multiple_rows(tmp_path):
    path = _write_csv(
        tmp_path / "data.csv",
        rows=["A,urn:a", "B,urn:b", "C,urn:c"],
        header="title,url",
    )
    items = from_csv(path, "web")
    assert len(items) == 3
    assert [i.title for i in items] == ["A", "B", "C"]
