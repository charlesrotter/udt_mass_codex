#!/usr/bin/env python3
"""Run and capture the repository test baseline."""

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
    sys.stdout.buffer.write(completed.stdout)
    sys.stderr.buffer.write(completed.stderr)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
