#!/usr/bin/env python3
"""Build the F01 package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION_RESULT.json"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    value.update(path.read_bytes())
    return value.hexdigest()


def main() -> None:
    paths = sorted(path for path in PKG.iterdir() if path.is_file() and path.name not in EXCLUDED)
    lines = [f"{digest(path)}  {path.name}" for path in paths]
    (PKG / "PACKAGE_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifested {len(paths)} files")


if __name__ == "__main__":
    main()
