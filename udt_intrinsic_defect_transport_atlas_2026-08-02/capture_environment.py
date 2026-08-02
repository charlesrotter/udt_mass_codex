#!/usr/bin/env python3
import json
import platform
import subprocess
import sys
from pathlib import Path

import mpmath
import sympy

here = Path(__file__).resolve().parent
root = here.parent
result = {
    "python": sys.version.split()[0],
    "sympy": sympy.__version__,
    "mpmath": mpmath.__version__,
    "platform": platform.platform(),
    "machine": platform.machine(),
    "processor": platform.processor(),
    "git_head_at_capture": subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True
    ).stdout.strip(),
    "method": "CPU_exact_SymPy_plus_90_digit_mpmath_independent_route",
    "gpu_used": False,
}
(here / "RUN_ENVIRONMENT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
