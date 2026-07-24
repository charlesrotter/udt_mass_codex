#!/usr/bin/env python3
"""Run production and independent calculations and capture raw streams."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent


def run(script: str, stdout_name: str, stderr_name: str) -> None:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, script],
        cwd=HERE,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / stdout_name).write_bytes(completed.stdout)
    (HERE / stderr_name).write_bytes(completed.stderr)
    if completed.returncode:
        sys.stdout.buffer.write(completed.stdout)
        sys.stderr.buffer.write(completed.stderr)
        raise SystemExit(completed.returncode)


def main() -> None:
    environment = {
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "compute": "CPU_ONLY",
        "cuda_visible_devices": "",
        "production_command": f"{sys.executable} derive_observer_cocycle.py",
        "independent_command": (
            f"{sys.executable} verify_observer_cocycle_independent.py"
        ),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    run(
        "derive_observer_cocycle.py",
        "PRODUCTION_STDOUT.txt",
        "PRODUCTION_STDERR.txt",
    )
    run(
        "verify_observer_cocycle_independent.py",
        "INDEPENDENT_STDOUT.txt",
        "INDEPENDENT_STDERR.txt",
    )
    print("production=PASS")
    print("independent=PASS")


if __name__ == "__main__":
    main()
