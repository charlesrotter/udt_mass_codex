#!/usr/bin/env python3
"""Run the bounded scientific subprocess and preserve stdout/stderr/exit/hash evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
command = [sys.executable, str(HERE / "check_record_types.py")]
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
started = stamp()
start_clock = time.monotonic()
record = {"command_argv": command, "cwd": str(ROOT), "timeout_seconds": 120,
          "started_utc": started, "runtime_model": "UNATTESTED",
          "purpose": "Independent implementation construction check; not independent adversarial review"}
for filename in ("CONSTRUCTION_FREEZE.md", "check_record_types.py", "run_record_checks.py"):
    record[filename + "_sha256_before_run"] = hashlib.sha256((HERE / filename).read_bytes()).hexdigest()
try:
    proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    stdout, stderr, exit_code = proc.stdout, proc.stderr, proc.returncode
    record["timeout"] = False
except subprocess.TimeoutExpired as exc:
    stdout, stderr, exit_code = exc.stdout or "", exc.stderr or "", 124
    if isinstance(stdout, bytes):
        stdout = stdout.decode(errors="replace")
    if isinstance(stderr, bytes):
        stderr = stderr.decode(errors="replace")
    record["timeout"] = True
(HERE / "RECORD_CHECK_STDOUT.json").write_text(stdout)
(HERE / "RECORD_CHECK_STDERR.txt").write_text(stderr)
record.update({"finished_utc": stamp(), "elapsed_seconds": time.monotonic() - start_clock,
               "exit_code": exit_code,
               "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
               "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest()})
(HERE / "RECORD_CHECK_RUN.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
raise SystemExit(exit_code)
