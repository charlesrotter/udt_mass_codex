#!/usr/bin/env python3
"""Freeze preregistered controlling-source bytes."""

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
        rows = list(csv.DictReader(handle, delimiter="\t"))
    output = []
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise SystemExit(f"missing source: {row['path']}")
        output.append({
            "source_id": row["source_id"],
            "path": row["path"],
            "bytes": str(path.stat().st_size),
            "sha256": digest(path),
        })
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["source_id", "path", "bytes", "sha256"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    main()
