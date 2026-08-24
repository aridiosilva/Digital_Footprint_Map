from __future__ import annotations

import os
import tomllib
from pathlib import Path


def load_config(path: str | Path) -> dict:
    with Path(path).open("rb") as handle:
        return tomllib.load(handle)


def db_path() -> Path:
    return Path(os.getenv("PEGADA_DB", "data/pegada.sqlite3"))


def output_path() -> Path:
    return Path(os.getenv("PEGADA_OUTPUT", "output"))
