#!/usr/bin/env python3
"""Run and capture the two exact implementations in bounded CPU processes."""

from __future__ import annotations

import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def capture(script: str, prefix: str) -> None:
    result = subprocess.run(
        ["python3", str(HERE / script)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    (HERE / f"{prefix}_STDOUT.txt").write_text(result.stdout, encoding="utf-8")
    (HERE / f"{prefix}_STDERR.txt").write_text(result.stderr, encoding="utf-8")
    assert result.returncode == 0, (script, result.returncode, result.stderr)
    assert '"status": "PASS"' in result.stdout


capture("derive_descent_atlas.py", "PRODUCTION")
capture("verify_descent_independent.py", "INDEPENDENT")
print("PASS production_and_independent_captured")
