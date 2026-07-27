#!/usr/bin/env python3
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDE = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE)
(HERE / "SHA256SUMS.txt").write_text("".join(f"{digest(path)}  {path.name}\n" for path in paths), encoding="utf-8")
print(f"PASS package_manifest entries={len(paths)}")
