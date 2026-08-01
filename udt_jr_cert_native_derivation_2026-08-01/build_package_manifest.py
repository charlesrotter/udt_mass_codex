#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for the flat result package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


files = sorted(path for path in HERE.iterdir() if path.is_file() and path != OUTPUT)
OUTPUT.write_text("".join(f"{digest(path)}  {path.name}\n" for path in files), encoding="utf-8")
print(f"PASS package manifest: files={len(files)}")
