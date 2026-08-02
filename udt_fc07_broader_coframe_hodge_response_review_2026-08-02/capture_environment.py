#!/usr/bin/env python3
"""Capture correction-review CPU environment."""

from __future__ import annotations

import json
import platform
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent


def main() -> int:
    result = {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "mode": "CPU_STDLIB_COLD_REVIEW_CORRECTION",
        "gpu_used": False,
        "cold_review": "fresh_zero_context_read_only",
    }
    (PACKAGE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
