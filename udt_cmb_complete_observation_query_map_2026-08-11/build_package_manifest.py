#!/usr/bin/env python3
"""Build the current package manifest; preserve REVIEW_MANIFEST.tsv as review history."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    paths = sorted(
        (path for path in HERE.iterdir() if path.is_file() and path != OUT),
        key=lambda path: path.name,
    )
    OUT.write_text(
        "".join(f"{digest(path)}  {path.name}\n" for path in paths),
        encoding="utf-8",
    )
    print(f"package_manifest_rows={len(paths)}")


if __name__ == "__main__":
    main()
