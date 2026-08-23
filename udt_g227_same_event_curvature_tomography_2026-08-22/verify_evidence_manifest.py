#!/usr/bin/env python3
"""Verify every current file frozen by the G227 evidence manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with (ROOT / "EVIDENCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise SystemExit(f"missing: {row['path']}")
        if digest(path) != row["sha256"]:
            raise SystemExit(f"hash mismatch: {row['path']}")
        if path.stat().st_size != int(row["bytes"]):
            raise SystemExit(f"byte-count mismatch: {row['path']}")
    print(f"PASS: {len(rows)} G227 evidence entries match")


if __name__ == "__main__":
    main()

