#!/usr/bin/env python3
import hashlib
from pathlib import Path

here = Path(__file__).resolve().parent
exclude = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

paths = sorted(
    path for path in here.rglob("*")
    if path.is_file() and path.name not in exclude and "__pycache__" not in path.parts
)
(here/"PACKAGE_MANIFEST.sha256").write_text(
    "\n".join(f"{digest(path)}  {path.relative_to(here)}" for path in paths)+"\n",
    encoding="utf-8",
)
print(f"PASS package_entries={len(paths)} manifest_sha256={digest(here/'PACKAGE_MANIFEST.sha256')}")
