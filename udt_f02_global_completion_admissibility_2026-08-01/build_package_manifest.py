#!/usr/bin/env python3
"""Freeze every regular package file except the manifest itself."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
MANIFEST = PKG / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    paths = sorted(path for path in PKG.iterdir() if path.is_file() and path != MANIFEST)
    MANIFEST.write_text("\n".join(f"{digest(path)}  {path.name}" for path in paths) + "\n", encoding="utf-8")
    print(f"PASS package files={len(paths)}")


if __name__ == "__main__":
    main()
