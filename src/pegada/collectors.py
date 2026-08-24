from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
import urllib.robotparser
from abc import ABC, abstractmethod
from html.parser import HTMLParser
from typing import Any

from .models import Evidence


def get_json(url: str, headers: dict[str, str] | None = None, timeout: float = 20) -> Any:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title: list[str] = []
        self.text: list[str] = []
        self.description = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag.lower() == "title": self.in_title = True
        if tag.lower() == "meta" and values.get("name", "").lower() == "description":
            self.description = values.get("content") or ""

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title": self.in_title = False

    def handle_data(self, data: str) -> None:
        clean = " ".join(data.split())
        if clean:
            self.text.append(clean)
            if self.in_title: self.title.append(clean)


class Collector(ABC):
    @abstractmethod
    def collect(self) -> list[Evidence]: ...


class WebCollector(Collector):
    def __init__(self, url: str, source: str, user_agent: str, timeout: float = 20,
                 delay: float = 1, respect_robots: bool = True):
        self.url, self.source, self.user_agent = url, source, user_agent
        self.timeout, self.delay, self.respect_robots = timeout, delay, respect_robots

    def _allowed(self) -> bool:
        if not self.respect_robots: return True
        robots = urllib.robotparser.RobotFileParser()
        parsed = urllib.parse.urlsplit(self.url)
        robots.set_url(urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "/robots.txt", "", "")))
        try:
            robots.read(); return robots.can_fetch(self.user_agent, self.url)
        except OSError:
            return False

    def collect(self) -> list[Evidence]:
        if not self._allowed(): return []
        time.sleep(max(0, self.delay))
        request = urllib.request.Request(self.url, headers={"User-Agent": self.user_agent})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            final_url = response.geturl(); html = response.read().decode("utf-8", errors="replace")
        parser = PageParser(); parser.feed(html)
        title = " ".join(parser.title) or final_url
        snippet = parser.description or " ".join(parser.text)[:500]
        return [Evidence(title=title, url=final_url, source=self.source,
                         snippet=snippet[:1000], confidence=0.45)]


class GitHubCollector(Collector):
    def __init__(self, username: str, token: str | None = None): self.username, self.token = username, token

    def collect(self) -> list[Evidence]:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "PegadaDigital/1.0"}
        if self.token: headers["Authorization"] = f"Bearer {self.token}"
        base = f"https://api.github.com/users/{urllib.parse.quote(self.username)}"
        data = get_json(base, headers)
        repos = get_json(f"{base}/repos?per_page=100&sort=updated", headers)
        items = [Evidence(title=f"Perfil GitHub: {data.get('name') or self.username}",
                          url=data["html_url"], source="GitHub", category="profile",
                          snippet=data.get("bio") or "", confidence=0.8, identity_status="reviewed")]
        for repo in repos:
            items.append(Evidence(title=repo["name"], url=repo["html_url"], source="GitHub",
                                  category="repository", snippet=repo.get("description") or "",
                                  published_at=repo.get("created_at"), confidence=0.75))
        return items


class OpenAlexCollector(Collector):
    def __init__(self, query: str): self.query = query

    def collect(self) -> list[Evidence]:
        params = urllib.parse.urlencode({"search": self.query, "per-page": 25})
        payload = get_json(f"https://api.openalex.org/works?{params}", {"User-Agent": "PegadaDigital/1.0"})
        items = []
        for work in payload.get("results", []):
            authors = [a["author"]["display_name"] for a in work.get("authorships", [])]
            items.append(Evidence(title=work.get("display_name") or "Sem título",
                                  url=work.get("doi") or work.get("id"), source="OpenAlex",
                                  category="academic", published_at=str(work.get("publication_year") or ""),
                                  authors=authors, identifiers={"openalex": work.get("id", "")},
                                  confidence=0.35, notes="Candidato: confirmar autoria/homônimo."))
        return items
