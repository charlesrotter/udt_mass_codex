#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for this package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def main() -> int:
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path == OUTPUT:
            continue
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} rows to {OUTPUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
