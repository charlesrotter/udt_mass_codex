#!/usr/bin/env python3
"""Build the deterministic package manifest, excluding self-referential outputs."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {
    "PACKAGE_MANIFEST.sha256",
    "PACKAGE_VERIFICATION.json",
    "MANIFEST_STDOUT.txt",
    "MANIFEST_STDERR.txt",
    "PACKAGE_VERIFIER_STDOUT.txt",
    "PACKAGE_VERIFIER_STDERR.txt",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = sorted(
    path for path in HERE.rglob("*")
    if path.is_file() and path.name not in EXCLUDE and "__pycache__" not in path.parts
)
lines = [f"{digest(path)}  {path.relative_to(HERE)}" for path in paths]
(HERE / "PACKAGE_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"PASS package_entries={len(paths)} manifest_sha256={digest(HERE / 'PACKAGE_MANIFEST.sha256')}")
