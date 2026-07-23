#!/usr/bin/env python3
"""Run and record the current full CPU-only repository test baseline."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def main() -> None:
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = ""
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-m", "pytest", "tests/"]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )
    summary = re.search(r"(\d+) passed, (\d+) xfailed", completed.stdout)
    if (
        completed.returncode != 0
        or summary is None
        or tuple(map(int, summary.groups())) != (70, 1)
    ):
        raise AssertionError("full test baseline did not match 70 passed / 1 xfailed")
    (HERE / "FULL_TEST_STDOUT.txt").write_text(
        completed.stdout, encoding="utf-8"
    )
    (HERE / "FULL_TEST_STDERR.txt").write_text(
        completed.stderr, encoding="utf-8"
    )
    result = {
        "schema": "udt-hygiene-current-test-baseline-1.0",
        "command": "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/",
        "exit_code": completed.returncode,
        "passed": 70,
        "failed": 0,
        "xfailed": 1,
        "stdout_sha256": digest(completed.stdout),
        "stderr_sha256": digest(completed.stderr),
        "result": "PASS",
    }
    (HERE / "FULL_TEST_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
