#!/usr/bin/env python3
"""Capture the exact CPU software environment for this audit."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
result = {
    "python": sys.version,
    "platform": platform.platform(),
    "processor": platform.processor(),
    "logical_cpu_count": os.cpu_count(),
    "sympy": sympy.__version__,
    "git_head_at_capture": subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip(),
    "device": "CPU",
    "gpu_used": False,
    "exact_worker_count": 4,
}
(HERE / "RUN_ENVIRONMENT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps(result, sort_keys=True))
