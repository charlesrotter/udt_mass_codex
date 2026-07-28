#!/usr/bin/env python3
"""Build the recursive P02 SHA-256 manifest without self-reference or caches."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    paths = [
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != "SHA256SUMS.txt"
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    ]
    lines = []
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative}")
    (ROOT / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
    print(f"entries={len(lines)}")


if __name__ == "__main__":
    main()
