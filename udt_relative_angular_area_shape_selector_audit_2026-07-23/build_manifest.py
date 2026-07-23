#!/usr/bin/env python3
"""Freeze every package file except manifest and repository-gate output."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    files = sorted(
        path
        for path in HERE.iterdir()
        if path.is_file() and path.name not in EXCLUDED
    )
    lines = [f"{digest(path)}  {path.name}" for path in files]
    (HERE / "MANIFEST.sha256").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(f"entries={len(files)}")


if __name__ == "__main__":
    main()
