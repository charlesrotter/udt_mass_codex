#!/usr/bin/env python3
"""Freeze exact P03 source identities without interpreting their contents."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    paths = [line.strip() for line in (HERE / "SOURCE_CANDIDATES.txt").read_text().splitlines() if line.strip()]
    if len(paths) != len(set(paths)):
        raise SystemExit("duplicate source candidate")
    rows = ["source_id\tpath\tsha256\tsize_bytes"]
    for index, relative in enumerate(paths, 1):
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        rows.append(f"S{index:03d}\t{relative}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\t{path.stat().st_size}")
    (HERE / "SOURCE_MANIFEST.tsv").write_text("\n".join(rows) + "\n")
    print(f"sources={len(paths)}")


if __name__ == "__main__":
    main()
