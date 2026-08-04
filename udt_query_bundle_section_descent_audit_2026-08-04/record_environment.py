#!/usr/bin/env python3
"""Record the bounded CPU audit environment."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
result = {
    "python": sys.version.split()[0],
    "sympy": sympy.__version__,
    "platform": platform.platform(),
    "machine": platform.machine(),
    "git_head_at_run": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "compute": "CPU exact algebra only",
}
(HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
