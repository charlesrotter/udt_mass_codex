#!/usr/bin/env python3
"""Build the non-self-referential G70 sealed-review manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = sorted(
        path for path in HERE.iterdir()
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "build_review_manifest.py"}
    )
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = [ROOT / row["path"] for row in csv.DictReader(stream, delimiter="\t")]
    records = [(path, "G70_PACKAGE") for path in package]
    records.extend((path, "CITED_SOURCE") for path in sources)
    lines = ["path\tsha256\trole"]
    for path, role in records:
        lines.append(f"{path.relative_to(ROOT)}\t{digest(path)}\t{role}")
    (HERE / "REVIEW_MANIFEST.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
