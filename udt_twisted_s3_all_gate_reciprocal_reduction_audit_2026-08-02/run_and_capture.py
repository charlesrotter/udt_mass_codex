#!/usr/bin/env python3
"""Run exact derivation, adjudication, independent replay, and repository gates with captures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
commands = (
    ("ENVIRONMENT", [sys.executable, str(HERE / "capture_environment.py")], 60),
    ("EXACT_DERIVATION", [sys.executable, str(HERE / "derive_invariant_certificate.py")], 600),
    ("ADJUDICATION", [sys.executable, str(HERE / "derive_adjudication.py")], 120),
    ("INDEPENDENT_REVIEW", [sys.executable, str(HERE / "independent_review/run_independent_capture.py")], 300),
    ("REPOSITORY_GATES", [sys.executable, str(HERE / "verify_repository_gates.py")], 600),
)
records = []
for label, command, timeout in commands:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
    (HERE / f"{label}_STDOUT.txt").write_text(result.stdout, encoding="utf-8")
    (HERE / f"{label}_STDERR.txt").write_text(result.stderr, encoding="utf-8")
    records.append({"label": label, "command": command, "exit_code": result.returncode})
    if result.returncode != 0:
        raise SystemExit(f"{label} failed with exit {result.returncode}")
(HERE / "RUN_LOG.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
print(json.dumps(records, sort_keys=True))
