#!/usr/bin/env python3
"""Build the deterministic package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def main() -> int:
    paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE)
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in paths]
    (HERE / "PACKAGE_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS package_manifest {len(paths)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
