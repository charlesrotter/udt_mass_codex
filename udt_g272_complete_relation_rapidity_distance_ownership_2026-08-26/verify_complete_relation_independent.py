#!/usr/bin/env python3
"""Implementation-independent exact-rational and floating checks for G272."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"
LANDING = (
    "COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_TRANSPORTED_RAPIDITY_STATE__"
    "PLANAR_TANH_DELTA_IS_EXACT_STRATUM__SCREEN_STATE_PREVENTS_DELTA_ONLY_COMPLETENESS__"
    "CONVENTIONAL_DISTANCE_SCALE_PROFILE_HISTORY_AND_XMAX_REMAIN_OPEN"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    rng = random.Random(272)
    cases = 24000
    planar_controls = 0
    nonplanar_separators = 0
    negative_depth_controls = 0
    exact_assertions = 0

    for index in range(cases):
        r = Fraction(rng.randint(1, 80), rng.randint(1, 80))
        w_a = Fraction(rng.randint(-30, 30), rng.randint(1, 30))
        w_b = Fraction(rng.randint(-30, 30), rng.randint(1, 30))
        screen2 = w_a**2 + w_b**2

        gamma = (r + 1 / r + r * screen2) / 2
        longitudinal = gamma - 1 / r
        mutual = 1 / gamma
        rho2 = 1 - mutual**2

        assert gamma >= 1
        assert gamma**2 - longitudinal**2 - screen2 == 1
        assert longitudinal**2 / gamma**2 + screen2 / gamma**2 == rho2
        assert mutual**2 + rho2 == 1
        exact_assertions += 4

        reverse_gamma = (1 / r + r + (1 / r) * (r**2 * screen2)) / 2
        assert reverse_gamma == gamma
        exact_assertions += 1

        gamma_float = float(gamma)
        eta = math.acosh(gamma_float)
        rho = math.sqrt(float(rho2))
        assert math.isclose(1 / math.cosh(eta), float(mutual), rel_tol=2e-13, abs_tol=2e-13)
        assert math.isclose(math.tanh(eta), rho, rel_tol=2e-13, abs_tol=2e-13)

        delta = -math.log(float(r))
        assert eta + 2e-13 >= abs(delta)
        if delta < 0:
            assert eta >= 0
            negative_depth_controls += 1

        if index % 89 == 0:
            planar_gamma = (r + 1 / r) / 2
            planar_mutual = 1 / planar_gamma
            signed_chi = (1 - r**2) / (1 + r**2)
            planar_rho2 = 1 - planar_mutual**2
            assert planar_rho2 == signed_chi**2
            assert planar_mutual == 2 * r / (1 + r**2)
            planar_controls += 1
            exact_assertions += 2

        if screen2 > 0:
            planar_gamma = (r + 1 / r) / 2
            assert gamma > planar_gamma
            assert mutual < 1 / planar_gamma
            nonplanar_separators += 1
            exact_assertions += 2

    assert planar_controls > 0
    assert nonplanar_separators > 0
    assert negative_depth_controls > 0

    result = {
        "status": "PASS",
        "landing": LANDING,
        "method": "INDEPENDENT_EXACT_FRACTION_TRANSPORT_DECOMPOSITION_PLUS_FLOAT_RAPIDITY",
        "production_imported": False,
        "cases": cases,
        "exact_assertions": exact_assertions,
        "planar_controls": planar_controls,
        "nonplanar_separators": nonplanar_separators,
        "negative_depth_controls": negative_depth_controls,
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
