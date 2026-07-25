#!/usr/bin/env python3
"""Build deterministic SHA-256 coverage for this audit package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt"}


def main() -> None:
    paths = sorted(
        path for path in HERE.iterdir()
        if path.is_file() and path.name not in EXCLUDED
    )
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
        for path in paths
    ]
    (HERE / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest_entries={len(paths)}")


if __name__ == "__main__":
    main()
