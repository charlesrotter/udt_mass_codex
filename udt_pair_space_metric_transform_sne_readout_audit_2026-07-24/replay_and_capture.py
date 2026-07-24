#!/usr/bin/env python3
"""Replay all scientific calculations and capture exact commands and streams."""

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


def run(label: str, script: str) -> dict[str, object]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        ["/usr/bin/python3", script],
        cwd=HERE,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / f"{label}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{label}_STDERR.txt").write_bytes(completed.stderr)
    return {
        "command": (
            "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 "
            f"/usr/bin/python3 {script}"
        ),
        "exit_code": completed.returncode,
        "stdout_sha256": digest(completed.stdout),
        "stderr_sha256": digest(completed.stderr),
    }


def main() -> None:
    production = run("PRODUCTION", "derive_pair_space_metrics.py")
    sne = run("SNE", "replay_sne_readouts.py")
    independent = run("INDEPENDENT", "verify_independent.py")
    if any(item["exit_code"] for item in (production, sne, independent)):
        raise SystemExit("scientific replay failed")
    import numpy
    import scipy
    import sympy

    result = {
        "schema": "udt-pair-space-sne-run-environment-1.0",
        "compute": "CPU_ONLY",
        "gpu_work_performed": False,
        "cuda_visible_devices": "",
        "python": sys.version.split()[0],
        "python_executable": "/usr/bin/python3",
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "production": production,
        "SNe": sne,
        "independent": independent,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
