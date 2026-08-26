# Requirements — BUG-REGISTRY: Bug Documentation Standard

## Introduction

Establishes the formal bug registry for the project. Every bug found, whether
discovered during testing, code review, or production use, MUST be recorded as
a `BUG-XXXXX` document in `docs/bugs/`. This spec covers the registry structure
and the initial population with the one bug already found and fixed.

---

## Glossary

| Term | Definition |
|---|---|
| BUG-XXXXX | A five-digit zero-padded sequential bug identifier (BUG-00001 to BUG-99999) |
| Bug report | A Markdown document in `docs/bugs/` describing one bug following the standard template |
| Regression | A bug reintroduced after having been fixed |

---

## Requirements

### Requirement 1: Bug Registry Index

**User Story:** As a developer, I want a central index of all known bugs and
their status, so that I can track what has been fixed and what is still open.

#### Acceptance Criteria

1. THE file `docs/bugs/BUG_REGISTRY.md` SHALL exist and serve as the master
   index of all bug reports.
2. EACH row in the registry table SHALL contain: ID, title, affected component,
   severity, status, and the PR that fixed it.
3. THE registry SHALL be updated every time a new bug is added or an existing
   bug changes status.
4. Bug IDs SHALL be assigned sequentially starting at `BUG-00001`; no gaps or
   reuse of IDs is permitted.

### Requirement 2: Bug Report Template

**User Story:** As a developer, I want a standard bug report template, so that
all reports contain consistent and actionable information.

#### Acceptance Criteria

1. EACH bug report SHALL be a Markdown file named `BUG-XXXXX.md` in `docs/bugs/`.
2. EACH report SHALL contain the following sections: ID, Title, Date found,
   Date fixed, Affected component, Severity, Status, Description, Root cause,
   Steps to reproduce, Fix applied, Tests added, and Related PRs.
3. THE `Status` field SHALL be one of: `Open`, `Fixed`, `Verified`, `Wontfix`.
4. THE `Severity` field SHALL be one of: `Critical`, `High`, `Medium`, `Low`.

### Requirement 3: Initial Population — BUG-00001

**User Story:** As a project maintainer, I want BUG-00001 documented, so that
the bug found during test implementation is formally recorded.

#### Acceptance Criteria

1. THE file `docs/bugs/BUG-00001.md` SHALL exist describing the whitespace
   `confidence` parsing bug found in `src/pegada/importers.py`.
2. THE report SHALL document: the exact failing input (`" "` as confidence
   value), the exception raised (`ValueError`), the root cause (`or` operator
   not stripping whitespace), and the fix applied.
3. THE report status SHALL be `Verified` (found, fixed, and covered by tests).
4. THE report SHALL reference PR #7 as the fixing PR.
