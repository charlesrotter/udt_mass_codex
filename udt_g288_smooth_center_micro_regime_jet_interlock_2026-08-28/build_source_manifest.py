#!/usr/bin/env python3
"""Build the frozen G288 source manifest from SOURCE_SCOPE.tsv."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    rows = []
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["source"]
            if not path.is_file():
                raise FileNotFoundError(path)
            rows.append((row["source"], sha256(path), row["role"]))
    out = HERE / "SOURCE_MANIFEST.tsv"
    with out.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("source", "sha256", "role"))
        writer.writerows(rows)
    print(f"PASS sources={len(rows)}")


if __name__ == "__main__":
    main()

