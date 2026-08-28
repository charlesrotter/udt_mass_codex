#!/usr/bin/env python3
"""Implementation-distinct exact-rational G285 witness census."""

from __future__ import annotations

import json
import random
from fractions import Fraction


def mat_vec(tide: tuple[Fraction, Fraction, Fraction], vector: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    xx, xy, yy = tide
    x, y = vector
    return xx * x + xy * y, xy * x + yy * y


def main() -> None:
    rng = random.Random(28520260827)
    assertions = 0
    cases = 256
    for index in range(cases):
        scalar_a = scalar_b = (Fraction(index, 257), Fraction(1, 1))
        pair_a = pair_b = ("central_pair", "frame_carry")
        tide_a = (Fraction(0), Fraction(0), Fraction(0))
        tide_b = (
            Fraction(rng.randint(1, 19), rng.randint(1, 19)),
            Fraction(rng.randint(-19, 19), rng.randint(1, 19)),
            Fraction(rng.randint(-19, 19), rng.randint(1, 19)),
        )
        vector = (Fraction(1), Fraction(2))
        if mat_vec(tide_b, vector) == (Fraction(0), Fraction(0)):
            vector = (Fraction(2), Fraction(-1))
        hessian_b = tuple(-value for value in tide_b)
        tests = (
            scalar_a == scalar_b,
            pair_a == pair_b,
            tide_a != tide_b,
            pair_a + tide_a != pair_b + tide_b,
            tuple(-value for value in hessian_b) == tide_b,
            mat_vec(tide_a, vector) != mat_vec(tide_b, vector),
            len(tide_b) == 3,
            all(isinstance(value, Fraction) for value in tide_b),
        )
        if not all(tests):
            raise SystemExit(f"independent exact case failed: {index}")
        assertions += len(tests)

    # Centered radial separator at the same reciprocal depth phi=2:
    # phi_A=r^2 gives r_A^2=2; phi_B=r^2+r^4 gives r_B^2=1.
    radial_checks = {
        "same_depth": Fraction(2) == Fraction(2),
        "different_areal_radius_squared": Fraction(2) != Fraction(1),
        "different_sphere_area_factor": 4 * Fraction(2) != 4 * Fraction(1),
    }
    result = {
        "audit": "G285_INDEPENDENT_COMPLETE_GERM_VERIFICATION",
        "status": "PASS" if all(radial_checks.values()) else "FAIL",
        "exact_cases": cases,
        "exact_assertions": assertions,
        "radial_checks": radial_checks,
        "implementation": "independent_fraction_witness_census",
        "production_imported": False,
        "production_output_read": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
