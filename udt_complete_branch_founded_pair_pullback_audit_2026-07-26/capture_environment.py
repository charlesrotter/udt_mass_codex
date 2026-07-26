#!/usr/bin/env python3
import json
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
data = {
    "python": sys.version,
    "platform": platform.platform(),
    "sympy": __import__("sympy").__version__,
    "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "cuda_visible_devices": "",
    "cpu_only": True,
}
(HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(data, indent=2, sort_keys=True))
