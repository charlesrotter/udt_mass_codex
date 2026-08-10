#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for the G56 package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    entries = [
        f"{digest(path)}  {path.name}"
        for path in sorted(HERE.iterdir(), key=lambda item: item.name)
        if path.is_file() and path != OUTPUT
    ]
    OUTPUT.write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(f"PASS: wrote {len(entries)} package hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
