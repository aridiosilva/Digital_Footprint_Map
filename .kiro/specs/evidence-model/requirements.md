# Requirements — F-0001: Evidence Model & Fingerprint

## Introduction

Defines the canonical data structure (`Evidence`) that represents a single
piece of collected evidence about a person's digital footprint, along with the
deterministic deduplication mechanism based on SHA-256 fingerprinting.

---

## Glossary

| Term | Definition |
|---|---|
| Evidence | A single auditable record of a publicly accessible digital artefact |
| Fingerprint | SHA-256 hash of `url.lower() \| title.lower() \| category` used for deduplication |
| Identity status | Classification of whether the evidence is attributed to the correct person |
| Confidence | Float in [0, 1] expressing strength of identity attribution |

---

## Requirements

### Requirement 1: Evidence Data Structure

**User Story:** As a developer, I want a typed data structure that holds all
fields of an evidence record, so that every layer of the system works with the
same schema.

#### Acceptance Criteria

1. WHEN an `Evidence` is instantiated with `title`, `url`, and `source` THEN the
   object is created without error.
2. THE `Evidence` dataclass SHALL use `slots=True` to reduce memory overhead.
3. THE `Evidence` dataclass SHALL provide default values for every optional
   field: `category="web"`, `snippet=""`, `published_at=None`, `authors=[]`,
   `identifiers={}`, `identity_status="pending"`, `confidence=0.5`, `notes=""`.
4. THE `collected_at` field SHALL default to the current UTC timestamp in ISO
   8601 format with second precision.
5. WHEN `authors` or `identifiers` defaults are used THEN each instance SHALL
   receive independent mutable objects (no shared-default mutation).

### Requirement 2: Deterministic Fingerprint

**User Story:** As a system operator, I want a stable unique key per evidence
record, so that re-collecting the same artefact never creates a duplicate.

#### Acceptance Criteria

1. THE `fingerprint` property SHALL return the hex-encoded SHA-256 digest of
   the string `"{url.strip().lower()}|{title.strip().lower()}|{category}"`.
2. WHEN two `Evidence` objects have the same URL (case-insensitive, stripped)
   and the same title (case-insensitive, stripped) and the same category THEN
   their fingerprints SHALL be equal.
3. WHEN any of URL, title, or category differ THEN the fingerprints SHALL
   differ.
4. THE fingerprint digest SHALL always be exactly 64 hexadecimal characters.
5. THE fingerprint SHALL NOT be stored as a dataclass field; it SHALL be
   computed on demand via a property.

### Requirement 3: Serialisation

**User Story:** As a developer, I want to convert an `Evidence` to a plain
dictionary, so that it can be stored, exported, and transmitted.

#### Acceptance Criteria

1. WHEN `to_dict()` is called THEN the result SHALL contain all dataclass
   fields as dictionary keys plus a `"fingerprint"` key.
2. THE serialised `authors` field SHALL be a Python list of strings.
3. THE serialised `identifiers` field SHALL be a Python dict.
4. WHEN the same `Evidence` instance is serialised twice THEN both results
   SHALL be equal.

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-01 | `fingerprint(e)` is pure: same inputs → same 64-char hex string |
| P-02 | Normalisation: `Evidence(url=U, title=T)` and `Evidence(url=U.upper().strip(), title=" "+T+" ")` have equal fingerprints |
| P-03 | `to_dict()["fingerprint"] == e.fingerprint` always holds |
| P-04 | `confidence` is always in [0.0, 1.0] when set by collectors |
