#!/usr/bin/env python3
"""Run all three CPU audit stages and preserve raw streams and hashes."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PINNED = "/tmp/udt_bootstrap_response_sympy_114_target"
STAGES = (
    ("production", "derive_orchestra_rehearsal.py"),
    ("independent", "verify_orchestra_independent.py"),
    ("diffgeom", "verify_orchestra_diffgeom.py"),
    ("audit", "verify_orchestra_audit.py"),
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    env = dict(os.environ)
    env.update({"PYTHONPATH": PINNED, "CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    records = []
    for stage, script in STAGES:
        command = [sys.executable, str(HERE / script)]
        result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=False)
        stdout_name = f"{stage.upper()}_STDOUT.txt"
        stderr_name = f"{stage.upper()}_STDERR.txt"
        (HERE / stdout_name).write_bytes(result.stdout)
        (HERE / stderr_name).write_bytes(result.stderr)
        records.append({
            "stage": stage,
            "command": f"PYTHONPATH={PINNED} CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 "
                       f"{sys.executable} {HERE.name}/{script}",
            "exit_code": result.returncode,
            "stdout": stdout_name,
            "stdout_sha256": digest(result.stdout),
            "stderr": stderr_name,
            "stderr_sha256": digest(result.stderr),
        })
        if result.returncode:
            raise SystemExit(result.returncode)
    output = {
        "schema": "udt-metric-orchestra-run-1.0",
        "python": sys.version.split()[0],
        "cpu_only": True,
        "gpu_process_launched": False,
        "pinned_pythonpath": PINNED,
        "stages": records,
        "result": "PASS",
    }
    (HERE / "RUN_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n",
                                           encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
