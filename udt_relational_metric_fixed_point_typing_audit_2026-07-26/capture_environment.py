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
    "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "cpu_only": True,
    "external_dependencies": [],
}
(HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(data, indent=2, sort_keys=True))
