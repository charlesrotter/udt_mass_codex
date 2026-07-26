#!/usr/bin/env python3
"""Freeze source identities for the completion-scoped map audit."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for row in source_rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise SystemExit(f"missing source: {row['path']}")
        rows.append({**row, "size_bytes": str(path.stat().st_size), "sha256": digest(path)})
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_id", "path", "role", "size_bytes", "sha256"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
