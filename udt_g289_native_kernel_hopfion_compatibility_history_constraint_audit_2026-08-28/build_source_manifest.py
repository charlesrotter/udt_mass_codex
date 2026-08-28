#!/usr/bin/env python3
"""Build the exact G289 source manifest from SOURCE_SCOPE.tsv."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    rows = []
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = ROOT / row["source"]
            if not source.is_file():
                raise FileNotFoundError(source)
            rows.append((row["source"], sha256(source), row["role"]))
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source", "sha256", "role"))
        writer.writerows(rows)
    print(f"PASS sources={len(rows)}")


if __name__ == "__main__":
    main()
