#!/usr/bin/env python3
"""Run and record the exact bounded CPU replay commands."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
PINNED = "/tmp/udt_phi_angular_xmax_pinned"


def execute(name: str, command: list[str], extra_env: dict[str, str] | None = None) -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    if extra_env:
        env.update(extra_env)
    result = subprocess.run(
        command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, check=False,
    )
    record = {
        "name": name,
        "command": command,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest(),
    }
    if result.returncode:
        raise AssertionError(record)
    return record


def main() -> None:
    pinned_env = {"PYTHONPATH": PINNED}
    pinned_version = execute(
        "pinned_versions",
        [sys.executable, "-c", "import sys,sympy; print(sys.version.split()[0]); print(sympy.__version__)"],
        pinned_env,
    )
    records = [
        pinned_version,
        execute(
            "production_build",
            [sys.executable, str(OUT / "build_atlas.py")],
            pinned_env,
        ),
        execute(
            "independent_fraction_replay",
            [sys.executable, str(OUT / "verify_independent.py")],
        ),
        execute(
            "fail_closed_verifier",
            [sys.executable, str(OUT / "verify_atlas.py")],
        ),
    ]
    output = {
        "schema": "udt-macro-phi-angular-xmax-run-log-1.0",
        "result": "PASS",
        "cpu_only": True,
        "records": records,
    }
    (OUT / "RUN_LOG.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"result": "PASS", "records": len(records)}, sort_keys=True))


if __name__ == "__main__":
    main()
