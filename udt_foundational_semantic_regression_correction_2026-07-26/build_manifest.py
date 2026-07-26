#!/usr/bin/env python3
"""Build package SHA-256 manifest excluding self-referential gate outputs."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json", "REPOSITORY_GATES_STDOUT.txt"}


def main() -> None:
    files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    text = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in files)
    (HERE / "SHA256SUMS.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
