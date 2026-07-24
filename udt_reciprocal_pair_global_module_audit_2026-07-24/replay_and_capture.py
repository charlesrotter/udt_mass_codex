#!/usr/bin/env python3
"""Replay production and independent routes and capture exact streams."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(script: str, prefix: str) -> dict[str, object]:
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
    (HERE / f"{prefix}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{prefix}_STDERR.txt").write_bytes(completed.stderr)
    if completed.returncode:
        raise SystemExit(
            completed.stderr.decode("utf-8", "replace")
            or completed.stdout.decode("utf-8", "replace")
        )
    return {
        "command": f"CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 {sys.executable} {script}",
        "exit_code": completed.returncode,
        "stdout_sha256": sha(completed.stdout),
        "stderr_sha256": sha(completed.stderr),
        "stdout_bytes": len(completed.stdout),
        "stderr_bytes": len(completed.stderr),
    }


def main() -> None:
    production = run("derive_pair_global_module.py", "PRODUCTION")
    independent = run(
        "verify_pair_global_module_independent.py", "INDEPENDENT"
    )
    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "cpu_only": True,
        "cuda_visible_devices": "",
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
