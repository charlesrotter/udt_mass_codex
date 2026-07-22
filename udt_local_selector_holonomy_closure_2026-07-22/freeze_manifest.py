#!/usr/bin/env python3
"""Freeze all package files except mutable gate outputs and the manifest itself."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"MANIFEST.sha256", "REPOSITORY_GATES.json", "REPOSITORY_GATES_TRANSCRIPT.txt"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    payload = "".join(f"{digest(path)}  {path.name}\n" for path in paths)
    (HERE / "MANIFEST.sha256").write_text(payload, encoding="utf-8")
    print(f"entries={len(paths)}")


if __name__ == "__main__":
    main()

