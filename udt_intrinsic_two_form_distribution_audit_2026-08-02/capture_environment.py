#!/usr/bin/env python3
"""Capture the bounded CPU environment used by this exact audit."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy


here = Path(__file__).resolve().parent
root = here.parent
head = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True
).stdout.strip()
result = {
    "schema": "udt-intrinsic-two-form-run-environment-1.0",
    "git_head_at_capture": head,
    "python": sys.version,
    "sympy": sympy.__version__,
    "platform": platform.platform(),
    "processor_mode": "CPU_EXACT_SYMBOLIC",
    "gpu_used": False,
}
(here / "RUN_ENVIRONMENT.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(result, sort_keys=True))
