#!/usr/bin/env python3
"""Build the non-self-referential SHA-256 manifest for this audit package."""

from __future__ import annotations

import hashlib
from pathlib import Path


OUT = Path(__file__).resolve().parent
MANIFEST = OUT / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


files = sorted(path for path in OUT.iterdir() if path.is_file() and path != MANIFEST)
MANIFEST.write_text("".join(f"{digest(path)}  {path.name}\n" for path in files), encoding="utf-8")
print(f"PASS package manifest: files={len(files)}")
