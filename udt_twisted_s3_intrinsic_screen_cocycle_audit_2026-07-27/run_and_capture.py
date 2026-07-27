#!/usr/bin/env python3
"""Run the two preregistered implementations and preserve exact streams/results."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PINNED = Path("/tmp/udt_screen_cocycle_sympy_114_pkgs")


def run(command: list[str], environment: dict[str, str]) -> tuple[str, str]:
    completed = subprocess.run(command, cwd=ROOT, env=environment, text=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    return completed.stdout, completed.stderr


def main() -> int:
    production_environment = dict(os.environ)
    production_environment.update({
        "PYTHONPATH": str(PINNED), "PYTHONDONTWRITEBYTECODE": "1", "CUDA_VISIBLE_DEVICES": "",
    })
    independent_environment = dict(os.environ)
    independent_environment.update({"PYTHONDONTWRITEBYTECODE": "1", "CUDA_VISIBLE_DEVICES": ""})

    production_command = [sys.executable, "-S", str(HERE / "derive_intrinsic_screen_cocycle.py")]
    independent_command = [sys.executable, "-S", str(HERE / "verify_screen_cocycle_independent.py")]
    production_stdout, production_stderr = run(production_command, production_environment)
    independent_stdout, independent_stderr = run(independent_command, independent_environment)
    production = json.loads(production_stdout)
    independent = json.loads(independent_stdout)
    assert production["status"] == independent["status"] == "PASS"
    assert production["sympy_version"] == "1.14.0"
    assert independent["production_module_imported"] is False

    (HERE / "DERIVATION_STDOUT.txt").write_text(production_stdout, encoding="utf-8")
    (HERE / "DERIVATION_STDERR.txt").write_text(production_stderr, encoding="utf-8")
    (HERE / "INDEPENDENT_STDOUT.txt").write_text(independent_stdout, encoding="utf-8")
    (HERE / "INDEPENDENT_STDERR.txt").write_text(independent_stderr, encoding="utf-8")
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(production, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(independent, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = {
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "platform": platform.platform(), "sympy": production["sympy_version"],
        "sympy_dependency_path": str(PINNED), "cpu_only": True,
        "production_command": "PYTHONPATH=/tmp/udt_screen_cocycle_sympy_114_pkgs PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -S "
                              + str(HERE.relative_to(ROOT) / "derive_intrinsic_screen_cocycle.py"),
        "independent_command": "PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 -S "
                               + str(HERE.relative_to(ROOT) / "verify_screen_cocycle_independent.py"),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS production and independent captures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
