#!/usr/bin/env python3
"""Post-review numerical diagnostics registered by G350 repair R3."""

import json
import math
import os
import random
from pathlib import Path


TOL = 2.0e-11
SEED = 3500531
DIRECT_CASES = 2000
LOG_DOMAIN_CASES = 2000


def mixed_absolute_relative_normalized_error(left, right):
    return abs(left - right) / max(1.0, abs(left), abs(right))


def main():
    rng = random.Random(SEED)
    max_mixed_error = 0.0
    max_log_error = 0.0
    checks = 0

    for _ in range(DIRECT_CASES):
        x0, x1, x2 = [rng.uniform(-12.0, 12.0) for _ in range(3)]
        y0, y1, y2 = [rng.uniform(-12.0, 12.0) for _ in range(3)]
        p, q = rng.uniform(-2.5, 2.5), rng.uniform(-2.5, 2.5)
        direct_log = p * (x2 - x0) + q * (y2 - y0)
        first_log = p * (x1 - x0) + q * (y1 - y0)
        second_log = p * (x2 - x1) + q * (y2 - y1)
        direct = math.exp(direct_log)
        sewn = math.exp(second_log) * math.exp(first_log)
        error = mixed_absolute_relative_normalized_error(direct, sewn)
        max_mixed_error = max(max_mixed_error, error)
        checks += 1
        if error > TOL:
            raise AssertionError((direct, sewn, error))

    # Work in logarithms so transfers far below direct floating tolerances remain visible.
    for _ in range(LOG_DOMAIN_CASES):
        x0, x1, x2 = [rng.uniform(-450.0, 450.0) for _ in range(3)]
        y0, y1, y2 = [rng.uniform(-450.0, 450.0) for _ in range(3)]
        p, q = rng.uniform(-2.5, 2.5), rng.uniform(-2.5, 2.5)
        direct_log = p * (x2 - x0) + q * (y2 - y0)
        sewn_log = p * (x2 - x1) + q * (y2 - y1)
        sewn_log += p * (x1 - x0) + q * (y1 - y0)
        error = abs(direct_log - sewn_log)
        max_log_error = max(max_log_error, error)
        checks += 1
        if error > TOL:
            raise AssertionError((direct_log, sewn_log, error))

    result = {
        "all_passed": True,
        "checks_passed": checks,
        "checks_total": checks,
        "direct_cases": DIRECT_CASES,
        "log_domain_cases": LOG_DOMAIN_CASES,
        "max_mixed_absolute_relative_normalized_error": max_mixed_error,
        "max_log_domain_absolute_error": max_log_error,
        "seed": SEED,
        "tolerance": TOL,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") == "1":
        print(rendered, end="")
    else:
        Path("REPAIR_NUMERICS_RESULT.json").write_text(rendered, encoding="utf-8")
        print(rendered, end="")


if __name__ == "__main__":
    main()
