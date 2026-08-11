#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for the local G69 package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.tsv"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    text = "path\tsha256\n" + "".join(f"{path.name}\t{digest(path)}\n" for path in files)
    (HERE / "PACKAGE_MANIFEST.tsv").write_text(text, encoding="utf-8")
    print(f"package_files={len(files)}")


if __name__ == "__main__":
    main()
