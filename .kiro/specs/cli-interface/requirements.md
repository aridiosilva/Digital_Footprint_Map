# Requirements — F-08: CLI Interface

## Introduction

The `pegada` command-line interface is the single entry point for all
operations: database initialisation, data import, automated collection, export,
report generation, and Notion synchronisation. Each operation is a subcommand
with its own arguments.

---

## Glossary

| Term | Definition |
|---|---|
| Subcommand | A named CLI verb (e.g. `pegada collect`) |
| `PEGADA_DB` | Environment variable overriding the default database path |
| `PEGADA_OUTPUT` | Environment variable overriding the default output directory |

---

## Requirements

### Requirement 1: Subcommand Structure

**User Story:** As a CLI user, I want a single `pegada` command with named
subcommands, so that operations are discoverable and self-documented.

#### Acceptance Criteria

1. THE CLI entry point SHALL be registered as `pegada` in `pyproject.toml`
   pointing to `pegada.cli:main`.
2. WHEN `pegada` is run without a subcommand THEN it SHALL print help and exit
   with a non-zero status.
3. THE CLI SHALL provide the following subcommands: `init`, `import-seed`,
   `import-csv`, `collect`, `export`, `report`, `notion-sync`.

### Requirement 2: `init` Subcommand

**User Story:** As a new user, I want to initialise the database and output
directory in one command, so that setup is a single step.

#### Acceptance Criteria

1. WHEN `pegada init` is run THEN the database SHALL be initialised and the
   output directory SHALL be created.
2. WHEN `pegada init` is run on an already-initialised system THEN it SHALL be
   idempotent (no error, no data loss).
3. AFTER `pegada init` the command SHALL print the database path.

### Requirement 3: `import-seed` Subcommand

**User Story:** As a researcher, I want to load a seed JSON file, so that the
database is pre-populated for offline use or demonstrations.

#### Acceptance Criteria

1. WHEN `pegada import-seed <path>` is run THEN all records in the JSON SHALL
   be upserted into the database.
2. AFTER import the command SHALL print the count of imported records.

### Requirement 4: `import-csv` Subcommand

**User Story:** As a researcher, I want to import a CSV file with a specific
evidence category, so that manual data from external tools is included.

#### Acceptance Criteria

1. WHEN `pegada import-csv <path> --kind <category>` is run THEN all rows in
   the CSV SHALL be upserted with the specified category.
2. THE `--kind` argument SHALL be required.
3. AFTER import the command SHALL print the count of imported records.

### Requirement 5: `collect` Subcommand

**User Story:** As a researcher, I want to run all enabled collectors from a
config file, so that sources are collected in one step.

#### Acceptance Criteria

1. WHEN `pegada collect --config <path>` is run THEN all enabled sources in
   the TOML file SHALL be collected.
2. THE `--config` argument SHALL default to `config/collector.toml`.
3. IF a collector fails THEN the error SHALL be printed and collection SHALL
   continue with the remaining sources.
4. AFTER collection the command SHALL print the total count of
   collected/updated records.

### Requirement 6: `export` Subcommand

**User Story:** As a researcher, I want to export all evidence to files, so
that I can share or analyse the data outside the tool.

#### Acceptance Criteria

1. WHEN `pegada export` is run THEN `evidencias.json` SHALL always be written.
2. WHEN `pegada export --all` is run THEN `evidencias.csv` and
   `mapa_pegada_digital.md` SHALL also be written.
3. AFTER export the command SHALL print the output directory path.

### Requirement 7: `report` Subcommand

**User Story:** As a researcher, I want to generate a PDF report from the
current database state.

#### Acceptance Criteria

1. WHEN `pegada report` or `pegada report --format pdf` is run THEN the PDF
   SHALL be generated in the output directory.
2. AFTER generation the command SHALL print the full path of the generated PDF.

### Requirement 8: `notion-sync` Subcommand

**User Story:** As an operator, I want to sync evidence to Notion explicitly
and safely.

#### Acceptance Criteria

1. WHEN `pegada notion-sync` is run THEN all evidence SHALL be synced to Notion.
2. WHEN `--only-reviewed` is passed THEN only evidence with
   `identity_status="reviewed"` SHALL be synced.
3. WHEN `--dry-run` is passed THEN nothing SHALL be written to Notion and the
   command SHALL print "Simulação concluída".
4. AFTER sync the command SHALL print counts of created and updated records.

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-29 | `pegada init` followed by `pegada init` → no error, same db path printed |
| P-30 | `pegada import-seed <path>` → printed count matches JSON array length |
| P-31 | `pegada export` always produces `evidencias.json` in output dir |
| P-32 | `pegada collect` with a failing source → remaining sources still run |
