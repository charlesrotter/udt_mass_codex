#!/usr/bin/env python3
"""Replay the audit under pinned SymPy with site packages disabled."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PINNED_TARGET = Path("/tmp/udt_metric_selector_sympy_114")
PYTHON = Path("/usr/bin/python3")


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    env = dict(os.environ)
    env.update({
        "CUDA_VISIBLE_DEVICES": "",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(PINNED_TARGET),
    })
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def save(prefix: str, result: subprocess.CompletedProcess[bytes]) -> dict[str, object]:
    stdout_path = HERE / f"{prefix}_STDOUT.txt"
    stderr_path = HERE / f"{prefix}_STDERR.txt"
    stdout_path.write_bytes(result.stdout)
    stderr_path.write_bytes(result.stderr)
    return {
        "command": result.args,
        "exit_code": result.returncode,
        "stdout_bytes": len(result.stdout),
        "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
        "stderr_bytes": len(result.stderr),
        "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
    }


def main() -> int:
    assert PINNED_TARGET.is_dir(), f"missing pinned target: {PINNED_TARGET}"
    version = run([
        str(PYTHON), "-S", "-c",
        "import platform,sys,sympy; print(platform.python_version()); print(sympy.__version__); print(sympy.__file__)",
    ])
    assert version.returncode == 0, version.stderr.decode(errors="replace")
    lines = version.stdout.decode("utf-8").splitlines()
    assert lines[0] == "3.10.12"
    assert lines[1] == "1.14.0"
    assert Path(lines[2]).resolve().is_relative_to(PINNED_TARGET.resolve())

    commands = {
        "DERIVATION": [str(PYTHON), "-S", str(HERE / "derive_metric_natural_selector.py")],
        "INDEPENDENT": [str(PYTHON), "-S", str(HERE / "verify_metric_natural_selector_independent.py")],
        "VERIFICATION": [str(PYTHON), "-S", str(HERE / "verify_audit.py")],
    }
    executions = {}
    for prefix, command in commands.items():
        result = run(command)
        executions[prefix.lower()] = save(prefix, result)
        assert result.returncode == 0, result.stderr.decode(errors="replace")

    exact_sha256 = hashlib.sha256((HERE / "EXACT_ALGEBRA.json").read_bytes()).hexdigest()
    assert exact_sha256 == "720e24dad2d613f0c2ddf18c4651e752c87b79a1eb41f07b5300d9e12e632d39"
    environment = {
        "schema": "udt-metric-natural-selector-clean-environment-1.0",
        "compute": "CPU_ONLY",
        "cuda_visible_devices": "",
        "executable": str(PYTHON),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "python": lines[0],
        "sympy": lines[1],
        "sympy_path": lines[2],
        "site_packages": "DISABLED_WITH_-S",
        "pinned_target": str(PINNED_TARGET),
        "dependency_specification": "requirements.txt: sympy==1.14.0",
        "installation_command": "python3 -m pip install --target /tmp/udt_metric_selector_sympy_114 sympy==1.14.0",
        "preregistration_commit": "d2c1efbb1870b0d8da7bbe5b713603c0e3ebf622",
        "exact_algebra_sha256": exact_sha256,
        "executions": executions,
        "external_review_sessions": [
            "019fa59c-947a-7290-8a9f-0c7bcf05da27",
            "019fa5aa-8dcb-72d3-b48a-56870842a3bf",
            "019fa5b7-cdbc-7271-b312-c5edceffb96a",
            "019fa5c3-00e1-79f3-95b0-9ec5ee31d49b",
        ],
        "result": "PASS",
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(environment, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
