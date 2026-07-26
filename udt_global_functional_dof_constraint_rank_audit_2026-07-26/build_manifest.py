#!/usr/bin/env python3
"""Build the package manifest, excluding self-referential gate outputs."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json", "REPOSITORY_GATES_STDOUT.txt"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    rendered = "".join(f"{digest(path)}  {path.name}\n" for path in paths)
    (HERE / "SHA256SUMS.txt").write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
