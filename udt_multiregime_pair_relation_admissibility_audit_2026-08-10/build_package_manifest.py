#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for the G55 package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    entries = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path != OUTPUT:
            entries.append(f"{digest(path)}  {path.name}")
    OUTPUT.write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(f"PASS: wrote {len(entries)} package hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
