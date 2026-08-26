# Design — F-03: Evidence Collectors

## Component

`src/pegada/collectors.py`

---

## Class Hierarchy

```
Collector (ABC)
└── collect() → list[Evidence]   ← abstract

WebCollector(Collector)
├── __init__(url, source, user_agent, timeout=20, delay=1, respect_robots=True)
├── _allowed() → bool            ← checks robots.txt
└── collect() → list[Evidence]

GitHubCollector(Collector)
├── __init__(username, token=None)
└── collect() → list[Evidence]   ← profile + repos

OpenAlexCollector(Collector)
├── __init__(query)
└── collect() → list[Evidence]
```

---

## Helper: `get_json(url, headers, timeout) → Any`

Module-level function using `urllib.request` stdlib.
No `requests` dependency. Returns parsed JSON or raises on HTTP/network errors.

---

## HTML Parsing: `PageParser(HTMLParser)`

Extracts:
- `<title>` text → `self.title`
- `<meta name="description" content="…">` → `self.description`
- All visible text → `self.text` (for snippet fallback)

---

## WebCollector Flow

```
_allowed()
  ├── respect_robots=False → return True
  └── respect_robots=True  → fetch /robots.txt → RobotFileParser.can_fetch()
      └── OSError (robots unreachable) → return False (safe default)

collect()
  ├── not _allowed() → return []
  ├── sleep(delay)
  ├── urllib.request.urlopen(url, User-Agent header)
  ├── PageParser.feed(html)
  ├── title = parser.title or final_url
  ├── snippet = parser.description or text[:500], truncated at 1000
  └── return [Evidence(…, confidence=0.45)]
```

---

## GitHubCollector Flow

```
collect()
  ├── GET /users/{username}       → profile data
  ├── GET /users/{username}/repos?per_page=100&sort=updated → repo list
  ├── profile Evidence: category="profile", status="reviewed", confidence=0.8
  └── per repo Evidence: category="repository", confidence=0.75
```

---

## OpenAlexCollector Flow

```
collect()
  ├── GET https://api.openalex.org/works?search={query}&per-page=25
  └── per work: category="academic", confidence=0.35,
        url = doi || openalex_id,
        authors from authorships,
        identifiers = {"openalex": id},
        notes = "Candidato: confirmar autoria/homônimo."
```

---

## Error Handling Strategy

Collectors do NOT catch errors internally.
The CLI (`cmd_collect`) wraps each collector in a try/except for:
`HTTPError, JSONDecodeError, KeyError, OSError, TypeError, URLError`
→ prints failure message and continues to next source.

---

## Dependencies

- `urllib.request`, `urllib.robotparser`, `urllib.parse` (stdlib)
- `html.parser` (stdlib)
- `json`, `time`, `abc` (stdlib)
- `pegada.models.Evidence`

---

## Configuration Integration

`WebCollector` parameters (`user_agent`, `timeout_seconds`, `delay_seconds`,
`respect_robots_txt`) come from the `[collection]` section of `collector.toml`
passed through `cmd_collect` in `cli.py`.
