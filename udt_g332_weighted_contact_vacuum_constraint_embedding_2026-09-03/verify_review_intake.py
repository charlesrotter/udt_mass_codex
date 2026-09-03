#!/usr/bin/env python3
"""Verify a sealed G332 review intake without mutating it."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("intake")
    args = parser.parse_args()
    root = Path(args.intake).resolve()
    manifest = root / "REVIEW_MANIFEST.tsv"
    seal = root / "REVIEW_MANIFEST.sha256"
    if not manifest.is_file() or not seal.is_file():
        raise SystemExit("missing manifest or seal")
    expected = seal.read_text(encoding="utf-8").split()[0]
    if digest(manifest) != expected:
        raise SystemExit("manifest seal mismatch")
    rows = list(csv.DictReader(manifest.open(encoding="utf-8"), delimiter="\t"))
    for row in rows:
        path = root / row["path"]
        if not path.is_file():
            raise SystemExit(f"missing payload: {row['path']}")
        if path.stat().st_size != int(row["bytes"]) or digest(path) != row["sha256"]:
            raise SystemExit(f"payload mismatch: {row['path']}")
    print(f"G332 review intake PASS: {len(rows)} manifest payloads")


if __name__ == "__main__":
    main()
