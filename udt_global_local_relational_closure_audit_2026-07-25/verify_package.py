#!/usr/bin/env python3
"""Fail-closed replay and package-verification harness."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TRACKED_OUTPUTS = ("RESULT.json", "INDEPENDENT.json", "ADVERSARIAL.json")


def run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=HERE,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    target = os.environ.get("UDT_SYMPY_TARGET", "/tmp/udt_bootstrap_closure_sympy_114")
    env = dict(os.environ)
    env.update(
        {
            "CUDA_VISIBLE_DEVICES": "",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": target,
            "UDT_REPO": str(ROOT),
        }
    )
    before = {name: (HERE / name).read_bytes() for name in TRACKED_OUTPUTS}
    commands = [
        [sys.executable, "audit_closure.py"],
        [sys.executable, "verify_independent.py"],
        [sys.executable, "verify_adversarial.py"],
    ]
    for command in commands:
        completed = run(command, env)
        if completed.returncode:
            raise AssertionError(
                f"{command}: stdout={completed.stdout}\nstderr={completed.stderr}"
            )
    if any((HERE / name).read_bytes() != before[name] for name in TRACKED_OUTPUTS):
        raise AssertionError("replay changed a tracked result")
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT.json").read_text(encoding="utf-8"))
    adversarial = json.loads((HERE / "ADVERSARIAL.json").read_text(encoding="utf-8"))
    if (
        result["result"] != "PASS"
        or result["check_count"] != 43
        or independent["result"] != "PASS"
        or independent["check_count"] != 18
        or adversarial["result"] != "PASS"
        or adversarial["catch_count"] != 7
    ):
        raise AssertionError("recorded result state")
    print(
        json.dumps(
            {
                "result": "PASS",
                "production_checks": 43,
                "independent_checks": 18,
                "adversarial_catches": 7,
                "result_sha256": digest(HERE / "RESULT.json"),
                "independent_sha256": digest(HERE / "INDEPENDENT.json"),
                "adversarial_sha256": digest(HERE / "ADVERSARIAL.json"),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
