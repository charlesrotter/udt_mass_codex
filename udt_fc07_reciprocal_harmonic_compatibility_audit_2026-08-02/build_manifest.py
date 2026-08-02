#!/usr/bin/env python3
"""Build the deterministic final package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def main() -> int:
    paths = sorted(path for path in PACKAGE.iterdir() if path.is_file() and path.name not in EXCLUDE)
    (PACKAGE / "PACKAGE_MANIFEST.sha256").write_text(
        "\n".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in paths)
        + "\n",
        encoding="utf-8",
    )
    print(f"PASS package manifest files={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
