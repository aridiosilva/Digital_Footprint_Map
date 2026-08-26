# Tasks — F-06: PDF Report Generator

## Status: ✅ Implemented (v1.0.0)

---

- [x] 1. Implement `build_pdf(rows, path, subject)` in `src/pegada/report.py`
  - Import ReportLab platypus, lib.styles, lib.pagesizes, lib.units
  - Auto-create parent directory

- [x] 2. Define `Cover` custom paragraph style
  - fontSize=25, TA_CENTER, colour #123B5D

- [x] 3. Build `SimpleDocTemplate` with A4, correct margins, and PDF title metadata

- [x] 4. Assemble cover page flowables (Spacer, Paragraphs, PageBreak)

- [x] 5. Build executive summary section
  - Total count sentence
  - `collections.Counter` for category counts
  - `Table` with styled header row

- [x] 6. Build per-evidence flowables loop

- [x] 7. Append methodology note section

- [x] 8. Wire `build_pdf` into CLI `report` command (`cmd_report`)
  - Output path: `output/Mapa_Pegada_Digital_Aridio_Silva_Gerado.pdf`

- [x] 9. Add smoke test for PDF generation
  - `build_pdf([], tmp_path / "test.pdf")` → file exists, starts with `%PDF`
  - _Implemented in tests/test_report.py (14 tests)_

