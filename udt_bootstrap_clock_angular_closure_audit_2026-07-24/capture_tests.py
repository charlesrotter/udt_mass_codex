#!/usr/bin/env python3
"""Run the repository test suite and preserve its exact output."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
command = [sys.executable, "-m", "pytest", "tests"]
completed = subprocess.run(
    command,
    cwd=ROOT,
    text=False,
    capture_output=True,
    check=False,
)
(HERE / "TEST_STDOUT.txt").write_bytes(completed.stdout)
(HERE / "TEST_STDERR.txt").write_bytes(completed.stderr)
text = completed.stdout.decode("utf-8", errors="replace")
passed = re.search(r"(\d+) passed", text)
xfailed = re.search(r"(\d+) xfailed", text)
record = {
    "schema": "udt-bootstrap-clock-angular-tests-1.0",
    "command": command,
    "exit_code": completed.returncode,
    "passed": int(passed.group(1)) if passed else None,
    "xfailed": int(xfailed.group(1)) if xfailed else 0,
    "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
    "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
}
(HERE / "TEST_RESULT.json").write_text(
    json.dumps(record, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps(record, indent=2, sort_keys=True))
if completed.returncode != 0:
    raise SystemExit(completed.returncode)
