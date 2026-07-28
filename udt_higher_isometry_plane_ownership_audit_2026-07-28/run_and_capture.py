#!/usr/bin/env python3
"""Run the production and independent CPU calculations and capture raw streams."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, stdout_name: str, stderr_name: str) -> int:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    completed = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=HERE, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    (HERE / stdout_name).write_bytes(completed.stdout)
    (HERE / stderr_name).write_bytes(completed.stderr)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.returncode


def main() -> None:
    import sympy

    freeze = subprocess.run(
        [sys.executable, str(HERE / "freeze_sources.py")], cwd=HERE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    (HERE / "SOURCE_FREEZE_STDOUT.txt").write_bytes(freeze.stdout)
    (HERE / "SOURCE_FREEZE_STDERR.txt").write_bytes(freeze.stderr)
    if freeze.returncode != 0:
        raise SystemExit(freeze.returncode)
    run("derive_higher_isometry_plane_ownership.py", "DERIVATION_STDOUT.txt", "DERIVATION_STDERR.txt")
    run("verify_higher_isometry_plane_ownership_independent.py", "INDEPENDENT_STDOUT.txt", "INDEPENDENT_STDERR.txt")
    environment = {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "sympy": sympy.__version__,
        "cpu_only": True,
        "cuda_visible_devices": "",
        "production_stdout_sha256": hashlib.sha256((HERE / "DERIVATION_STDOUT.txt").read_bytes()).hexdigest(),
        "production_stderr_sha256": hashlib.sha256((HERE / "DERIVATION_STDERR.txt").read_bytes()).hexdigest(),
        "independent_stdout_sha256": hashlib.sha256((HERE / "INDEPENDENT_STDOUT.txt").read_bytes()).hexdigest(),
        "independent_stderr_sha256": hashlib.sha256((HERE / "INDEPENDENT_STDERR.txt").read_bytes()).hexdigest(),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("run_and_capture=PASS")
    print(f"production_stdout_sha256={environment['production_stdout_sha256']}")
    print(f"independent_stdout_sha256={environment['independent_stdout_sha256']}")


if __name__ == "__main__":
    main()

