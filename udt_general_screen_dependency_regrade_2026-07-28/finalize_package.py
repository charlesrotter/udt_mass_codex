#!/usr/bin/env python3
"""Write a deterministic non-self-referential package hash manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> None:
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path.name in EXCLUDED or path.suffix == ".pyc":
            continue
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (HERE / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"manifest_entries={len(rows)}")
    print(f"manifest_sha256={hashlib.sha256((HERE / 'SHA256SUMS.txt').read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
