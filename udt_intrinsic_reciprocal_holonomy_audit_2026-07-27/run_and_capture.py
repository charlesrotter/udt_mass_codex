#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import numpy
import scipy
import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def execute(script: str):
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    completed = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    return completed.stdout, completed.stderr, json.loads(completed.stdout)


def main() -> int:
    stdout, stderr, production = execute("compute_holonomy_atlas.py")
    (HERE / "DERIVATION_STDOUT.txt").write_text(stdout, encoding="utf-8")
    (HERE / "DERIVATION_STDERR.txt").write_text(stderr, encoding="utf-8")
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(production, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    stdout, stderr, independent = execute("verify_holonomy_independent.py")
    (HERE / "INDEPENDENT_STDOUT.txt").write_text(stdout, encoding="utf-8")
    (HERE / "INDEPENDENT_STDERR.txt").write_text(stderr, encoding="utf-8")
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(independent, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    assert production["status"] == "COMPUTED" and independent["status"] == "PASS"
    environment = {
        "python": platform.python_version(), "platform": platform.platform(),
        "numpy": numpy.__version__, "scipy": scipy.__version__, "torch": torch.__version__,
        "dtype": "float64", "cpu_only": True, "CUDA_VISIBLE_DEVICES": "",
        "production_command": "PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 "
                              + str(HERE.relative_to(ROOT) / "compute_holonomy_atlas.py"),
        "independent_command": "PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 "
                               + str(HERE.relative_to(ROOT) / "verify_holonomy_independent.py"),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS production and independent captures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
