#!/usr/bin/env python3
"""Verify a sealed G333 review intake without modifying it."""

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
    intake = Path(args.intake).resolve()
    manifest = intake / "REVIEW_MANIFEST.tsv"
    seal = intake / "REVIEW_MANIFEST.sha256"
    expected_seal = f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n"
    if seal.read_text(encoding="utf-8") != expected_seal:
        raise SystemExit("detached manifest seal mismatch")
    rows = list(csv.DictReader(manifest.open(encoding="utf-8"), delimiter="\t"))
    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"unsafe path: {relative}")
        path = (intake / relative).resolve()
        if not path.is_relative_to(intake):
            raise SystemExit(f"escaped path: {relative}")
        if not path.is_file():
            raise SystemExit(f"missing path: {relative}")
        if path.stat().st_size != int(row["bytes"]) or digest(path) != row["sha256"]:
            raise SystemExit(f"manifest mismatch: {relative}")
    print(f"G333 intake PASS: {len(rows)} payloads")


if __name__ == "__main__":
    main()
