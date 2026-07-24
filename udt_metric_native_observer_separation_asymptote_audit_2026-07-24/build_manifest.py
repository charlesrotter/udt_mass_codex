#!/usr/bin/env python3
"""Build the package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> None:
    entries = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path.name in EXCLUDE:
            continue
        entries.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (HERE / "SHA256SUMS.txt").write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(f"entries={len(entries)}")
    print(
        "manifest_sha256="
        + hashlib.sha256((HERE / "SHA256SUMS.txt").read_bytes()).hexdigest()
    )


if __name__ == "__main__":
    main()
