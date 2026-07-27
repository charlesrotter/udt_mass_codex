#!/usr/bin/env python3
"""Print package SHA-256 entries; manifest and repository-gate result exclude themselves."""

from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDE = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> int:
    for path in sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in EXCLUDE):
        print(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
