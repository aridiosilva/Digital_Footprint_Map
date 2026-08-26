# Design — F-0006: PDF Report Generator

## Component

`src/pegada/report.py`

---

## Entry Point

```python
build_pdf(rows: list[dict], path: Path, subject: str = "Aridio Silva") → None
```

Uses ReportLab `platypus` (flowable document API). Builds a `story` list of
flowables then calls `SimpleDocTemplate.build(story)`.

---

## Document Layout

```
SimpleDocTemplate (A4, margins 1.7cm/1.6cm)
└── story: list[Flowable]
    ├── [Cover page]
    │   ├── Spacer(5cm)
    │   ├── Paragraph("MAPA DA PEGADA DIGITAL", Cover style)
    │   ├── Spacer(0.5cm)
    │   ├── Paragraph(subject, Heading1)
    │   ├── Spacer(1cm)
    │   ├── Paragraph("Relatório auditável…", Normal)
    │   └── PageBreak
    ├── [Executive Summary]
    │   ├── Paragraph("Resumo executivo", Heading1)
    │   ├── Paragraph(f"{len(rows)} evidências…", BodyText)
    │   ├── Spacer(0.4cm)
    │   ├── Table(category counts, colWidths=[12cm, 3cm])
    │   └── PageBreak
    ├── [Evidence section]
    │   ├── Paragraph("Evidências", Heading1)
    │   └── per row:
    │       ├── Paragraph(title, Heading2)
    │       ├── Paragraph(source + category, BodyText)
    │       ├── Paragraph(url, BodyText)
    │       ├── Paragraph(status + confidence, BodyText)
    │       ├── Paragraph(snippet or notes, BodyText)
    │       └── Spacer(0.3cm)
    └── [Methodology]
        ├── PageBreak
        ├── Paragraph("Metodologia e limitações", Heading1)
        └── Paragraph(methodology text, BodyText)
```

---

## Custom Style

```python
ParagraphStyle(
    name="Cover",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=25,
    leading=31,
    textColor=colors.HexColor("#123B5D"),
)
```

---

## Table Style (category summary)

```python
TableStyle([
    ("BACKGROUND", (0,0), (-1,0), HexColor("#123B5D")),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("GRID",       (0,0), (-1,-1), 0.25, colors.grey),
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
    ("PADDING",    (0,0), (-1,-1), 6),
])
```

---

## Dependencies

- `reportlab >=4.2,<5` (production dependency)
- `collections.Counter` (stdlib)
- `pathlib` (stdlib)

---

## Design Decisions

| Decision | Rationale |
|---|---|
| ReportLab platypus | High-level flowable API; handles pagination, page breaks, and tables |
| `subject` parameter | Reusable for any person without code changes |
| `snippet or notes` fallback | Ensures every evidence entry has some descriptive text in the PDF |
| Auto-create parent dir | Consistent with exporter behaviour |
