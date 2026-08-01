#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for the completed audit package."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
OUT = PKG / "PACKAGE_MANIFEST.sha256"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


rows = []
for path in sorted(p for p in PKG.iterdir() if p.is_file() and p.name != OUT.name):
    rows.append(f"{sha256(path)}  {path.name}")
OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"PASS package manifest: files={len(rows)}")

