#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    completed = subprocess.run(
        [sys.executable, str(HERE / "verify_audit.py")], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    (HERE / "VERIFICATION_STDOUT.txt").write_text(completed.stdout, encoding="utf-8")
    (HERE / "VERIFICATION_STDERR.txt").write_text(completed.stderr, encoding="utf-8")
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    print("PASS verification capture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
