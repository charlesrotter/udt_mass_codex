#!/usr/bin/env python3
"""Authenticate a sealed G330 review intake without writing to it."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    manifest = root / "REVIEW_MANIFEST.tsv"
    seal = root / "REVIEW_MANIFEST.sha256"
    if not manifest.is_file() or not seal.is_file():
        raise SystemExit("missing manifest or detached seal")
    seal_fields = seal.read_text(encoding="utf-8").strip().split()
    if len(seal_fields) != 2 or seal_fields[1] != "REVIEW_MANIFEST.tsv":
        raise SystemExit("malformed detached seal")
    if digest(manifest) != seal_fields[0]:
        raise SystemExit("manifest seal mismatch")
    rows = list(csv.DictReader(manifest.open(encoding="utf-8"), delimiter="\t"))
    expected = {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"unsafe manifest path: {row['path']}")
        path = root / relative
        if not path.is_file():
            raise SystemExit(f"missing payload: {row['path']}")
        if path.stat().st_size != int(row["bytes"]):
            raise SystemExit(f"payload byte mismatch: {row['path']}")
        if digest(path) != row["sha256"]:
            raise SystemExit(f"payload hash mismatch: {row['path']}")
        expected.add(relative.as_posix())
    found = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and ".review_runtime" not in path.relative_to(root).parts
    }
    unexpected = sorted(found - expected)
    missing = sorted(expected - found)
    if unexpected or missing:
        raise SystemExit(f"sealed tree mismatch: unexpected={unexpected}; missing={missing}")
    print(f"G330 sealed intake authentication PASS: {len(rows)} payloads; {len(found)} files")


if __name__ == "__main__":
    main()
