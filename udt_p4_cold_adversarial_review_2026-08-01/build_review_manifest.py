#!/usr/bin/env python3
"""Write a deterministic SHA-256 manifest for every review-package file except itself."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE / "REVIEW_MANIFEST.sha256"


def main() -> None:
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda p: p.name):
        if not path.is_file() or path == TARGET or path.name == "__pycache__":
            continue
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    TARGET.write_text("\n".join(rows) + "\n")
    print(f"PASS review manifest: {len(rows)} files")


if __name__ == "__main__":
    main()
