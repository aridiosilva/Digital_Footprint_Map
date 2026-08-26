# Requirements — F-0003: Evidence Collectors

## Introduction

Automated collectors that fetch publicly accessible evidence from GitHub,
OpenAlex, and generic web pages. Each collector runs independently; a failure
in one SHALL NOT abort the others.

---

## Glossary

| Term | Definition |
|---|---|
| Collector | A class that fetches public data from a specific source and returns `list[Evidence]` |
| robots.txt | Standard file that declares which paths a crawler may access |
| Candidate | Evidence with `identity_status="pending"` requiring human validation |
| Rate limiting | Deliberate delay between HTTP requests to be a polite crawler |

---

## Requirements

### Requirement 1: Collector Abstraction

**User Story:** As a developer, I want all collectors to share a common
interface, so that new sources can be added without changing the collection
pipeline.

#### Acceptance Criteria

1. THE system SHALL define an abstract base class `Collector` with an abstract
   method `collect() → list[Evidence]`.
2. EVERY concrete collector SHALL implement `collect()` and return a
   `list[Evidence]`.
3. WHEN a collector encounters a network or parsing error THEN it SHALL raise
   the exception (the CLI layer handles isolation, not the collector itself).

### Requirement 2: Web Page Collector

**User Story:** As a researcher, I want to collect a public web page's title
and description as evidence, so that I can record manually confirmed URLs.

#### Acceptance Criteria

1. WHEN `WebCollector.collect()` is called THEN it SHALL first check
   `robots.txt` at the root of the URL's origin.
2. IF `robots.txt` disallows the configured `user_agent` for the target URL
   THEN `collect()` SHALL return an empty list without raising an error.
3. WHEN fetching is allowed THEN `collect()` SHALL sleep `delay` seconds before
   making the request.
4. THE collector SHALL parse the HTML `<title>` tag as the evidence title.
5. THE collector SHALL use the `<meta name="description">` content as the
   snippet, falling back to the first 500 characters of visible text.
6. THE snippet SHALL be truncated to 1000 characters maximum.
7. THE returned `Evidence` SHALL have `confidence=0.45`.
8. THE collector SHALL follow HTTP redirects and use the final URL.

### Requirement 3: GitHub Collector

**User Story:** As a researcher, I want to collect a public GitHub user's
profile and repositories as evidence, so that the map includes technical
contributions.

#### Acceptance Criteria

1. WHEN `GitHubCollector.collect()` is called THEN it SHALL call the GitHub
   REST API at `GET /users/{username}` and `GET /users/{username}/repos`.
2. THE profile evidence SHALL have `category="profile"`,
   `identity_status="reviewed"`, and `confidence=0.8`.
3. EACH repository SHALL become a separate evidence with
   `category="repository"` and `confidence=0.75`.
4. IF a GitHub token is provided THEN it SHALL be sent in the
   `Authorization: Bearer <token>` header.
5. THE `Accept: application/vnd.github+json` header SHALL always be set.

### Requirement 4: OpenAlex Collector

**User Story:** As a researcher, I want to search OpenAlex for academic works
by name, so that the map includes publication candidates for review.

#### Acceptance Criteria

1. WHEN `OpenAlexCollector.collect()` is called THEN it SHALL query
   `https://api.openalex.org/works` with `search=<query>&per-page=25`.
2. EACH result SHALL be returned as an evidence with `category="academic"`,
   `confidence=0.35`, and a note stating it is a candidate requiring validation.
3. THE `authors` field SHALL be populated from `authorships[*].author.display_name`.
4. THE `identifiers` dict SHALL include `{"openalex": "<work_id>"}`.
5. IF the work has a DOI THEN the DOI SHALL be used as the `url`; otherwise
   the OpenAlex work ID SHALL be used.

### Requirement 5: Ethical Collection Rules

**User Story:** As a project operator, I want the tool to follow ethical
collection practices, so that it complies with site policies and LGPD.

#### Acceptance Criteria

1. THE system SHALL NOT attempt to bypass authentication, CAPTCHAs, or access
   controls.
2. THE `WebCollector` SHALL respect `robots.txt` by default
   (`respect_robots=True`).
3. THE minimum delay between requests SHALL be configurable and default to 1.0
   second.
4. ALL collectors SHALL identify themselves with a descriptive `User-Agent`
   string.

---

## Correctness Properties (Property-Based Testing)

| ID | Property |
|---|---|
| P-09 | Every `Evidence` returned by any collector has non-empty `title`, `url`, `source` |
| P-10 | `WebCollector` with `respect_robots=True` and a disallowing robots.txt returns `[]` |
| P-11 | OpenAlex results always have `confidence <= 0.5` (candidates, not confirmed) |
| P-12 | GitHub profile evidence always has `identity_status="reviewed"` |
