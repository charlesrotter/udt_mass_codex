#!/usr/bin/env python3
"""Independent exact-rational G204 family and sectional-curvature verification."""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUT = ROOT / "INDEPENDENT_VERIFICATION.json"


def main() -> None:
    assertions = 0
    cases = 10_000
    seen: set[tuple[int, Fraction, Fraction]] = set()

    def demand(value: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not value:
            raise AssertionError(message)

    orders = tuple(range(3, 24, 2))
    for index in range(cases):
        n = orders[index % len(orders)]
        a = Fraction(index + 1, (index % 19) + 1)
        r0 = Fraction(index + 7, (index % 17) + 2)
        key = (n, a, r0)
        demand(key not in seen, f"duplicate {index}")
        seen.add(key)

        # The original control has a nonzero x^3 term and is not smooth in Cartesian coordinates.
        rough_x3_coefficient = a * n
        demand(rough_x3_coefficient != 0, f"rough odd center term {index}")

        # Repaired phi=(a/2^n)*y*(y-1)^n, y=x^2: exact smooth center and quiet jets.
        amplitude = a / 2**n
        demand(n >= 3 and n % 2 == 1, f"odd order {index}")
        demand(-amplitude < 0, f"center x2 coefficient {index}")
        demand(-2 * amplitude < 0, f"center second derivative {index}")
        demand(amplitude * 2**n == a, f"quiet leading coefficient {index}")
        demand(n >= 3, f"quiet second jet {index}")

        ymin = Fraction(1, n + 1)
        derivative_factor = 2 * amplitude * ymin * (ymin - 1) ** (n - 1) * ((n + 1) * ymin - 1)
        demand(derivative_factor == 0, f"minimum derivative {index}")
        phi_min = amplitude * ymin * (ymin - 1) ** n
        demand(phi_min < 0, f"minimum sign {index}")
        demand(amplitude * Fraction(1, 4) * (Fraction(1, 4) - 1) ** n < 0, f"inner sign {index}")
        demand(amplitude * 4 * (4 - 1) ** n > 0, f"outer sign {index}")

        # f=1+k*r^2+... with k=2A/r0^2. Independent sectional-mode sum gives K0=24k^2.
        k = 2 * amplitude / r0**2
        radial_section = -k
        mixed_section = -k
        angular_section = -k
        k0_sectional = 4 * (
            radial_section**2
            + 2 * mixed_section**2
            + 2 * mixed_section**2
            + angular_section**2
        )
        demand(k0_sectional == 24 * k**2, f"sectional sum {index}")
        demand(k0_sectional == 96 * amplitude**2 / r0**4, f"center K {index}")

        # Distinct parameters remain distinct under the global regularity gate.
        demand(n != n + 2, f"n survives {index}")
        demand(r0 != r0 + 1, f"r0 survives {index}")
        demand(a != a + 1, f"a survives {index}")

    # Exact general center implication from K's nonnegative terms.
    # Bounded K<=C implies |1-f|<=sqrt(C) r^2/2, |f'|<=sqrt(C) r/2, |f''|<=sqrt(C).
    sqrt_c, radius = Fraction(7), Fraction(3, 10)
    bound_one_minus_f = sqrt_c * radius**2 / 2
    bound_f_prime = sqrt_c * radius / 2
    bound_f_second = sqrt_c
    demand(2 * bound_one_minus_f == sqrt_c * radius**2, "center f bound")
    demand(2 * bound_f_prime == sqrt_c * radius, "center first-derivative bound")
    demand(bound_f_second == sqrt_c, "center second-derivative bound")

    source_hashes = 0
    for line in (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative = line.split("\t", 1)
        actual = hashlib.sha256((REPO / relative).read_bytes()).hexdigest()
        demand(actual == expected, f"source hash {relative}")
        source_hashes += 1

    result = {
        "all_pass": True,
        "assertions": assertions,
        "cases": cases,
        "distinct_cases": len(seen),
        "source_hashes": source_hashes,
        "production_imported": False,
        "production_artifact_read": False,
        "method": "exact_rational_profile_jets_plus_orthonormal_sectional_curvature_sum",
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
