#!/usr/bin/env python3
"""Build the preregistered source manifest without changing source files."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    rows = []
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            if not path.is_file():
                raise SystemExit(f"missing source: {row['path']}")
            rows.append(
                {
                    **row,
                    "size_bytes": str(path.stat().st_size),
                    "sha256": sha256(path),
                }
            )

    out = HERE / "SOURCE_MANIFEST.tsv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source_id", "path", "role", "size_bytes", "sha256"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
