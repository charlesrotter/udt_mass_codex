#!/usr/bin/env python3
"""Build a deterministic manifest for the completed audit package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
lines = [f"{digest(path)}  {path.stat().st_size}  {path.name}" for path in paths]
(HERE / "PACKAGE_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"PASS package_members={len(paths)} manifest_sha256={digest(HERE / 'PACKAGE_MANIFEST.sha256')}")
