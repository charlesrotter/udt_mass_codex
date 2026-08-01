#!/usr/bin/env python3
"""Build the immutable-content manifest for the inverse-surface package."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION_RESULT.json"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    paths = sorted(path for path in PKG.iterdir() if path.is_file() and path.name not in EXCLUDED)
    (PKG / "PACKAGE_MANIFEST.sha256").write_text(
        "".join(f"{digest(path)}  {path.name}\n" for path in paths), encoding="utf-8"
    )
    print(f"manifested_files={len(paths)}")


if __name__ == "__main__":
    main()
