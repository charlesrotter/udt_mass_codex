#!/usr/bin/env python3
"""Build the preregistered source manifest without modifying source evidence."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    out = []
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise SystemExit(f"missing source: {row['path']}")
        out.append(
            {
                "source_id": row["source_id"],
                "path": row["path"],
                "bytes": str(path.stat().st_size),
                "sha256": sha256(path),
            }
        )
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=["source_id", "path", "bytes", "sha256"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(out)


if __name__ == "__main__":
    main()
