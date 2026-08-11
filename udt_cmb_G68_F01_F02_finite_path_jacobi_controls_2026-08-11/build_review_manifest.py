#!/usr/bin/env python3
"""Build the exact sealed-intake manifest for the G68 cold review."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXCLUDED = {
    "REVIEW_MANIFEST.tsv",
    "EXTERNAL_REVIEW_RAW.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "EXTERNAL_REVIEW_ADJUDICATION_PREREGISTRATION.md",
    "POSTREVIEW_MANIFEST.tsv",
    "POSTREVIEW_VERIFICATION_RESULT.json",
    "REPOSITORY_GATES.json",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    paths = [
        path for path in HERE.iterdir()
        if path.is_file() and path.name not in EXCLUDED
    ]
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            paths.append(ROOT / row["path"])
    unique = sorted({path.resolve() for path in paths})
    rows = []
    for path in unique:
        if not path.is_file():
            raise AssertionError(path)
        rows.append((path.relative_to(ROOT).as_posix(), digest(path)))
    output = "path\tsha256\n" + "".join(f"{path}\t{sha}\n" for path, sha in rows)
    (HERE / "REVIEW_MANIFEST.tsv").write_text(output, encoding="utf-8")
    print(f"review_files={len(rows)}")


if __name__ == "__main__":
    main()
