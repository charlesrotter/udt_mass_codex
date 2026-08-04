#!/usr/bin/env python3
"""Run bounded production and independent selector checks with raw capture."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


records = []
for label, script in (
    ("PRODUCTION", "derive_selector_atlas.py"),
    ("INDEPENDENT", "verify_selector_independent.py"),
):
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        capture_output=True,
        timeout=120,
        check=False,
    )
    (HERE / f"{label}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{label}_STDERR.txt").write_bytes(completed.stderr)
    records.append(
        {
            "label": label,
            "command": f"{sys.executable} {HERE.name}/{script}",
            "exit_code": completed.returncode,
            "stdout_sha256": digest(completed.stdout),
            "stderr_sha256": digest(completed.stderr),
        }
    )
    assert completed.returncode == 0, (label, completed.stderr.decode(errors="replace"))

environment = {
    "python": platform.python_version(),
    "sympy": sympy.__version__,
    "platform": platform.platform(),
    "cpu_only": True,
    "gpu_used": False,
    "runs": records,
}
(HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(environment, sort_keys=True))
