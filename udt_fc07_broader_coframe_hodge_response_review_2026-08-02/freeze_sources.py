#!/usr/bin/env python3
"""Freeze correction-layer source identities before implementation."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    with (PACKAGE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    output = []
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise SystemExit(f"missing source: {row['path']}")
        blob = subprocess.check_output(
            ["git", "hash-object", "--", row["path"]], cwd=ROOT, text=True
        ).strip()
        output.append(
            {
                **row,
                "git_blob": blob,
                "sha256": digest(path),
                "bytes": str(path.stat().st_size),
            }
        )
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "path", "role", "git_blob", "sha256", "bytes"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(output)
    print(f"SOURCES_FROZEN={len(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
