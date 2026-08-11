#!/usr/bin/env python3
"""Build the deterministic package SHA-256 and size manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_SHA256SUMS.tsv"


def main() -> None:
    files = sorted(
        path for path in HERE.iterdir()
        if path.is_file() and path.name != OUTPUT.name and not path.name.endswith(".pyc")
    )
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=("path", "size", "sha256"), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for path in files:
            writer.writerow({
                "path": path.name,
                "size": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    print(f"PASS: wrote {len(files)} package members")


if __name__ == "__main__":
    main()
