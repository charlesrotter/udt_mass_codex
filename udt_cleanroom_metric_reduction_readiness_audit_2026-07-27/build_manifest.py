#!/usr/bin/env python3
"""Build the deterministic package hash manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> None:
    paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    text = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in paths)
    (HERE / "SHA256SUMS.txt").write_text(text)
    print(f"PASS {len(paths)} entries")


if __name__ == "__main__":
    main()
