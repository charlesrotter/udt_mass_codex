#!/usr/bin/env python3
"""Build the deterministic package file manifest (excluding the manifest itself)."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_SHA256SUMS.tsv"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    files = sorted(
        path for path in HERE.iterdir()
        if path.is_file() and path.name != OUTPUT.name and not path.name.endswith(".pyc")
    )
    lines = ["path\tsha256\tsize"]
    lines.extend(f"{path.name}\t{digest(path)}\t{path.stat().st_size}" for path in files)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {len(files)} package files hashed")


if __name__ == "__main__":
    main()
