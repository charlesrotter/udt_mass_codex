#!/usr/bin/env python3
"""Build the deterministic package manifest."""

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
(HERE / "MANIFEST.sha256").write_text(
    "".join(f"{digest(path)}  {path.name}\n" for path in files), encoding="utf-8"
)
print(f"entries={len(files)}")
