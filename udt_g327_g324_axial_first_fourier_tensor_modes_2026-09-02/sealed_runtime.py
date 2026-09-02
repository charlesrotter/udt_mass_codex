"""Activate the intake-local G327 symbolic runtime using only the standard library."""

from __future__ import annotations

import sys
from pathlib import Path


def activate_runtime() -> Path:
    archive = Path(__file__).resolve().with_name("VENDORED_SYMPY_RUNTIME.zip")
    if not archive.is_file():
        raise RuntimeError(f"sealed runtime missing: {archive}")
    if str(archive) not in sys.path:
        sys.path.insert(0, str(archive))
    return archive

