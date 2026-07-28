#!/usr/bin/env python3
"""Create the deterministic top-level package manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> None:
    files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in files]
    (HERE / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    digest = hashlib.sha256((HERE / "SHA256SUMS.txt").read_bytes()).hexdigest()
    print(f"entries={len(lines)}")
    print(f"manifest_sha256={digest}")


if __name__ == "__main__":
    main()
