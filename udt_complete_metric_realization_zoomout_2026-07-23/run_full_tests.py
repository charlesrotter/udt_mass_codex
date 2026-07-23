#!/usr/bin/env python3
"""Run and record the current repository test baseline."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    command = [sys.executable, "-m", "pytest", "-q"]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True)
    (HERE / "FULL_TEST_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / "FULL_TEST_STDERR.txt").write_bytes(completed.stderr)
    text = (completed.stdout + completed.stderr).decode(
        "utf-8", errors="replace"
    )
    passed_match = re.search(r"(\d+) passed", text)
    xfailed_match = re.search(r"(\d+) xfailed", text)
    failed_match = re.search(r"(\d+) failed", text)
    result = {
        "schema": "udt-full-test-result-v1",
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "passed": int(passed_match.group(1)) if passed_match else 0,
        "failed": int(failed_match.group(1)) if failed_match else 0,
        "xfailed": int(xfailed_match.group(1)) if xfailed_match else 0,
    }
    (HERE / "FULL_TEST_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if completed.returncode:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
