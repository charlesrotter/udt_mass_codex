#!/usr/bin/env python3
"""Build the package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> None:
    lines = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name not in EXCLUDE:
            lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (HERE / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest_entries={len(lines)}")


if __name__ == "__main__":
    main()
