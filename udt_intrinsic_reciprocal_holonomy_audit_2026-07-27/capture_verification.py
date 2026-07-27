#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    done = subprocess.run(
        [sys.executable, str(HERE / "verify_audit.py")], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    (HERE / "VERIFICATION_STDOUT.txt").write_text(done.stdout, encoding="utf-8")
    (HERE / "VERIFICATION_STDERR.txt").write_text(done.stderr, encoding="utf-8")
    if done.returncode:
        raise AssertionError(done.stderr or done.stdout)
    print("PASS verification capture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
