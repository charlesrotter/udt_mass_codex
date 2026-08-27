#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SCOPE = PACKAGE / "SOURCE_SCOPE.tsv"
OUTPUT = PACKAGE / "SOURCE_MANIFEST.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with SCOPE.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert rows, "empty source scope"
    assert len({row["path"] for row in rows}) == len(rows), "duplicate source path"

    frozen = []
    for row in rows:
        source = ROOT / row["path"]
        assert source.is_file(), f"missing source: {row['path']}"
        frozen.append(
            {
                "sha256": sha256(source),
                "bytes": source.stat().st_size,
                "path": row["path"],
                "role": row["role"],
            }
        )

    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sha256", "bytes", "path", "role"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(frozen)
    print(f"PASS: froze {len(frozen)} load-bearing sources")


if __name__ == "__main__":
    main()
