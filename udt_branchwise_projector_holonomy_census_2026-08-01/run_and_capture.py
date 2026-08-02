#!/usr/bin/env python3
"""Replay deterministic package commands and preserve raw stdout/stderr."""

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
    ("DISCOVERY", [sys.executable, str(HERE / "discover_candidates.py")]),
    ("REPORT_EXTRACT", [sys.executable, str(HERE / "extract_report_evidence.py")]),
    ("CENSUS_LEDGER", [sys.executable, str(HERE / "build_census_ledgers.py")]),
    ("DERIVATION", [sys.executable, str(HERE / "derive_branchwise_projector_gates.py")]),
    ("INDEPENDENT", [sys.executable, str(HERE / "verify_branchwise_projector_gates_independent.py")]),
    ("VERIFICATION", [sys.executable, str(HERE / "verify_census.py")]),
]


def main() -> int:
    records = []
    for label, command in COMMANDS:
        result = subprocess.run(command, cwd=ROOT, text=False, capture_output=True, timeout=120, check=False)
        (HERE / f"{label}_STDOUT.txt").write_bytes(result.stdout)
        (HERE / f"{label}_STDERR.txt").write_bytes(result.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"{label} failed: {result.returncode}")
        records.append({
            "label": label, "command": command, "exit_code": result.returncode,
            "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
        })
    try:
        import sympy
        sympy_version = sympy.__version__
    except ImportError:
        sympy_version = "UNAVAILABLE"
    environment = {
        "schema": "udt.branchwise_projector_holonomy_census.environment.v1",
        "platform": platform.platform(), "python": platform.python_version(),
        "python_executable": sys.executable, "sympy": sympy_version,
        "compute": "CPU_ONLY", "commands": records,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(environment, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
