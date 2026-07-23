#!/usr/bin/env python3
"""Run and capture the deterministic scientific and independent audit routes."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import numpy
import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run(script: str, prefix: str) -> dict[str, object]:
    command = [sys.executable, str(HERE / script)]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True)
    stdout_path = HERE / f"{prefix}_STDOUT.txt"
    stderr_path = HERE / f"{prefix}_STDERR.txt"
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    return {
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "stdout_sha256": digest_bytes(completed.stdout),
        "stderr_sha256": digest_bytes(completed.stderr),
        "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr),
    }


def main() -> None:
    derivation = run("derive_composition_audit.py", "DERIVATION")
    independent = run("verify_composition_independent.py", "INDEPENDENT")
    if derivation["exit_code"] or independent["exit_code"]:
        raise SystemExit("composition audit replay failed")
    result = {
        "schema": "udt-native-coframe-composition-replay-v1",
        "environment": {
            "python": platform.python_version(),
            "numpy": numpy.__version__,
            "sympy": sympy.__version__,
            "platform": platform.platform(),
            "cpu_only": True,
            "gpu_work_performed": False,
        },
        "derivation": derivation,
        "independent": independent,
        "all_exit_zero": True,
    }
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
