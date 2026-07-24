#!/usr/bin/env python3
"""Replay production and independent algebra and capture exact environment/output."""

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


def run(script: str, prefix: str) -> dict[str, object]:
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
    (HERE / f"{prefix}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{prefix}_STDERR.txt").write_bytes(completed.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    return {
        "command": f"CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 {sys.executable} {script}",
        "exit_code": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
    }


def main() -> None:
    production = run("derive_metric_native_separation.py", "PRODUCTION")
    independent = run("verify_metric_native_separation_independent.py", "INDEPENDENT")
    record = {
        "schema": "udt-metric-native-observer-separation-run-environment-1.0",
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "sympy": sympy.__version__,
        "compute": "CPU_ONLY",
        "cuda_visible_devices": "",
        "production": production,
        "independent": independent,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()
