"""One small, exact same-context algebra check; not independent review."""

import json
import platform
import resource
import sys
import time
from collections import defaultdict


def derivative(expression):
    """Differentiate x**n times 1, sin(x**-2), or cos(x**-2)."""
    result = defaultdict(int)
    for (power, factor), coefficient in expression.items():
        result[power - 1, factor] += power * coefficient
        if factor == "sin":
            result[power - 3, "cos"] -= 2 * coefficient
        elif factor == "cos":
            result[power - 3, "sin"] += 2 * coefficient
        elif factor != "one":
            raise ValueError(factor)
    return {key: value for key, value in result.items() if value}


def phase(expression, sine, cosine):
    """Exact coefficient collection at specified trigonometric phases."""
    result = defaultdict(int)
    values = {"one": 1, "sin": sine, "cos": cosine}
    for (power, factor), coefficient in expression.items():
        result[power] += coefficient * values[factor]
    return {key: value for key, value in result.items() if value}


def encode(expression):
    return [
        {"power": power, "factor": factor, "coefficient": coefficient}
        for (power, factor), coefficient in sorted(expression.items())
    ]


start = time.perf_counter()
original = {(8, "one"): 2, (8, "sin"): 1}
first = derivative(original)
second = derivative(first)
checks = {
    "first_derivative": first == {
        (7, "one"): 16, (7, "sin"): 8, (5, "cos"): -2
    },
    "second_derivative": second == {
        (6, "one"): 112, (6, "sin"): 56,
        (4, "cos"): -26, (2, "sin"): -4
    },
    "negative_curvature_phase": phase(second, 1, 0) == {6: 168, 2: -4},
    "positive_curvature_phase": phase(second, -1, 0) == {6: 56, 2: 4},
    "negative_slope_phase": phase(first, 0, 1) == {7: 16, 5: -2},
    "positive_slope_phase": phase(first, 0, -1) == {7: 16, 5: 2},
}
result = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "first_derivative": encode(first),
    "second_derivative": encode(second),
    "arithmetic": "Python exact integers; no floating-point scientific check",
    "scope": "same-context algebra regression; no independent review",
    "python": sys.version,
    "platform": platform.platform(),
    "elapsed_seconds": time.perf_counter() - start,
    "peak_resident_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}
print(json.dumps(result, indent=2))
sys.exit(0 if all(checks.values()) else 1)
