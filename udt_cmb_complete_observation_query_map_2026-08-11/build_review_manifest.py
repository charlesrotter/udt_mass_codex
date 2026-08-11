#!/usr/bin/env python3
"""Build the exact sealed-review manifest from package files and frozen sources."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "REVIEW_MANIFEST.tsv"
EXCLUDE = {"REVIEW_MANIFEST.tsv", "EXTERNAL_REVIEW_RAW.md", "PACKAGE_MANIFEST.sha256"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    package_paths = {
        path.relative_to(ROOT)
        for path in HERE.iterdir()
        if path.is_file() and path.name not in EXCLUDE
    }
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        package_paths.update(Path(row["path"]) for row in csv.DictReader(stream, delimiter="\t"))
    rows = []
    for relative in sorted(package_paths, key=str):
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"missing review file: {relative}")
        rows.append((str(relative), digest(path)))
    with OUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256"))
        writer.writerows(rows)
    print(f"review_manifest_rows={len(rows)}")


if __name__ == "__main__":
    main()
