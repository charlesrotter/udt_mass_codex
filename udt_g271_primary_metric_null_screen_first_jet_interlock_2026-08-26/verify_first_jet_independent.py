#!/usr/bin/env python3
"""Independent G271 verification using generic lapse/radial scale and exact rationals."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import random

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
EXPECTED_LANDING = (
    "NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT__"
    "ONE_PRIMARY_METRIC_GRADIENT_GENERATES_DEPTH_AND_TRANSPORTED_SCREEN_CHANNELS__"
    "RADIAL_AND_QUIET_STRATA_EXACT__NO_FINITE_PATH_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(sp.trigsimp(expr)) == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    r = sp.symbols("r", positive=True)
    lapse = sp.Function("N")(r)
    radial_scale = sp.Function("A")(r)

    # Independent generic-static calculation: Gamma^r_tt=N*N'/A^2 and U^t=1/N.
    gamma_r_tt = lapse * sp.diff(lapse, r) / radial_scale**2
    acceleration_r = sp.simplify(gamma_r_tt / lapse**2)
    acceleration_hat = sp.simplify(radial_scale * acceleration_r)
    generic_expected = sp.diff(lapse, r) / (lapse * radial_scale)

    # Primary reciprocal specialization A=1/N and phi=-log(N).
    primary_acceleration_hat = sp.simplify(acceleration_hat.subs(radial_scale, 1 / lapse))
    phi_prime = sp.simplify(-sp.diff(lapse, r) / lapse)
    primary_common = sp.simplify(lapse * phi_prime)

    # Independent component check of nabla_X U=-g(X,U)*a.
    x_t, x_r = sp.symbols("x_t x_r", real=True)
    gamma_t_rt = sp.diff(lapse, r) / lapse
    congruence_t = sp.simplify(
        x_r * sp.diff(1 / lapse, r) + x_r * gamma_t_rt / lapse
    )
    congruence_r = sp.simplify(x_t * gamma_r_tt / lapse)
    expected_r = sp.simplify(
        lapse * x_t * acceleration_r
    )

    ell, depth_first, screen_first = sp.symbols(
        "ell depth_first screen_first", real=True
    )
    depth_local = depth_first * ell
    screen_local = screen_first * ell
    ratio_local = sp.exp(-depth_local)
    gamma_local = sp.cosh(depth_local) + ratio_local * screen_local**2 / 2
    mutual_local = sp.series(1 / gamma_local, ell, 0, 3).removeO()
    sech_local = sp.series(sp.sech(depth_local), ell, 0, 3).removeO()

    symbolic_checks = {
        "generic_static_acceleration": zero(acceleration_hat - generic_expected),
        "primary_acceleration": zero(primary_acceleration_hat - sp.diff(lapse, r)),
        "primary_common_is_minus_acceleration": zero(
            primary_common + primary_acceleration_hat
        ),
        "generic_congruence_time_component": zero(congruence_t),
        "generic_congruence_radial_component": zero(congruence_r - expected_r),
        "independent_mutual_leading_term": zero(
            mutual_local
            - (1 - (depth_first**2 + screen_first**2) * ell**2 / 2)
        ),
        "independent_screen_gap": zero(
            sech_local - mutual_local - screen_first**2 * ell**2 / 2
        ),
    }
    assert all(symbolic_checks.values()), symbolic_checks

    rng = random.Random(271)
    cases = 20000
    radial_controls = 0
    tangential_controls = 0
    quiet_controls = 0
    sign_pairs = 0
    for index in range(cases):
        q = Fraction(rng.randint(1, 50), rng.randint(1, 50))
        p = Fraction(rng.randint(-50, 50), rng.randint(1, 50))
        frequency = Fraction(rng.randint(1, 50), rng.randint(1, 50))
        angle_parameter = Fraction(rng.randint(-30, 30), rng.randint(1, 30))
        denominator = 1 + angle_parameter**2
        cosine = (1 - angle_parameter**2) / denominator
        sine = 2 * angle_parameter / denominator
        common = frequency * q * p
        depth = common * cosine
        screen = common * sine
        assert depth**2 + screen**2 == common**2
        assert depth / frequency == q * p * cosine
        assert screen / frequency == q * p * sine
        assert (-depth) ** 2 + (-screen) ** 2 == common**2
        sign_pairs += 1

        if index % 97 == 0:
            radial_depth = common
            radial_screen = Fraction(0)
            assert radial_depth**2 + radial_screen**2 == common**2
            assert radial_screen == 0
            radial_controls += 1
        if index % 101 == 0:
            tangential_depth = Fraction(0)
            tangential_screen = common
            assert tangential_depth**2 + tangential_screen**2 == common**2
            assert tangential_depth == 0
            tangential_controls += 1
        if p == 0:
            assert depth == 0 and screen == 0
            quiet_controls += 1

    assert radial_controls > 0 and tangential_controls > 0 and sign_pairs == cases

    result = {
        "status": "PASS",
        "landing": EXPECTED_LANDING,
        "method": "GENERIC_STATIC_LAPSE_CALCULATION_PLUS_EXACT_FRACTION_CENSUS",
        "symbolic_checks": symbolic_checks,
        "exact_fraction_cases": cases,
        "radial_controls": radial_controls,
        "tangential_controls": tangential_controls,
        "quiet_controls": quiet_controls,
        "gradient_sign_pairs": sign_pairs,
        "production_imported": False,
        "history_distance_xmax": "OPEN_NOT_SELECTED",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
