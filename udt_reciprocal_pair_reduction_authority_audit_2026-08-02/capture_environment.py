#!/usr/bin/env python3
"""Capture the CPU source-adjudication environment."""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
result = {
    "python": platform.python_version(),
    "python_executable": sys.executable,
    "platform": platform.platform(),
    "device": "CPU_ONLY",
    "external_dependencies": "NONE",
}
(HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
