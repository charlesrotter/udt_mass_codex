#!/usr/bin/env python3
"""Write deterministic SHA-256 records for the completed P03 package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "SHA256SUMS.txt"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    excluded = {OUTPUT.name, "REPOSITORY_GATES.json"}
    files = sorted(
        path for path in HERE.iterdir()
        if path.is_file() and path.name not in excluded and not path.name.endswith(".pyc")
    )
    OUTPUT.write_text("".join(f"{digest(path)}  {path.name}\n" for path in files))


if __name__ == "__main__":
    main()
