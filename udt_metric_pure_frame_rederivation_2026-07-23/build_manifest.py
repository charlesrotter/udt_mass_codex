#!/usr/bin/env python3
"""Build this package's SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    rows = []
    for path in sorted(item for item in here.iterdir() if item.is_file()):
        if path.name in excluded:
            continue
        rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    here.joinpath("MANIFEST.sha256").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"entries {len(rows)}")


if __name__ == "__main__":
    main()
