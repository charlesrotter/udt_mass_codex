#!/usr/bin/env python3
"""Replay the production and independent depth-angle audits."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(script: str) -> dict[str, object]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = ["/usr/bin/python3", script]
    completed = subprocess.run(
        command,
        cwd=HERE,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    stem = "PRODUCTION" if script.startswith("derive_") else "INDEPENDENT"
    (HERE / f"{stem}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(completed.stderr)
    return {
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 " + script,
        "exit_code": completed.returncode,
        "stdout_sha256": digest(completed.stdout),
        "stderr_sha256": digest(completed.stderr),
    }


def main() -> None:
    production = run("derive_observer_depth_angle_transition.py")
    independent = run("verify_observer_depth_angle_transition_independent.py")
    if production["exit_code"] or independent["exit_code"]:
        raise SystemExit("depth-angle replay failed")
    import sympy

    environment = {
        "schema": "udt-observer-depth-angle-transition-run-environment-1.0",
        "compute": "CPU_ONLY",
        "cuda_visible_devices": "",
        "python": sys.version.split()[0],
        "python_executable": "/usr/bin/python3",
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "production": production,
        "independent": independent,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(environment, sort_keys=True))


if __name__ == "__main__":
    main()
