#!/usr/bin/env python3
"""Build deterministic N02 SHA-256 manifest after review repairs."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def main() -> None:
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path != OUTPUT:
            rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"PASS: wrote {len(rows)} package hashes")


if __name__ == "__main__":
    main()
