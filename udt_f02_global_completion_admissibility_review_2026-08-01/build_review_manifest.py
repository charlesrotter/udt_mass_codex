#!/usr/bin/env python3
"""Build the review-layer SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "REVIEW_LAYER_MANIFEST.sha256"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


paths = sorted(path for path in HERE.iterdir() if path.is_file() and path != MANIFEST)
MANIFEST.write_text(
    "".join(f"{sha256(path)}  {path.name}\n" for path in paths), encoding="utf-8"
)
print(f"WROTE {MANIFEST.name} {len(paths)} files")
