#!/usr/bin/env python3
"""Verify a sealed G324 review intake without writing to it."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = Path(__file__).resolve().parent
    intake = package.parent
    manifest = intake / "REVIEW_MANIFEST.tsv"
    seal = intake / "REVIEW_MANIFEST.sha256"
    expected_seal, expected_name = seal.read_text().strip().split(maxsplit=1)
    assert expected_name == "REVIEW_MANIFEST.tsv"
    assert sha(manifest) == expected_seal
    with manifest.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        path = intake / row["relative_path"]
        assert path.is_file(), row["relative_path"]
        assert int(row["bytes"]) == path.stat().st_size, row["relative_path"]
        assert sha(path) == row["sha256"], row["relative_path"]
    print(f"PASS sealed_payloads={len(rows)} manifest_sha256={expected_seal}")


if __name__ == "__main__":
    main()
