#!/usr/bin/env python3
"""Freeze every regular package file except the manifest itself."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
MANIFEST = PKG / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    paths = sorted(path for path in PKG.iterdir() if path.is_file() and path != MANIFEST)
    lines = [f"{digest(path)}  {path.name}" for path in paths]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS package files={len(paths)}")


if __name__ == "__main__":
    main()
