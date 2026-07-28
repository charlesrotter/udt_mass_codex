#!/usr/bin/env python3
"""Freeze the exact preregistered native global-definition source universe."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    paths = [line for line in (HERE / "SOURCE_CANDIDATES.txt").read_text().splitlines() if line]
    assert paths == list(dict.fromkeys(paths)), "duplicate source path"
    rows = ["source_id\tpath\tsha256\tsize_bytes\n"]
    for index, relative in enumerate(paths, start=1):
        path = ROOT / relative
        assert path.is_file(), relative
        rows.append(f"S{index:03d}\t{relative}\t{digest(path)}\t{path.stat().st_size}\n")
    (HERE / "SOURCE_MANIFEST.tsv").write_text("".join(rows))
    print(f"sources={len(paths)}")


if __name__ == "__main__":
    main()
