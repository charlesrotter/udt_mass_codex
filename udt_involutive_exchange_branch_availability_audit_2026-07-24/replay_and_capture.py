#!/usr/bin/env python3
"""Replay both audit implementations and capture exact execution evidence."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run(script: str, stem: str) -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    completed = subprocess.run(
        [sys.executable, script],
        cwd=HERE,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / f"{stem}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(completed.stderr)
    if completed.returncode:
        raise SystemExit(
            f"{script} failed with {completed.returncode}: "
            f"{completed.stderr.decode(errors='replace')}"
        )
    return {
        "command": f"PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 {script}",
        "exit_code": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
    }


def main() -> None:
    production = run("derive_branch_availability.py", "PRODUCTION")
    independent = run(
        "verify_branch_availability_independent.py", "INDEPENDENT"
    )
    environment = {
        "schema": "udt-involutive-exchange-branch-run-environment-v1",
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "cuda_visible_devices": "",
        "external_dependencies": [],
        "production": production,
        "independent": independent,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(environment, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
