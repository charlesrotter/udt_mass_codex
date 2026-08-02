#!/usr/bin/env python3
"""Capture the exact bounded CPU environment."""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path

import sympy


PACKAGE = Path(__file__).resolve().parent


def main() -> int:
    data = {
        "python": sys.version,
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "mode": "CPU_EXACT_AND_STDLIB_INDEPENDENT",
        "gpu_used": False,
    }
    (PACKAGE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(data, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
