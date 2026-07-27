#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> int:
    paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in paths]
    (HERE / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
    print(f"entries={len(paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
