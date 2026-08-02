#!/usr/bin/env python3
"""Replay the fresh reviewer's independent scripts with normalized raw captures."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

import torch


HERE = Path(__file__).resolve().parent
COMMANDS = (
    ("coordinate", [sys.executable, str(HERE / "verify_intrinsic_contact_coordinate.py")], 300),
    ("exact_values", [sys.executable, str(HERE / "exact_contact_values.py")], 60),
)
records = []
for label, command, timeout in COMMANDS:
    result = subprocess.run(command, cwd=HERE, text=True, capture_output=True, timeout=timeout, check=False)
    (HERE / f"{label}.stdout.txt").write_text(result.stdout, encoding="utf-8")
    (HERE / f"{label}.stderr.txt").write_text(result.stderr, encoding="utf-8")
    records.append({"label": label, "command": command, "exit_code": result.returncode})
    if result.returncode != 0:
        raise SystemExit(f"{label} failed with exit {result.returncode}")
environment = {
    "python": sys.version,
    "platform": platform.platform(),
    "torch": torch.__version__,
    "dtype": "torch.float64",
    "device": "CPU",
    "cuda_available": torch.cuda.is_available(),
}
(HERE / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
(HERE / "run_log.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"environment": environment, "runs": records}, sort_keys=True))
