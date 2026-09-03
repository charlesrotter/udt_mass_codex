#!/usr/bin/env python3
"""Verify an exact sealed G337 review intake without modifying it."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("intake")
    args = parser.parse_args()
    intake = Path(args.intake).resolve()
    manifest, seal = intake / "REVIEW_MANIFEST.tsv", intake / "REVIEW_MANIFEST.sha256"
    if seal.read_text(encoding="utf-8") != f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n":
        raise SystemExit("detached manifest seal mismatch")
    rows = list(csv.DictReader(manifest.open(encoding="utf-8"), delimiter="\t"))
    expected = {Path("REVIEW_MANIFEST.tsv"), Path("REVIEW_MANIFEST.sha256")}
    for row in rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"unsafe path: {relative}")
        path = (intake / relative).resolve()
        if not path.is_relative_to(intake) or not path.is_file():
            raise SystemExit(f"missing or escaped path: {relative}")
        if path.stat().st_size != int(row["bytes"]) or digest(path) != row["sha256"]:
            raise SystemExit(f"manifest mismatch: {relative}")
        expected.add(relative)
    actual = {path.relative_to(intake) for path in intake.rglob("*") if path.is_file()}
    if actual != expected:
        raise SystemExit(
            f"sealed file-set mismatch: extras={sorted(actual-expected)}, missing={sorted(expected-actual)}"
        )
    print(f"G337 intake PASS: {len(rows)} payloads")


if __name__ == "__main__":
    main()
