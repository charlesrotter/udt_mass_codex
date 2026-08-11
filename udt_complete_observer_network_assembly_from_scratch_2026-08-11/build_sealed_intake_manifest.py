#!/usr/bin/env python3
"""Freeze exact file identities for the already-created sealed review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("intake", type=Path)
    args = parser.parse_args()
    intake = args.intake.resolve()
    files = sorted(path for path in intake.rglob("*") if path.is_file())
    assert len(files) == 36
    package = [path for path in files if path.relative_to(intake).parts[0] == HERE.name]
    sources = [path for path in files if path.relative_to(intake).parts[0] == "sources"]
    assert len(package) == 21 and len(sources) == 15
    output = HERE / "SEALED_INTAKE_SHA256SUMS.tsv"
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=("path", "size", "sha256"), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for path in files:
            writer.writerow({
                "path": path.relative_to(intake).as_posix(),
                "size": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    print(f"PASS files={len(files)} package={len(package)} sources={len(sources)}")


if __name__ == "__main__":
    main()
