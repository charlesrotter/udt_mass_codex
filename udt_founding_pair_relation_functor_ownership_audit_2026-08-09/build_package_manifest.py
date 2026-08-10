#!/usr/bin/env python3
"""Build the deterministic SHA-256 manifest for this evidence package."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "PACKAGE_MANIFEST.sha256"
EXCLUDED = {OUTPUT.name}


def main() -> None:
    rows: list[str] = []
    for path in sorted(ROOT.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path.name in EXCLUDED:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.name}")
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"PASS: wrote {len(rows)} package hashes to {OUTPUT.name}")


if __name__ == "__main__":
    main()
