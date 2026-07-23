#!/usr/bin/env python3
"""Run and capture both deterministic coframe-Hopf audit routes."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run(script: str, prefix: str) -> dict[str, object]:
    command = [sys.executable, str(HERE / script)]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True)
    (HERE / f"{prefix}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{prefix}_STDERR.txt").write_bytes(completed.stderr)
    return {
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "stdout_sha256": digest(completed.stdout),
        "stderr_sha256": digest(completed.stderr),
        "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr),
    }


def main() -> None:
    production = run("derive_bridge.py", "DERIVATION")
    independent = run("verify_bridge_independent.py", "INDEPENDENT")
    if production["exit_code"] or independent["exit_code"]:
        raise SystemExit("coframe-Hopf replay failed")
    output = {
        "schema": "udt-coframe-hopf-bridge-replay-v1",
        "environment": {
            "python": platform.python_version(),
            "sympy": sympy.__version__,
            "cpu_only": True,
            "gpu_work_performed": False,
        },
        "production": production,
        "independent": independent,
        "all_exit_zero": True,
    }
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
