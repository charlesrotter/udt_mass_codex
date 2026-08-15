#!/usr/bin/env python3
"""Build and immediately verify the compact G99 result manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "RESULT_MANIFEST.tsv"
EXCLUDED = {"RESULT_MANIFEST.tsv", "MANIFEST_VERIFICATION.txt"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    files = sorted(
        path
        for path in HERE.iterdir()
        if path.is_file() and path.name not in EXCLUDED
    )
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        for path in files:
            writer.writerow((path.name, path.stat().st_size, digest(path)))

    with OUTPUT.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = HERE / row["path"]
        if path.stat().st_size != int(row["bytes"]) or digest(path) != row["sha256"]:
            raise AssertionError(f"result manifest mismatch: {row['path']}")
    (HERE / "MANIFEST_VERIFICATION.txt").write_text(
        f"PASS G99 result manifest {len(rows)}/{len(rows)}\n", encoding="utf-8"
    )
    print(f"PASS G99 result manifest {len(rows)}/{len(rows)}")


if __name__ == "__main__":
    main()
