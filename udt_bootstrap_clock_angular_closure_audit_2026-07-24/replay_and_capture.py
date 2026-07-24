#!/usr/bin/env python3
"""Replay production and independent checks and preserve raw streams."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = os.environ.get("UDT_SYMPY_TARGET", "")
if not TARGET:
    raise SystemExit("UDT_SYMPY_TARGET must name an isolated SymPy 1.14.0 target")

environment = os.environ.copy()
environment["PYTHONPATH"] = TARGET

commands = [
    (
        "production",
        [sys.executable, "derive_bootstrap_closure.py"],
        environment,
        "PRODUCTION_STDOUT.txt",
        "PRODUCTION_STDERR.txt",
    ),
    (
        "independent",
        [sys.executable, "verify_bootstrap_closure_independent.py"],
        os.environ.copy(),
        "INDEPENDENT_STDOUT.txt",
        "INDEPENDENT_STDERR.txt",
    ),
]

records = []
for label, command, env, stdout_name, stderr_name in commands:
    completed = subprocess.run(
        command,
        cwd=HERE,
        env=env,
        text=False,
        capture_output=True,
        check=False,
    )
    (HERE / stdout_name).write_bytes(completed.stdout)
    (HERE / stderr_name).write_bytes(completed.stderr)
    records.append(
        {
            "label": label,
            "command": command,
            "exit_code": completed.returncode,
            "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
        }
    )
    if completed.returncode != 0:
        raise SystemExit(f"{label} failed: {completed.returncode}")

version = subprocess.run(
    [sys.executable, "-c", "import sympy; print(sympy.__version__)"],
    env=environment,
    text=True,
    capture_output=True,
    check=True,
).stdout.strip()
if version != "1.14.0":
    raise SystemExit(f"wrong pinned SymPy version: {version}")

record = {
    "schema": "udt-bootstrap-clock-angular-replay-environment-1.0",
    "python": platform.python_version(),
    "platform": platform.platform(),
    "sympy": version,
    "isolated_target": TARGET,
    "commands": records,
}
(HERE / "RUN_ENVIRONMENT.json").write_text(
    json.dumps(record, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps(record, indent=2, sort_keys=True))
