# Tasks — F-0003: Evidence Collectors

## Status: ✅ Implemented (v1.0.0)

---

- [x] 1. Define `Collector` abstract base class with `collect()` abstract method
  - `src/pegada/collectors.py`

- [x] 2. Implement `get_json(url, headers, timeout)` module-level helper
  - Use `urllib.request.Request` + `urlopen`; parse with `json.loads`

- [x] 3. Implement `PageParser(HTMLParser)`
  - Extract `<title>`, `<meta name="description">`, and visible text

- [x] 4. Implement `WebCollector`
  - `__init__`: store url, source, user_agent, timeout, delay, respect_robots
  - `_allowed()`: check robots.txt; return `False` on `OSError`
  - `collect()`: gate on `_allowed()`, sleep, fetch, parse, return `[Evidence]`
  - Truncate snippet at 1000 chars; confidence = 0.45

- [x] 5. Implement `GitHubCollector`
  - Fetch profile + repos via GitHub REST API
  - Profile: `category="profile"`, `status="reviewed"`, `confidence=0.8`
  - Repos: `category="repository"`, `confidence=0.75`
  - Support optional Bearer token

- [x] 6. Implement `OpenAlexCollector`
  - Query OpenAlex works endpoint with `per-page=25`
  - `category="academic"`, `confidence=0.35`
  - Populate `authors`, `identifiers`, and candidate note
  - Use DOI as URL when available

- [ ] 7. Write integration smoke tests (manual)
  - Collectors depend on live external services — automated tests not in scope
  - Document manual verification procedure in `docs/MAPA_DO_COLETOR.md`
