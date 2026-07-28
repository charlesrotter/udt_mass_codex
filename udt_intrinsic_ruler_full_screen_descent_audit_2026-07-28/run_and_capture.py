#!/usr/bin/env python3
"""Run production and independent exact CPU replays and preserve raw streams."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import sympy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script: str, stem: str):
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    process = subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    (HERE / f"{stem}_STDOUT.txt").write_bytes(process.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(process.stderr)
    if process.returncode:
        raise SystemExit(process.returncode)
    return {
        "command": f"{sys.executable} {HERE.name}/{script}",
        "exit_code": process.returncode,
        "stdout_sha256": hashlib.sha256(process.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
    }


def main():
    result = {
        "schema": "udt-intrinsic-ruler-full-screen-descent-run-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "device": "CPU_ONLY",
        "production": run("derive_intrinsic_ruler_descent.py", "DERIVATION"),
        "independent": run("verify_intrinsic_ruler_descent_independent.py", "INDEPENDENT"),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
