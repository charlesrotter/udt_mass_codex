#!/usr/bin/env python3
"""Write the package SHA-256 manifest, excluding the manifest itself."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "MANIFEST.sha256"
EXCLUDED = {OUT.name, "REPOSITORY_GATES.json", "REPOSITORY_GATES_TRANSCRIPT.txt"}
paths = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
OUT.write_text(
    "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in paths),
    encoding="utf-8",
)
