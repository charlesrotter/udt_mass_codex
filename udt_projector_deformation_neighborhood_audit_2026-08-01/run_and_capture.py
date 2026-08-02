#!/usr/bin/env python3
"""Replay deterministic package commands and preserve raw streams."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMMANDS = [
    ("SOURCE_FREEZE", [sys.executable, str(HERE / "build_source_manifest.py")]),
    ("DERIVATION", [sys.executable, str(HERE / "derive_deformation_neighborhood.py")]),
    ("INDEPENDENT", [sys.executable, str(HERE / "verify_deformation_neighborhood_independent.py")]),
    ("VERIFICATION", [sys.executable, str(HERE / "verify_audit.py")]),
]


def main() -> int:
    records = []
    for label, command in COMMANDS:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, timeout=120, check=False
        )
        (HERE / f"{label}_STDOUT.txt").write_bytes(result.stdout)
        (HERE / f"{label}_STDERR.txt").write_bytes(result.stderr)
        if result.returncode:
            raise RuntimeError(f"{label} failed with {result.returncode}")
        records.append(
            {
                "label": label,
                "command": command,
                "exit_code": result.returncode,
                "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
                "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
            }
        )
    import sympy

    environment = {
        "schema": "udt.projector_deformation_neighborhood.environment.v1",
        "platform": platform.platform(),
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "sympy": sympy.__version__,
        "compute": "CPU_ONLY",
        "commands": records,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(environment, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

