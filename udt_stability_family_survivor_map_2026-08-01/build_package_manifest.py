#!/usr/bin/env python3
"""Build deterministic survivor-map package manifest."""

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
OUT = PKG / "PACKAGE_MANIFEST.sha256"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = [f"{sha256(path)}  {path.name}" for path in sorted(PKG.iterdir()) if path.is_file() and path.name != OUT.name]
OUT.write_text("\n".join(records) + "\n", encoding="utf-8")
print(f"PASS package manifest: files={len(records)}")
