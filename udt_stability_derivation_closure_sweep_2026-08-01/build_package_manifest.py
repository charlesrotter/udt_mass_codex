#!/usr/bin/env python3
"""Build the sweep package manifest, excluding the manifest itself."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
OUT = PKG / "PACKAGE_MANIFEST.sha256"


def main() -> None:
    rows = []
    for path in sorted(PKG.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path == OUT:
            continue
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    OUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"PASS package manifest: files={len(rows)}")


if __name__ == "__main__":
    main()
