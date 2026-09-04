#!/usr/bin/env python3
"""Independent numerical reconstruction of the bounded G338 pair result.

This verifier neither imports the production module nor reads its JSON output.
"""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


LANDING = (
    "EXPLICIT_LAWFUL_TAUB_DEVELOPMENT_CARRIES_NATIVE_COMPLETED_PAIR_RESPONSE_FOR_FINITE_TIME"
    "__ZERO_BOOST_TERMINAL_BLINDNESS_COEXISTS_WITH_NONTRIVIAL_RULER_DENSITY"
    "__INITIAL_SILENCE_CAN_TURN_ON_EXACTLY__NO_OCCUPANCY_OR_SCALE_SELECTION"
)


def contract(v: tuple[float, float], w: tuple[float, float], spatial_norm: float) -> float:
    return -v[0] * w[0] + spatial_norm * v[1] * w[1]


def evolved_spatial_norm(u: float, rho: float) -> float:
    return rho * u ** (-2.0 / 3.0) + (1.0 - rho) * u ** (4.0 / 3.0)


def bisect_root(func, lo: float, hi: float, iterations: int = 120) -> float:
    flo = func(lo)
    fhi = func(hi)
    if flo * fhi >= 0:
        raise AssertionError("root_not_bracketed")
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        fm = func(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def main() -> None:
    rng = random.Random(338)
    checks: dict[str, bool] = {}
    max_det_error = 0.0
    max_w1_error = 0.0
    regular_cases = 0

    # Rebuild the pullback directly from two carried basis vectors.
    for i in range(500):
        log_u = rng.uniform(-5.0, 5.0)
        u = math.exp(log_u)
        rho = rng.random()
        z = rng.uniform(-2.0, 2.0)
        G = evolved_spatial_norm(u, rho)
        c, s = math.cosh(z), math.sinh(z)
        e0 = (c, s)
        e1 = (s, c)
        h00 = contract(e0, e0, G)
        h01 = contract(e0, e1, G)
        h11 = contract(e1, e1, G)
        det = h00 * h11 - h01 * h01
        det_error = abs(det + G) / max(1.0, G)
        max_det_error = max(max_det_error, det_error)
        if det_error >= 2e-11:
            raise AssertionError(f"direct_pullback_determinant_{i}")

        Delta = -h00
        if Delta <= 0:
            continue
        regular_cases += 1
        L2 = h11 - h01 * h01 / h00
        # Independent ruler calibration ds=sqrt(G) d-sigma.
        h00s = h00
        h01s = h01 / math.sqrt(G)
        h11s = h11 / G
        dets = h00s * h11s - h01s * h01s
        reciprocal_error = max(abs(dets + 1.0), abs(Delta * L2 / G - 1.0))
        max_w1_error = max(max_w1_error, reciprocal_error)
        if reciprocal_error >= 3e-10:
            raise AssertionError(f"independent_w1_{i}")
        phi = -0.5 * math.log(Delta)
        chi_direct = math.tanh(phi)
        chi_projective = (1.0 - Delta) / (1.0 + Delta)
        if abs(chi_direct - chi_projective) >= 3e-14:
            raise AssertionError(f"independent_projective_{i}")

    checks["direct_pullback_random_sweep"] = max_det_error < 2e-11
    checks["independent_w1_random_sweep"] = max_w1_error < 3e-10
    checks["random_regular_cases_nonempty"] = regular_cases > 100

    # Independent finite-difference test of the exactly silent initial direction.
    rho = 2.0 / 3.0
    h = 2.0e-4
    values = [math.sqrt(evolved_spatial_norm(1.0 + k * h, rho)) for k in (-2, -1, 0, 1, 2)]
    first = (values[0] - 8 * values[1] + 8 * values[3] - values[4]) / (12 * h)
    second = (-values[0] + 16 * values[1] - 30 * values[2] + 16 * values[3] - values[4]) / (12 * h * h)
    checks["silent_first_derivative_numerically_zero"] = abs(first) < 2e-12
    checks["silent_second_derivative_matches_four_ninths"] = abs(second - 4.0 / 9.0) < 2e-8

    # It turns on on both finite-time sides, with no Taylor truncation involved.
    checks["silent_exact_finite_time_turn_on"] = all(
        evolved_spatial_norm(u, rho) > 1.0
        for u in (0.02, 0.2, 0.8, 1.2, 5.0, 50.0)
    )

    # Independently locate the two regular-stratum boundaries for mixed directions.
    z = 0.8
    threshold = (math.cosh(z) / math.sinh(z)) ** 2
    for i, rho in enumerate((0.1, 0.5, 2.0 / 3.0, 0.9)):
        residual = lambda u, rho=rho: evolved_spatial_norm(u, rho) - threshold
        left = bisect_root(residual, 1e-10, 1.0)
        right = bisect_root(residual, 1.0, 1e10)
        checks[f"mixed_two_boundaries_{i}"] = left < 1.0 < right and abs(residual(left)) < 2e-8 and abs(residual(right)) < 2e-5

    # Endpoint directions have the independently predicted closed-form boundaries.
    tanh_z = math.tanh(z)
    left_longitudinal = tanh_z**3
    right_transverse = (1.0 / tanh_z) ** 1.5
    checks["longitudinal_closed_boundary"] = abs(evolved_spatial_norm(left_longitudinal, 1.0) - threshold) < 2e-14
    checks["transverse_closed_boundary"] = abs(evolved_spatial_norm(right_transverse, 0.0) - threshold) < 2e-14

    # Zero boost is a deliberate terminal-scalar blindness test.
    zero_boost_phis = []
    zero_boost_densities = []
    for u in (0.1, 0.5, 1.0, 2.0, 10.0):
        G = evolved_spatial_norm(u, 0.37)
        h00 = contract((1.0, 0.0), (1.0, 0.0), G)
        zero_boost_phis.append(-0.5 * math.log(-h00))
        zero_boost_densities.append(math.sqrt(G))
    checks["zero_boost_terminal_blind"] = max(abs(x) for x in zero_boost_phis) == 0.0
    checks["zero_boost_full_pair_not_blind"] = max(zero_boost_densities) - min(zero_boost_densities) > 0.1

    # Separate Ricci-component reconstruction for the source Kasner powers.
    powers = (-1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0)
    ricci00_coefficient = -(sum(x * x for x in powers) - sum(powers))
    riccii_coefficients = [x * (sum(powers) - 1.0) for x in powers]
    checks["source_ricci_reconstruction"] = abs(ricci00_coefficient) < 2e-15 and max(abs(x) for x in riccii_coefficients) < 2e-15

    # A pair boundary at positive T has finite spacetime curvature; it is not
    # automatically a horizon or singularity of the ambient metric.
    boundary_u = right_transverse
    kretschmann_T0_one = 64.0 / (27.0 * boundary_u**4)
    checks["pair_boundary_has_finite_ambient_curvature"] = math.isfinite(kretschmann_T0_one) and kretschmann_T0_one > 0.0

    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise AssertionError(f"independent failures: {failed}")

    result = {
        "landing": LANDING,
        "method": "independent direct-basis numerical reconstruction; no production import or result read",
        "seed": 338,
        "random_cases": 500,
        "regular_cases": regular_cases,
        "max_relative_determinant_error": max_det_error,
        "max_w1_error": max_w1_error,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_passed": all(checks.values()),
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        out = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("landing", "method", "checks_passed", "checks_total", "all_passed")}, indent=2))


if __name__ == "__main__":
    main()
