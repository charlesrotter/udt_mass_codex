#!/usr/bin/env python3
"""Write the frozen package SHA-256 manifest, excluding the manifest itself and caches."""

from __future__ import annotations

import hashlib
import pathlib


def main() -> None:
    package = pathlib.Path(__file__).resolve().parent
    manifest = package / "SHA256SUMS.txt"
    rows = []
    for path in sorted(package.iterdir(), key=lambda item: item.name):
        if path.name == manifest.name or path.name == "__pycache__":
            continue
        if not path.is_file():
            raise RuntimeError(f"unexpected non-file package entry: {path.name}")
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  ./{path.name}")
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"MANIFEST entries={len(rows)}")


if __name__ == "__main__":
    main()
