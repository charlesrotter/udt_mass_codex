#!/usr/bin/env python3
"""Write deterministic SHA-256 rows for the banked pair-first package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "PACKAGE_MANIFEST.sha256"


def main() -> None:
    rows = []
    for path in sorted(HERE.iterdir()):
        if not path.is_file() or path == OUTPUT:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.name}")
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{len(rows)} files")


if __name__ == "__main__":
    main()
