#!/usr/bin/env python3
"""Resolve G277 evidence paths in the repository or a sealed review intake."""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
CONTAINER = PACKAGE.parent
SEALED_MAP = CONTAINER / "SEALED_SOURCE_MAP.tsv"


@lru_cache(maxsize=1)
def _sealed_paths() -> dict[str, Path]:
    if not SEALED_MAP.is_file():
        return {}
    with SEALED_MAP.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    paths = {row["logical_path"]: CONTAINER / row["sealed_path"] for row in rows}
    assert len(paths) == len(rows)
    return paths


def source_path(logical_path: str, repository_root: Path) -> Path:
    sealed = _sealed_paths()
    if sealed:
        assert logical_path in sealed, logical_path
        return sealed[logical_path]
    path = Path(logical_path)
    return path if path.is_absolute() else repository_root / path
