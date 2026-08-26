# Design — FEAT-ID-PREFIX: Feature Sequential ID Standard

## Renumbering Map

| Old ID | New ID | Spec directory |
|---|---|---|
| F-0001 | F-0001 | evidence-model |
| F-0002 | F-0002 | auditable-database |
| F-0003 | F-0003 | evidence-collectors |
| F-0004 | F-0004 | evidence-importers |
| F-0005 | F-0005 | evidence-exporters |
| F-0006 | F-0006 | pdf-report |
| F-0007 | F-0007 | notion-sync |
| F-0008 | F-0008 | cli-interface |

---

## Files to Update

### `.kiro/specs/SPEC.md`
- Features table: IDs column `F-0001`…`F-0008` → `F-0001`…`F-0008`
- References in text

### Per-feature spec files (24 files total — 3 per feature × 8 features)
Pattern: `# Requirements — F-XX:` → `# Requirements — F-XXXX:`
Same for design.md and tasks.md headings.
In-body references: `(F-0004)`, `(F-0006)` etc. → updated format.

### `.kiro/steering/project-conventions.md`
Add explicit statement of the `F-XXXX` standard.

---

## No Source Code Changes

Feature IDs are documentation-only identifiers. No Python source files
reference them. This change is purely in `.kiro/` and `docs/`.

---

## Validation

After the change, `grep -r "F-0[1-9][^0-9]" .kiro/` should return zero results
(all old two-digit IDs replaced).
