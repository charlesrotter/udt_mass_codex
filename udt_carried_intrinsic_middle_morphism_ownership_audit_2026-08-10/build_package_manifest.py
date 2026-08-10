#!/usr/bin/env python3
"""Build a non-self-referential SHA-256 manifest for this package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def main() -> None:
    rows = []
    for path in sorted(HERE.iterdir()):
        if not path.is_file() or path == OUTPUT:
            continue
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"PASS: {len(rows)} package files hashed")


if __name__ == "__main__":
    main()
