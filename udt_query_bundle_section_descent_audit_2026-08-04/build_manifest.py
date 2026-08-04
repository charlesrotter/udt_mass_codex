#!/usr/bin/env python3
"""Freeze all package members except the manifest and its verification record."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


members = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
lines = [f"{digest(path)}  {path.name}" for path in members]
(HERE / "PACKAGE_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"PASS package_members={len(members)} manifest_sha256={digest(HERE / 'PACKAGE_MANIFEST.sha256')}")
