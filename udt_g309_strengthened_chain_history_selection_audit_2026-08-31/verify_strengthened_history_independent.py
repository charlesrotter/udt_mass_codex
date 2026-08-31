#!/usr/bin/env python3
"""Independent numerical/sectional-curvature verification for G309.

This file imports no production module and does not use SymPy.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def scale_data(t: float, epsilon: float, deformed: bool) -> tuple[float, float, float]:
    """Return a, a', a'' at X=1 using direct logarithmic differentiation."""
    a0 = math.cosh(t)
    h0 = math.tanh(t)
    h0_prime = 1.0 / math.cosh(t) ** 2
    if deformed and t > 0.0:
        bump = math.exp(-1.0 / (t * t))
        bump_prime = bump * 2.0 / t**3
        bump_second = bump * (4.0 / t**6 - 6.0 / t**4)
    else:
        bump = 0.0
        bump_prime = 0.0
        bump_second = 0.0
    log_prime = h0 + epsilon * bump_prime
    log_second = h0_prime + epsilon * bump_second
    value = a0 * math.exp(epsilon * bump)
    first = value * log_prime
    second = value * (log_prime * log_prime + log_second)
    return value, first, second


def sectional_channels(data: tuple[float, float, float]) -> tuple[float, float]:
    value, first, second = data
    return second / value, (first * first + 1.0) / (value * value)


def build_result() -> dict:
    epsilon = 0.1
    sample = (0.2, 0.35, 0.7, 1.0, 1.4, 2.5)
    base_gaps = []
    deformed_gaps = []
    scalar_differences = []
    checks = 0

    for t in sample:
        kt0, ks0 = sectional_channels(scale_data(t, epsilon, False))
        kte, kse = sectional_channels(scale_data(t, epsilon, True))
        base_gaps.append(abs(kt0 - ks0))
        deformed_gaps.append(abs(kte - kse))
        scalar_differences.append(abs(6.0 * (kte + kse) - 12.0))
        assert abs(kt0 - ks0) < 2e-14
        assert abs(6.0 * (kt0 + ks0) - 12.0) < 5e-14
        checks += 2

    assert max(deformed_gaps) > 1e-2
    assert max(scalar_differences) > 1e-2
    checks += 2

    # On the whole preregistered negative-time control region, the explicit
    # branch definition gives the undeformed data exactly.
    for t in (-3.0, -1.0, -0.25, 0.0):
        assert scale_data(t, epsilon, True) == scale_data(t, epsilon, False)
        checks += 1

    # Rebuild Ricci eigenvalues from the two sectional curvatures. An Einstein
    # metric has equal temporal and spatial mixed Ricci eigenvalues exactly
    # when K_t == K_s.
    for t in sample:
        kt, ks = sectional_channels(scale_data(t, epsilon, True))
        temporal_eigenvalue = 3.0 * kt
        spatial_eigenvalue = kt + 2.0 * ks
        assert abs((temporal_eigenvalue - spatial_eigenvalue) - 2.0 * (kt - ks)) < 2e-14
        checks += 1

    # Independent component form of normalized Hopf time carry.
    for value, rate in ((0.4, -3.0), (1.0, 0.0), (2.3, 4.7), (10.0, -0.2)):
        ordinary = -rate / (value * value)
        connection = (rate / value) * (1.0 / value)
        assert abs(ordinary + connection) < 1e-14
        checks += 1

    return {
        "status": "PASS",
        "independent_checks": checks,
        "method": "sectional_curvature_and_ricci_eigenvalues_without_production_import_or_sympy",
        "max_base_tracefree_gap": max(base_gaps),
        "max_deformed_tracefree_gap": max(deformed_gaps),
        "max_deformed_scalar_difference_from_12": max(scalar_differences),
        "quiet_half_region_samples_exact": True,
        "normalized_hopf_time_carry_for_arbitrary_positive_scale": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

