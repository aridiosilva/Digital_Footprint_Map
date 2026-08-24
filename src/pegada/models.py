from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(slots=True)
class Evidence:
    title: str
    url: str
    source: str
    category: str = "web"
    snippet: str = ""
    published_at: str | None = None
    authors: list[str] = field(default_factory=list)
    identifiers: dict[str, str] = field(default_factory=dict)
    collected_at: str = field(default_factory=utc_now)
    identity_status: str = "pending"
    confidence: float = 0.5
    notes: str = ""

    @property
    def fingerprint(self) -> str:
        raw = "|".join((self.url.strip().lower(), self.title.strip().lower(), self.category))
        return sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["fingerprint"] = self.fingerprint
        return value
