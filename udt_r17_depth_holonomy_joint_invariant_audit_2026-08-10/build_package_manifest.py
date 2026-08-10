#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for this audit package."""

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
    files = sorted(path for path in HERE.iterdir() if path.is_file() and path != OUTPUT)
    lines = [f"{digest(path)}  {path.name}" for path in files]
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {len(files)} package files hashed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
