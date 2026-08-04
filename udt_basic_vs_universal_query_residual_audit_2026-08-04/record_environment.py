#!/usr/bin/env python3
from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import sympy

HERE = Path(__file__).resolve().parent

result = {
    "execution": "CPU_ONLY",
    "platform": platform.platform(),
    "python": sys.version.split()[0],
    "sympy": sympy.__version__,
}
(HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
