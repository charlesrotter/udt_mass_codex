#!/usr/bin/env python3
"""Build the deterministic final package manifest, excluding the manifest itself."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


paths = sorted(path for path in HERE.iterdir() if path.is_file() and path != MANIFEST)
MANIFEST.write_text("".join(f"{digest(path)}  {path.name}\n" for path in paths), encoding="utf-8")
print(f"PASS package manifest: {len(paths)} files")
