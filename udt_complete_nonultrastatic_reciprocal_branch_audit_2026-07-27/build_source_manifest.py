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
    assert len(rows) == 19
    assert len({row["path"] for row in rows}) == 19
    for row in rows:
        assert digest(ROOT / row["path"]) == row["sha256"], row["path"]
    print("PASS source_manifest 19/19")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
