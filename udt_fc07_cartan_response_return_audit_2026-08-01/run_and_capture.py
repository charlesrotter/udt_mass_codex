#!/usr/bin/env python3
"""Replay deterministic derivation and capture raw output."""

from __future__ import annotations

import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMMANDS = (
    ("SOURCE_FREEZE", ["python3", str(HERE / "build_source_manifest.py")]),
    ("DERIVATION", ["python3", str(HERE / "derive_cartan_response.py")]),
    ("INDEPENDENT", ["python3", str(HERE / "verify_cartan_independent.py")]),
    ("VERIFICATION", ["python3", str(HERE / "verify_audit.py")]),
)


def main() -> int:
    for label, command in COMMANDS:
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180, check=False)
        (HERE / f"{label}_STDOUT.txt").write_text(result.stdout, encoding="utf-8")
        (HERE / f"{label}_STDERR.txt").write_text(result.stderr, encoding="utf-8")
        if result.returncode:
            raise RuntimeError(f"{label} failed with {result.returncode}")
    print("PASS captured source freeze, derivation, independent replay, and semantic verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
