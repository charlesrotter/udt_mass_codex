#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for the audit package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def main() -> None:
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path == OUTPUT or path.name == "__pycache__":
            continue
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"PASS: wrote {len(rows)} package hashes")


if __name__ == "__main__":
    main()
