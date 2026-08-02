#!/usr/bin/env python3
"""Replay deterministic ownership audit and capture raw output."""

from __future__ import annotations

import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMMANDS = (
    ("SOURCE_FREEZE", ["python3", str(HERE / "build_source_manifest.py")]),
    ("DERIVATION", ["python3", str(HERE / "derive_harmonic_ownership.py")]),
    ("INDEPENDENT", ["python3", str(HERE / "verify_harmonic_independent.py")]),
    ("VERIFICATION", ["python3", str(HERE / "verify_audit.py")]),
    ("REPOSITORY_GATES", ["python3", str(HERE / "verify_repository_gates.py")]),
)


def main() -> int:
    for label, command in COMMANDS:
        result = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, timeout=300, check=False
        )
        (HERE / f"{label}_STDOUT.txt").write_text(result.stdout, encoding="utf-8")
        (HERE / f"{label}_STDERR.txt").write_text(result.stderr, encoding="utf-8")
        if result.returncode:
            raise RuntimeError(f"{label} failed with {result.returncode}")
    print("PASS captured source, derivation, independent, semantic, and repository gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
