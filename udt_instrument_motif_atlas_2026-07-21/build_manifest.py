#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
paths = sorted(
    path for path in HERE.rglob("*")
    if path.is_file()
    and path.relative_to(HERE).as_posix() not in EXCLUDED
    and "__pycache__" not in path.parts
    and path.suffix != ".pyc"
)
(HERE / "SHA256SUMS.txt").write_text(
    "\n".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(HERE).as_posix()}"
        for path in paths
    ) + "\n",
    encoding="utf-8",
)
print(f"PASS entries={len(paths)}")
