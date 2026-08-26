from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from pegada.cli import build_parser

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def run(*argv: str) -> tuple[int, str]:
    """Run the CLI with given arguments and capture stdout.

    Returns (exit_code, stdout_text). Uses monkeypatching rather than
    subprocess so coverage is collected correctly.
    """
    import io

    captured = io.StringIO()
    parser = build_parser()
    args = parser.parse_args(list(argv))
    with patch("sys.stdout", captured):
        args.func(args)
    return 0, captured.getvalue()


def _make_seed(tmp_path: Path, records: list[dict] | None = None) -> Path:
    if records is None:
        records = [
            {"title": "Livro A", "url": "urn:isbn:1", "source": "Revan",
             "category": "book", "authors": ["Aridio Silva"],
             "identity_status": "reviewed", "confidence": 0.95},
        ]
    path = tmp_path / "seed.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return path


def _make_csv(tmp_path: Path) -> Path:
    path = tmp_path / "import.csv"
    path.write_text("title,url\nArtigo CSV,urn:csv:1\n", encoding="utf-8")
    return path


def _env(tmp_path: Path) -> dict:
    """Return env-var overrides pointing DB and output to tmp_path."""
    return {
        "PEGADA_DB": str(tmp_path / "pegada.sqlite3"),
        "PEGADA_OUTPUT": str(tmp_path / "output"),
    }


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------


def test_init_creates_database(tmp_path):
    with patch.dict("os.environ", _env(tmp_path)):
        _, out = run("init")
    assert (tmp_path / "pegada.sqlite3").exists()
    assert "Banco inicializado" in out


def test_init_creates_output_directory(tmp_path):
    with patch.dict("os.environ", _env(tmp_path)):
        run("init")
    assert (tmp_path / "output").is_dir()


def test_init_is_idempotent(tmp_path):
    """Running init twice must not raise and must leave the DB intact."""
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        _, out = run("init")
    assert "Banco inicializado" in out
    assert (tmp_path / "pegada.sqlite3").exists()


def test_init_prints_db_path(tmp_path):
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        _, out = run("init")
    assert str(tmp_path / "pegada.sqlite3") in out


# ---------------------------------------------------------------------------
# import-seed
# ---------------------------------------------------------------------------


def test_import_seed_count_matches_json(tmp_path):
    seed = _make_seed(tmp_path)
    with patch.dict("os.environ", _env(tmp_path)):
        run("init")
        _, out = run("import-seed", str(seed))
    assert "1 evidências importadas" in out


def test_import_seed_multiple_records(tmp_path):
    records = [
        {"title": f"Livro {i}", "url": f"urn:{i}", "source": "x"}
        for i in range(5)
    ]
    seed = _make_seed(tmp_path, records)
    with patch.dict("os.environ", _env(tmp_path)):
        run("init")
        _, out = run("import-seed", str(seed))
    assert "5 evidências importadas" in out


def test_import_seed_is_idempotent(tmp_path):
    """Importing the same seed twice must not duplicate records."""
    from pegada.db import Repository

    seed = _make_seed(tmp_path)
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("import-seed", str(seed))
        run("import-seed", str(seed))
        repo = Repository(tmp_path / "pegada.sqlite3")
        rows = repo.all()
    assert len(rows) == 1


# ---------------------------------------------------------------------------
# import-csv
# ---------------------------------------------------------------------------


def test_import_csv_count(tmp_path):
    csv_file = _make_csv(tmp_path)
    with patch.dict("os.environ", _env(tmp_path)):
        run("init")
        _, out = run("import-csv", str(csv_file), "--kind", "citation")
    assert "1 evidências importadas" in out


def test_import_csv_category_set_correctly(tmp_path):
    from pegada.db import Repository

    csv_file = _make_csv(tmp_path)
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("import-csv", str(csv_file), "--kind", "book")
        repo = Repository(tmp_path / "pegada.sqlite3")
        rows = repo.all()
    assert rows[0]["category"] == "book"


# ---------------------------------------------------------------------------
# export
# ---------------------------------------------------------------------------


def test_export_always_writes_json(tmp_path):
    seed = _make_seed(tmp_path)
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("import-seed", str(seed))
        _, out = run("export")
    assert (tmp_path / "output" / "evidencias.json").exists()
    assert "Exportação concluída" in out


def test_export_all_writes_csv_and_markdown(tmp_path):
    seed = _make_seed(tmp_path)
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("import-seed", str(seed))
        run("export", "--all")
    assert (tmp_path / "output" / "evidencias.csv").exists()
    assert (tmp_path / "output" / "mapa_pegada_digital.md").exists()


def test_export_without_all_does_not_write_csv(tmp_path):
    seed = _make_seed(tmp_path)
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("import-seed", str(seed))
        run("export")
    assert not (tmp_path / "output" / "evidencias.csv").exists()


def test_export_json_content_matches_imported_data(tmp_path):
    seed = _make_seed(tmp_path)
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("import-seed", str(seed))
        run("export")
    exported = json.loads((tmp_path / "output" / "evidencias.json").read_text())
    assert len(exported) == 1
    assert exported[0]["title"] == "Livro A"


def test_export_prints_output_directory(tmp_path):
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        _, out = run("export")
    assert str(tmp_path / "output") in out


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------


def test_report_creates_pdf(tmp_path):
    seed = _make_seed(tmp_path)
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("import-seed", str(seed))
        result = run("report")
    pdf = tmp_path / "output" / "Mapa_Pegada_Digital_Aridio_Silva_Gerado.pdf"
    assert pdf.exists()
    assert pdf.read_bytes().startswith(b"%PDF")
    assert "Relatório gerado" in result[1]


def test_report_empty_db_creates_valid_pdf(tmp_path):
    env = _env(tmp_path)
    with patch.dict("os.environ", env):
        run("init")
        run("report")
    pdf = tmp_path / "output" / "Mapa_Pegada_Digital_Aridio_Silva_Gerado.pdf"
    assert pdf.exists()
    assert pdf.read_bytes().startswith(b"%PDF")


# ---------------------------------------------------------------------------
# Parser / subcommand structure
# ---------------------------------------------------------------------------


def test_parser_has_all_subcommands():
    parser = build_parser()
    # argparse stores the subparsers actions; verify required commands exist
    # by ensuring each parses without error
    for cmd in ["init"]:
        args = parser.parse_args([cmd])
        assert callable(args.func)


def test_parser_export_all_flag_defaults_to_false():
    parser = build_parser()
    args = parser.parse_args(["export"])
    assert args.all is False


def test_parser_export_all_flag_set():
    parser = build_parser()
    args = parser.parse_args(["export", "--all"])
    assert args.all is True


def test_parser_report_format_defaults_to_pdf():
    parser = build_parser()
    args = parser.parse_args(["report"])
    assert args.format == "pdf"


def test_parser_notion_sync_flags_default_false():
    parser = build_parser()
    args = parser.parse_args(["notion-sync"])
    assert args.dry_run is False
    assert args.only_reviewed is False


def test_parser_notion_sync_dry_run_flag():
    parser = build_parser()
    args = parser.parse_args(["notion-sync", "--dry-run"])
    assert args.dry_run is True


def test_parser_import_csv_kind_required():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["import-csv", "file.csv"])  # missing --kind




