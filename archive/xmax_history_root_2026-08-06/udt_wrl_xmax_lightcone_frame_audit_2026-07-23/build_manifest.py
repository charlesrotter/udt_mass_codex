#!/usr/bin/env python3
"""Build the deterministic audit manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}


def main() -> None:
    files = sorted(
        path
        for path in HERE.iterdir()
        if path.is_file() and path.name not in EXCLUDED
    )
    text = "".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in files
    )
    (HERE / "MANIFEST.sha256").write_text(text, encoding="utf-8")
    print(f"wrote {len(files)} entries")


if __name__ == "__main__":
    main()
