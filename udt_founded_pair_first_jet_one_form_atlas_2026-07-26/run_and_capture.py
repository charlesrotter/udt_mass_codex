#!/usr/bin/env python3
"""Run one command with CPU-only environment and capture stdout/stderr."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("usage: run_and_capture.py STDOUT STDERR COMMAND...")
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(sys.argv[3:], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    Path(sys.argv[1]).write_bytes(result.stdout)
    Path(sys.argv[2]).write_bytes(result.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
