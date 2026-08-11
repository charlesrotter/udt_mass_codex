#!/usr/bin/env python3
"""Build the deterministic external-review file/hash manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT = HERE / "REVIEW_MANIFEST.tsv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    package_files = sorted(
        p for p in HERE.iterdir()
        if p.is_file() and p.name not in {"REVIEW_MANIFEST.tsv", "EXTERNAL_REVIEW_RAW.md"}
    )
    source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    paths = {p.relative_to(REPO) for p in package_files}
    paths.update(Path(row["path"]) for row in source_rows)
    rows = []
    for relative in sorted(paths, key=str):
        path = REPO / relative
        if not path.is_file():
            raise RuntimeError(f"missing review source {relative}")
        rows.append((str(relative), sha256(path)))
    with OUT.open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256"))
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
