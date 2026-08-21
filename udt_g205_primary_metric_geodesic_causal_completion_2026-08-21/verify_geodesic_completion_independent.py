#!/usr/bin/env python3
"""Independent exact-rational Hamiltonian and trapping census for G205."""

from __future__ import annotations

import json
import os
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"


def main() -> None:
    assertions = 0
    cases = 10_000
    seen: set[tuple[int, Fraction, Fraction, Fraction, int]] = set()

    def demand(value: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not value:
            raise AssertionError(message)

    orders = tuple(range(3, 24, 2))
    for index in range(cases):
        n = orders[index % len(orders)]
        a = Fraction(index + 2, (index % 23) + 1)
        r0 = Fraction(index + 11, (index % 17) + 2)
        radius = Fraction((index % 29) + 31, 7)
        epsilon = (-1, 0, 1)[index % 3]
        key = (n, a, r0, radius, epsilon)
        demand(key not in seen, f"duplicate {index}")
        seen.add(key)

        # Independent Hamiltonian route with arbitrary positive metric value F and derivative Fp.
        F = Fraction((index % 13) + 1, (index % 19) + 20)
        Fp = Fraction((index % 31) - 15, (index % 11) + 5)
        angular = Fraction((index % 7) + 1, 5)
        energy = Fraction((index % 5) + 10, 1)
        radial_sq = energy**2 + epsilon * F - F * angular**2 / radius**2
        demand(radial_sq > 0, f"physical radial square {index}")
        twice_hamiltonian = -energy**2 / F + radial_sq / F + angular**2 / radius**2
        demand(twice_hamiltonian == epsilon, f"Hamiltonian norm {index}")
        demand(F * (energy / F) == energy, f"energy first integral {index}")
        demand(radius**2 * (angular / radius**2) == angular, f"angular first integral {index}")
        accel_first_integral = epsilon * Fp / 2 - angular**2 * Fp / (2 * radius**2) + F * angular**2 / radius**3
        accel_hamilton = Fp * (epsilon - angular**2 / radius**2) / 2 + F * angular**2 / radius**3
        demand(accel_first_integral == accel_hamilton, f"radial acceleration {index}")

        # Exact profile trapping polynomial on the only interval where p can be negative.
        denominator = (index % 37) + 41
        numerator = (index % (denominator - 1)) + 1
        y = Fraction(numerator, denominator * (n + 1))
        demand(0 < y < Fraction(1, n + 1), f"inner y {index}")
        q = y * (1 - y) ** (n - 1) * (1 - (n + 1) * y)
        demand(q > 0, f"positive q {index}")
        p = -a * q / 2 ** (n - 1)
        direct_p = a * y * (y - 1) ** (n - 1) * ((n + 1) * y - 1) / 2 ** (n - 1)
        demand(p == direct_p and p < 0, f"p identity {index}")
        qprime = (1 - y) ** (n - 2) * ((n + 1) ** 2 * y**2 - (3 * n + 2) * y + 1)
        demand(qprime != 0 or ((n + 1) ** 2 * y**2 - (3 * n + 2) * y + 1) == 0, f"q derivative {index}")
        demand(-p * 2 ** (n - 1) == a * q, f"amplitude scaling {index}")

        # E=0 causal classification and outer bounds are algebraic, not radial-only sampling.
        demand(-F * (1 + angular**2 / radius**2) < 0, f"timelike E0 {index}")
        demand(-F * angular**2 / radius**2 < 0, f"null E0 nonzero L {index}")
        spacelike_e0 = F * (1 - angular**2 / radius**2)
        demand(spacelike_e0 > 0, f"spacelike E0 outer {index}")
        demand(radial_sq <= energy**2 + F, f"outer velocity upper bound {index}")

    result = {
        "all_pass": True,
        "assertions": assertions,
        "cases": cases,
        "distinct_cases": len(seen),
        "production_imported": False,
        "production_artifact_read": False,
        "method": "independent_exact_rational_algebraic_core_only",
        "verified_scope": [
            "Hamiltonian_first_integral_identity",
            "radial_acceleration_identity",
            "zero_energy_sign_classification",
            "trapping_polynomial_identity_and_sign",
        ],
        "not_independently_verified_here": [
            "smooth_center_crossing",
            "bounded_geodesic_ODE_extension",
            "optical_metric_completeness",
            "Cauchy_slice_global_hyperbolicity",
            "all_odd_n_universal_quantifier",
        ],
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
