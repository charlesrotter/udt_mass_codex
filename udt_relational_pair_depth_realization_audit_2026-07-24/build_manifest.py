#!/usr/bin/env python3
"""Build the complete package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> None:
    files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE)
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in files]
    output = "\n".join(lines) + "\n"
    (HERE / "SHA256SUMS.txt").write_text(output, encoding="utf-8")
    print(f"entries={len(files)}")
    print(f"manifest_sha256={hashlib.sha256(output.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
