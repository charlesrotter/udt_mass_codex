#!/usr/bin/env python3
"""Freeze the exact 50-file intake already reviewed externally."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("intake", type=Path)
    args = parser.parse_args()
    intake = args.intake.resolve()
    files = sorted(p for p in intake.rglob("*") if p.is_file())
    package = [p for p in files if p.relative_to(intake).parts[0] == PACKAGE]
    sources = [p for p in files if p.relative_to(intake).parts[0] == "sources"]
    assert len(files) == 50 and len(package) == 28 and len(sources) == 22
    with (HERE / "REVIEWED_INTAKE_SHA256SUMS.tsv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=("path", "size", "sha256"), delimiter="\t", lineterminator="\n")
        w.writeheader()
        for path in files:
            w.writerow({
                "path": path.relative_to(intake).as_posix(),
                "size": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    print("PASS reviewed-intake files=50 package=28 sources=22")


if __name__ == "__main__":
    main()
