#!/usr/bin/env python3
"""Freeze exact G294 declared source hashes."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def main() -> None:
    rows: list[dict[str, str]] = []
    with (PACKAGE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            payload = path.read_bytes()
            rows.append(
                {
                    "path": row["path"],
                    "role": row["role"],
                    "bytes": str(len(payload)),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
            )
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("path", "role", "bytes", "sha256"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"frozen_sources={len(rows)}")


if __name__ == "__main__":
    main()
