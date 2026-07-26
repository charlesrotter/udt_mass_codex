#!/usr/bin/env python3
"""Run and preserve both exact founded-pair implementations."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script: str, prefix: str) -> dict[str, object]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / f"{prefix}_STDOUT.txt").write_bytes(result.stdout)
    (HERE / f"{prefix}_STDERR.txt").write_bytes(result.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)
    parsed = json.loads(result.stdout)
    result_name = "DERIVATION_RESULT.json" if prefix == "DERIVATION" else "INDEPENDENT_RESULT.json"
    (HERE / result_name).write_text(json.dumps(parsed, indent=2, sort_keys=True) + "\n")
    return {
        "command": f"PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 {HERE.name}/{script}",
        "exit_code": result.returncode,
        "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
    }


def main() -> None:
    output = {
        "schema": "udt-founded-pair-global-alignment-run-environment-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "cpu_only": True,
        "runs": {
            "production": run("derive_founded_pair_alignment.py", "DERIVATION"),
            "independent": run("verify_alignment_independent.py", "INDEPENDENT"),
        },
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

