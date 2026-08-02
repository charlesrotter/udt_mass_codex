#!/usr/bin/env python3
"""Build the deterministic package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_MANIFEST_VERIFICATION.json"}


def main() -> int:
    paths = sorted(path for path in PKG.iterdir() if path.is_file() and path.name not in EXCLUDED)
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in paths]
    (PKG / "PACKAGE_MANIFEST.sha256").write_text("".join(lines), encoding="utf-8")
    print(f"manifested {len(paths)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
