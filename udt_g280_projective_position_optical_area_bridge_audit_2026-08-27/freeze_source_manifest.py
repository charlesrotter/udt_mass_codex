#!/usr/bin/env python3
"""Freeze the exact G280 source universe."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with (PACKAGE / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        scope = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for item in scope:
        path = ROOT / item["path"]
        if not path.is_file():
            raise SystemExit(f"missing source: {item['path']}")
        rows.append(
            {
                "path": item["path"],
                "role": item["role"],
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("path", "role", "bytes", "sha256"), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS: froze {len(rows)} G280 sources")


if __name__ == "__main__":
    main()
