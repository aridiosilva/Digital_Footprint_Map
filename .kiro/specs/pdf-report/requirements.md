# Requirements — F-0006: PDF Report Generator

## Introduction

Generates a professionally formatted, multi-page PDF report of the digital
footprint map from a list of evidence dicts. The PDF includes a cover page,
executive summary with category table, per-evidence detail section, and a
methodology note.

---

## Glossary

| Term | Definition |
|---|---|
| Report | A multi-page PDF document summarising all evidence for a subject |
| Subject | The person whose digital footprint is being reported (default: "Aridio Silva") |

---

## Requirements

### Requirement 1: PDF Structure

**User Story:** As a researcher, I want the report to have clear sections so
that it is easy to navigate and present.

#### Acceptance Criteria

1. THE PDF SHALL contain, in order: cover page, executive summary, evidence
   section, and methodology note.
2. THE cover page SHALL display the report title centred and the subject name.
3. THE executive summary SHALL state the total number of evidence records and
   include a table of counts by category.
4. THE evidence section SHALL have one entry per record showing title, source,
   category, URL, identity status, confidence percentage, and snippet or notes.
5. THE methodology note SHALL state that automatic results are candidates
   requiring human validation.

### Requirement 2: PDF Formatting

**User Story:** As a researcher, I want the report to use a consistent visual
style, so that it looks professional.

#### Acceptance Criteria

1. THE page size SHALL be A4.
2. THE cover page title SHALL use font size 25, centred, in colour `#123B5D`.
3. THE category summary table SHALL have a dark header row (`#123B5D`
   background, white text) and gridlines.
4. THE document SHALL use 1.7 cm right/left margins and 1.6 cm top/bottom
   margins.
5. THE PDF metadata `title` property SHALL be set to
   `"Mapa da Pegada Digital — {subject}"`.

### Requirement 3: Output Path

**User Story:** As a CLI user, I want the PDF saved to a predictable path so
that I can find it after generation.

#### Acceptance Criteria

1. WHEN `build_pdf(rows, path)` is called THEN the PDF SHALL be written to
   `path`.
2. WHEN the parent directory of `path` does not exist THEN it SHALL be created
   automatically.

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-21 | `build_pdf` creates a file at the specified path |
| P-22 | The generated file starts with `%PDF` (valid PDF header) |
| P-23 | `build_pdf([])` produces a valid PDF with zero evidence rows and no error |
