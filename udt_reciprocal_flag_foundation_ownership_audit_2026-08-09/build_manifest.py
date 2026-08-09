#!/usr/bin/env python3
"""Build a non-self-referential SHA-256 manifest for this audit package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


members = sorted(
    path for path in HERE.iterdir()
    if path.is_file() and path.name not in {OUTPUT.name}
)
OUTPUT.write_text(
    "".join(f"{digest(path)}  {path.name}\n" for path in members),
    encoding="utf-8",
)
print(f"wrote {OUTPUT.name}: {len(members)} members")
