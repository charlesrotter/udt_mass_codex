#!/usr/bin/env python3
"""Build package manifest excluding self-referential gate files."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}


def main() -> None:
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name not in EXCLUDED:
            rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    HERE.joinpath("MANIFEST.sha256").write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
