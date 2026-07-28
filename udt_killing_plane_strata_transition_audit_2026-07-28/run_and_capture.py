#!/usr/bin/env python3
"""Run the exact CPU derivation and independent replay with raw-stream hashes."""

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


def run(script: str, stem: str) -> dict[str, object]:
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    process = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
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


def main() -> None:
    result = {
        "schema": "udt-killing-plane-strata-transition-run-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "device": "CPU_ONLY",
        "production": run("derive_killing_plane_transition.py", "DERIVATION"),
        "independent": run("verify_killing_plane_transition_independent.py", "INDEPENDENT"),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
