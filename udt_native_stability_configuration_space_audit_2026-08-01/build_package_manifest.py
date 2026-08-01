#!/usr/bin/env python3
"""Freeze every package file except the manifest and its verification result."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION_RESULT.json"}


def main() -> None:
    paths = sorted(
        path for path in PKG.iterdir() if path.is_file() and path.name not in EXCLUDE
    )
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in paths]
    (PKG / "PACKAGE_MANIFEST.sha256").write_text("".join(lines), encoding="utf-8")
    print(f"manifested={len(paths)}")


if __name__ == "__main__":
    main()
