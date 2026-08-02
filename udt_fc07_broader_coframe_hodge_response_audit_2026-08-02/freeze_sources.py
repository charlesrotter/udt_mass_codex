#!/usr/bin/env python3
"""Freeze the preregistered source scope before derivation."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SCOPE = PACKAGE / "SOURCE_SCOPE.tsv"
MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with SCOPE.open(newline="", encoding="utf-8") as handle:
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
                "sha256": sha256(path),
                "bytes": str(path.stat().st_size),
            }
        )
    with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["id", "path", "role", "git_blob", "sha256", "bytes"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(output)
    print(f"SOURCES_FROZEN={len(output)}")


if __name__ == "__main__":
    main()
