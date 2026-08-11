#!/usr/bin/env python3
"""Fail closed if a banked package member differs from PACKAGE_SHA256SUMS.tsv."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    with (HERE / "PACKAGE_SHA256SUMS.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert rows and len({row["path"] for row in rows}) == len(rows)
    for row in rows:
        path = HERE / row["path"]
        assert path.is_file(), row["path"]
        assert path.stat().st_size == int(row["size"]), row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]
    actual = {
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name != "PACKAGE_SHA256SUMS.tsv" and not path.name.endswith(".pyc")
    }
    expected = {row["path"] for row in rows}
    assert actual == expected, sorted(actual ^ expected)
    print(f"PASS: {len(rows)} package files verified")


if __name__ == "__main__":
    main()
