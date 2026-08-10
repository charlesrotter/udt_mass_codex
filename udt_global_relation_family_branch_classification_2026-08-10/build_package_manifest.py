#!/usr/bin/env python3
"""Build the package hash manifest, excluding the self-referential manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def main() -> None:
    lines = []
    for path in sorted(HERE.iterdir()):
        if not path.is_file() or path == OUTPUT or path.name == "__pycache__":
            continue
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {len(lines)} package files hashed")


if __name__ == "__main__":
    main()
