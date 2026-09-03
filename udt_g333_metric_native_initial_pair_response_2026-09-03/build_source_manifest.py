#!/usr/bin/env python3
"""Build the exact G333 source manifest from SOURCE_SCOPE.tsv."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows = list(csv.DictReader((PACKAGE / "SOURCE_SCOPE.tsv").open(encoding="utf-8"), delimiter="\t"))
    output = ["source_id\tpath\tbytes\tsha256"]
    for row in rows:
        path = REPO / row["path"]
        if not path.is_file():
            raise SystemExit(f"missing source: {row['path']}")
        output.append(f"{row['source_id']}\t{row['path']}\t{path.stat().st_size}\t{digest(path)}")
    (PACKAGE / "SOURCE_MANIFEST.tsv").write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"G333 source manifest PASS: {len(rows)} sources")


if __name__ == "__main__":
    main()
