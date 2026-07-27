#!/usr/bin/env python3
"""Replay the preregistered source identities without modifying files."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).resolve().parent / "SOURCE_MANIFEST.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 21
    assert len({row["path"] for row in rows}) == len(rows)
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        assert sha256(path) == row["sha256"], row["path"]
    print(f"PASS source_manifest {len(rows)}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

