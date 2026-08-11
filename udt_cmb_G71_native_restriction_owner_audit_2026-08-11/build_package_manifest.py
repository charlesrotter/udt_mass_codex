#!/usr/bin/env python3
"""Build the non-self-referential local G71 package manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.tsv", "REVIEW_MANIFEST.tsv"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE)
    lines = ["path\tsha256"]
    lines.extend(f"{path.name}\t{digest(path)}" for path in paths)
    (HERE / "PACKAGE_MANIFEST.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
