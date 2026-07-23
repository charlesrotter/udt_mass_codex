#!/usr/bin/env python3
"""Capture the current CPU-only repository test baseline."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> None:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/"],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=300,
        check=False,
    )
    stdout = completed.stdout.decode("utf-8", "replace")
    summary = re.search(r"(\d+) passed, (\d+) xfailed", stdout)
    if (
        completed.returncode != 0
        or summary is None
        or tuple(map(int, summary.groups())) != (70, 1)
        or " failed" in stdout
    ):
        raise AssertionError("test baseline mismatch")
    (HERE / "FULL_TEST_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / "FULL_TEST_STDERR.txt").write_bytes(completed.stderr)
    result = {
        "schema": "udt-coframe-hopf-test-baseline-v1",
        "command": (
            "CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 "
            "python3 -m pytest tests/"
        ),
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
