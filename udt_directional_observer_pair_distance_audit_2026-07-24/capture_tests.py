#!/usr/bin/env python3
"""Capture the documented CPU-only repository test baseline."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/"],
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / "TEST_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / "TEST_STDERR.txt").write_bytes(completed.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    print(completed.stdout.decode("utf-8", errors="replace"), end="")


if __name__ == "__main__":
    main()
