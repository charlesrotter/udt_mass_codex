#!/usr/bin/env python3
"""Capture the CPU/SymPy environment for the production audit."""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import sympy


PACKAGE = Path(__file__).resolve().parent


def main() -> int:
    result = {
        "python": sys.version,
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "mode": "CPU_EXACT_SYMBOLIC",
        "gpu_used": False,
        "fresh_blind_review": False,
    }
    (PACKAGE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

