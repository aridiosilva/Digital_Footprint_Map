from __future__ import annotations

from pegada.report import build_pdf

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sample_row(**overrides) -> dict:
    base = {
        "title": "Dominando OO",
        "url": "urn:isbn:1",
        "source": "Book Express",
        "category": "book",
        "snippet": "Trecho representativo do livro.",
        "published_at": "2002",
        "authors": ["Aridio Silva"],
        "identifiers": {"isbn": "000"},
        "collected_at": "2026-08-26T00:00:00+00:00",
        "identity_status": "reviewed",
        "confidence": 0.9,
        "notes": "",
    }
    return {**base, **overrides}


# ---------------------------------------------------------------------------
# Basic smoke tests
# ---------------------------------------------------------------------------

def test_build_pdf_creates_file(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([], path)
    assert path.exists()


def test_build_pdf_produces_valid_pdf_header(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([], path)
    assert path.read_bytes().startswith(b"%PDF")


def test_build_pdf_with_rows_creates_file(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row()], path)
    assert path.exists()
    assert path.stat().st_size > 0


def test_build_pdf_with_rows_valid_pdf_header(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row()], path)
    assert path.read_bytes().startswith(b"%PDF")


# ---------------------------------------------------------------------------
# Output path handling
# ---------------------------------------------------------------------------

def test_build_pdf_creates_parent_directory(tmp_path):
    nested = tmp_path / "a" / "b" / "c" / "report.pdf"
    build_pdf([], nested)
    assert nested.exists()


def test_build_pdf_overwrites_existing_file(tmp_path):
    path = tmp_path / "report.pdf"
    path.write_bytes(b"placeholder")
    build_pdf([], path)
    assert path.read_bytes().startswith(b"%PDF")


# ---------------------------------------------------------------------------
# Multiple evidence categories
# ---------------------------------------------------------------------------

def test_build_pdf_multiple_categories(tmp_path):
    rows = [
        _sample_row(title="Livro A", category="book"),
        _sample_row(title="Perfil GitHub", url="https://github.com/x", category="profile"),
        _sample_row(title="Artigo OA", url="urn:oa:1", category="academic"),
    ]
    path = tmp_path / "report.pdf"
    build_pdf(rows, path)
    assert path.read_bytes().startswith(b"%PDF")


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_build_pdf_empty_snippet_falls_back_to_notes(tmp_path):
    """Row with empty snippet and non-empty notes must not raise."""
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row(snippet="", notes="Ver página 42.")], path)
    assert path.read_bytes().startswith(b"%PDF")


def test_build_pdf_both_snippet_and_notes_empty(tmp_path):
    """Row with no snippet and no notes must not raise (falls back to 'Sem resumo.')."""
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row(snippet="", notes="")], path)
    assert path.read_bytes().startswith(b"%PDF")


def test_build_pdf_custom_subject(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row()], path, subject="João Silva")
    assert path.read_bytes().startswith(b"%PDF")


def test_build_pdf_row_with_no_authors(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row(authors=[])], path)
    assert path.read_bytes().startswith(b"%PDF")


def test_build_pdf_high_confidence_row(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row(confidence=1.0, identity_status="reviewed")], path)
    assert path.read_bytes().startswith(b"%PDF")


def test_build_pdf_pending_identity_row(tmp_path):
    path = tmp_path / "report.pdf"
    build_pdf([_sample_row(confidence=0.35, identity_status="pending")], path)
    assert path.read_bytes().startswith(b"%PDF")


def test_build_pdf_many_rows_does_not_raise(tmp_path):
    """50 rows with varied data must complete without error."""
    rows = [
        _sample_row(
            title=f"Evidência {i}",
            url=f"urn:ev:{i}",
            category=["book", "academic", "profile", "repository", "web"][i % 5],
        )
        for i in range(50)
    ]
    path = tmp_path / "report.pdf"
    build_pdf(rows, path)
    assert path.read_bytes().startswith(b"%PDF")
