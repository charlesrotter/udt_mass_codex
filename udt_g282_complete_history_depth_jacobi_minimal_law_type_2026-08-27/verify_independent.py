#!/usr/bin/env python3
"""Independent standard-library G282 witness check; imports no production code."""

from __future__ import annotations

import json
import math
import random


def rk4_step(state: tuple[float, float], step: float, sign_a: float) -> tuple[float, float]:
    def rhs(value: tuple[float, float]) -> tuple[float, float]:
        return value[1], sign_a * value[0]

    y, p = state
    k1 = rhs((y, p))
    k2 = rhs((y + step * k1[0] / 2, p + step * k1[1] / 2))
    k3 = rhs((y + step * k2[0] / 2, p + step * k2[1] / 2))
    k4 = rhs((y + step * k3[0], p + step * k3[1]))
    return (
        y + step * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6,
        p + step * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6,
    )


def integrate(length: float, a: float, steps: int = 800) -> tuple[float, float]:
    step = length / steps
    x_state = (0.0, 1.0)
    y_state = (0.0, 1.0)
    for _ in range(steps):
        x_state = rk4_step(x_state, step, a)
        y_state = rk4_step(y_state, step, -a)
    return x_state[0], y_state[0]


def main() -> None:
    rng = random.Random(282)
    cases = 512
    assertions = 0
    maximum_component_error = 0.0
    maximum_area_error = 0.0
    area_separators = 0

    for _ in range(cases):
        a = rng.uniform(0.05, 3.0)
        q = math.sqrt(a)
        length = rng.uniform(0.02, min(1.0, 0.8 * math.pi / q))
        dx_num, dy_num = integrate(length, a)
        dx_exact = math.sinh(q * length) / q
        dy_exact = math.sin(q * length) / q
        maximum_component_error = max(
            maximum_component_error,
            abs(dx_num - dx_exact),
            abs(dy_num - dy_exact),
        )
        area_num = dx_num * dy_num
        area_exact = dx_exact * dy_exact
        maximum_area_error = max(maximum_area_error, abs(area_num - area_exact))
        assertions += 3
        assert abs(dx_num - dx_exact) < 3e-12
        assert abs(dy_num - dy_exact) < 3e-12
        assert abs(area_num - area_exact) < 5e-12

        flat_area = length * length
        assertions += 1
        assert not math.isclose(area_exact, flat_area, rel_tol=0.0, abs_tol=1e-14)
        area_separators += 1

        depth = rng.uniform(0.01, 5.0)
        s_a = math.sqrt(depth)
        s_b = math.sqrt((-1.0 + math.sqrt(1.0 + 4.0 * depth)) / 2.0)
        assertions += 3
        assert math.isclose(s_a * s_a, depth, abs_tol=2e-15)
        assert math.isclose(s_b * s_b + s_b**4, depth, abs_tol=4e-15)
        assert not math.isclose(s_a, s_b, rel_tol=0.0, abs_tol=1e-14)

    checks = {
        "all_numerical_jacobi_cases_match_exact": area_separators == cases,
        "all_same_depth_primary_cases_separate_area": area_separators == cases,
        "maximum_component_error_below_3e_12": maximum_component_error < 3e-12,
        "maximum_area_error_below_5e_12": maximum_area_error < 5e-12,
    }
    assert all(checks.values())
    print(
        json.dumps(
            {
                "audit": "G282_INDEPENDENT_NEIGHBOR_RAY_CHECK",
                "status": "PASS",
                "checks": checks,
                "cases": cases,
                "assertions": assertions,
                "maximum_component_error": maximum_component_error,
                "maximum_area_error": maximum_area_error,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
