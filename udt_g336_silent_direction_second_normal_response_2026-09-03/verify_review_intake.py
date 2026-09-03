#!/usr/bin/env python3
"""Verify a sealed G336 review intake without modifying it."""

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
    manifest = intake / "REVIEW_MANIFEST.tsv"
    seal = intake / "REVIEW_MANIFEST.sha256"
    expected_seal = f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n"
    if seal.read_text(encoding="utf-8") != expected_seal:
        raise SystemExit("detached manifest seal mismatch")
    rows = list(csv.DictReader(manifest.open(encoding="utf-8"), delimiter="\t"))
    expected = {Path("REVIEW_MANIFEST.tsv"), Path("REVIEW_MANIFEST.sha256")}
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
        expected.add(relative)
    actual = {path.relative_to(intake) for path in intake.rglob("*") if path.is_file()}
    if actual != expected:
        raise SystemExit(
            f"sealed file-set mismatch: extras={sorted(actual-expected)}, missing={sorted(expected-actual)}"
        )
    print(f"G336 intake PASS: {len(rows)} payloads")


if __name__ == "__main__":
    main()
