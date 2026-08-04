#!/usr/bin/env python3
from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy

here = Path(__file__).resolve().parent
root = here.parent
record = {
    "python": sys.version.split()[0],
    "sympy": sympy.__version__,
    "platform": platform.platform(),
    "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
    "mode": "CPU_ONLY",
}
(here / "RUN_ENVIRONMENT.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(record, sort_keys=True))

