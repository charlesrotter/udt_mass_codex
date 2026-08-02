#!/usr/bin/env python3
"""Build the deterministic package manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = sorted(
    path for path in HERE.rglob("*")
    if path.is_file() and path.name not in EXCLUDE and "__pycache__" not in path.parts
)
(HERE / "PACKAGE_MANIFEST.sha256").write_text(
    "\n".join(f"{digest(path)}  {path.relative_to(HERE)}" for path in paths) + "\n",
    encoding="utf-8",
)
print(f"PASS package manifest files={len(paths)}")
