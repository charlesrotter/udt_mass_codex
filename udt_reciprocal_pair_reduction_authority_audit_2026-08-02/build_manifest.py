#!/usr/bin/env python3
"""Build deterministic source and package manifests."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


(HERE / "SOURCE_MANIFEST.sha256").write_text(
    f"{digest(HERE / 'SOURCE_MANIFEST.tsv')}  SOURCE_MANIFEST.tsv\n", encoding="utf-8"
)
paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE)
(HERE / "PACKAGE_MANIFEST.sha256").write_text(
    "\n".join(f"{digest(path)}  {path.name}" for path in paths) + "\n", encoding="utf-8"
)
print(f"PASS package manifest files={len(paths)}")
