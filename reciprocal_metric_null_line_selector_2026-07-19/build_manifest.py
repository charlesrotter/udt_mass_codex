#!/usr/bin/env python3
"""Build the deterministic SHA-256 manifest for this audit package."""

from __future__ import annotations

import hashlib
import pathlib


def main() -> None:
    package = pathlib.Path(__file__).resolve().parent
    output = package / "SHA256SUMS.txt"
    paths = sorted(path for path in package.iterdir() if path.is_file() and path.name != output.name)
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in paths]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"MANIFEST BUILT entries={len(paths)}")


if __name__ == "__main__":
    main()
