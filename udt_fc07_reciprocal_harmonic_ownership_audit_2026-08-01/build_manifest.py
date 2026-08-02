#!/usr/bin/env python3
"""Build the deterministic package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def main() -> int:
    paths = sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in EXCLUDE)
    (HERE / "PACKAGE_MANIFEST.sha256").write_text(
        "\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}" for p in paths)
        + "\n",
        encoding="utf-8",
    )
    print(f"PASS package manifest files={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
