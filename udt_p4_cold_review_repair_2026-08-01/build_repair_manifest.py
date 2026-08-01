#!/usr/bin/env python3
"""Write a deterministic primary-repair manifest, excluding itself and the target manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE / "REPAIR_MANIFEST.sha256"


def main() -> None:
    excluded = {TARGET.name, Path(__file__).name}
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name not in excluded:
            rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    TARGET.write_text("\n".join(rows) + "\n")
    print(f"PASS repair manifest: {len(rows)} files")


if __name__ == "__main__":
    main()
