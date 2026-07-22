#!/usr/bin/env python3
"""Build the complete final package manifest, excluding self-referential gate outputs."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {
    "SHA256SUMS.txt",
    "FINAL_REPOSITORY_GATES.json",
    "FINAL_REPOSITORY_GATES_TRANSCRIPT.txt",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    (HERE / "SHA256SUMS.txt").write_text(
        "".join(f"{digest(path)}  {path.name}\n" for path in files), encoding="utf-8"
    )
    print(f"final_manifest_entries={len(files)}")
    print(f"final_manifest_sha256={digest(HERE / 'SHA256SUMS.txt')}")


if __name__ == "__main__":
    main()
