#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 17
    assert len({row["path"] for row in rows}) == 17
    for row in rows:
        path = ROOT / row["path"]
        assert digest(path) == row["sha256"], row["path"]
    print("PASS source_manifest 17/17")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
