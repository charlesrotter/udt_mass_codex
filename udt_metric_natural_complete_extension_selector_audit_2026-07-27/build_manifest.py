#!/usr/bin/env python3
"""Write the final package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> int:
    rows = []
    for path in sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in EXCLUDE):
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (HERE / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"entries={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
