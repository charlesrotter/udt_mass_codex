#!/usr/bin/env python3
"""Build the exact G69 sealed-review manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXCLUDED = {
    "PACKAGE_MANIFEST.tsv",
    "REVIEW_MANIFEST.tsv",
    "EXTERNAL_REVIEW_RAW.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package_paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    records = [(str(path.relative_to(ROOT)), digest(path), "G69_PACKAGE") for path in package_paths]
    records.extend((row["path"], row["sha256"], "CITED_SOURCE") for row in source_rows)
    assert len(records) == len({path for path, _, _ in records})
    text = "path\tsha256\trole\n" + "".join(f"{path}\t{sha}\t{role}\n" for path, sha, role in records)
    (HERE / "REVIEW_MANIFEST.tsv").write_text(text, encoding="utf-8")
    print(f"review_rows={len(records)} sealed_files={len(records) + 1}")


if __name__ == "__main__":
    main()
