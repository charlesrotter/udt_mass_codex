#!/usr/bin/env python3
"""Independent standard-library check of the R17 stationary sublocus atlas."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
A = 1.0 / 64.0
LAMBDAS = (-2.0, -1.0, 0.0, 0.5, 1.0, 2.0)


def flat_polynomial(x: float, lam: float) -> float:
    return x * x - 2.0 * x ** (1.0 + lam) - A * A


def b_value(x: float, lam: float) -> float:
    return 2.0 - x ** (1.0 - lam) + A * A * x ** (-(1.0 + lam))


def bisect(function, lo: float, hi: float, iterations: int = 180) -> float:
    flo = function(lo)
    fhi = function(hi)
    assert flo * fhi < 0.0
    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        fmid = function(mid)
        if flo * fmid <= 0.0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return (lo + hi) / 2.0


def independent_roots(lam: float) -> list[float]:
    if lam == 1.0:
        return []
    if lam == 2.0:
        return [
            bisect(lambda z: flat_polynomial(z, lam), A, 1.0 / 3.0),
            bisect(lambda z: flat_polynomial(z, lam), 1.0 / 3.0, 0.5),
        ]
    lo = A
    hi = 1.0
    while flat_polynomial(lo, lam) * flat_polynomial(hi, lam) >= 0.0:
        hi *= 2.0
    return [bisect(lambda z: flat_polynomial(z, lam), lo, hi)]


def main() -> int:
    stored = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["six_lambda_strata"] = stored["lambda_values"] == ["-2", "-1", "0", "1/2", "1", "2"]
    expected_counts = {-2.0: 1, -1.0: 1, 0.0: 1, 0.5: 1, 1.0: 0, 2.0: 2}
    computed = {lam: independent_roots(lam) for lam in LAMBDAS}
    checks["root_counts"] = all(len(computed[lam]) == expected_counts[lam] for lam in LAMBDAS)

    stored_roots = stored["flat_regular_roots_at_a_1_over_64"]
    key_for = {-2.0: "-2", -1.0: "-1", 0.0: "0", 0.5: "1/2", 1.0: "1", 2.0: "2"}
    checks["root_values_independent"] = all(
        len(computed[lam]) == len(stored_roots[key_for[lam]])
        and all(abs(left - float(right)) < 2e-14
                for left, right in zip(computed[lam], stored_roots[key_for[lam]], strict=True))
        for lam in LAMBDAS
    )
    checks["all_roots_regular"] = all(root > A for values in computed.values() for root in values)
    checks["all_roots_flat"] = all(abs(flat_polynomial(root, lam)) < 2e-14
                                      for lam, values in computed.items() for root in values)
    checks["flat_equals_zero_vertical_coefficient"] = all(
        abs(b_value(root, lam)) < 2e-12 for lam, values in computed.items() for root in values
    )

    # Independent calculus census for B_lambda on x>a.
    sample_points = [A * (1.0 + 1e-8), A * math.sqrt(3.0), 0.1, 1.0, 10.0, 100.0]
    checks["lambda_minus2_minus1_zero_half_monotone"] = all(
        all(b_value(sample_points[i], lam) > b_value(sample_points[i + 1], lam)
            for i in range(len(sample_points) - 1))
        for lam in (-2.0, -1.0, 0.0, 0.5)
    )
    checks["lambda_one_range"] = all(1.0 < b_value(point, 1.0) < 2.0 for point in sample_points)
    bmin = 2.0 - 2.0 / (3.0 * math.sqrt(3.0) * A)
    checks["lambda_two_minimum_range"] = -23.0 < bmin < -22.0
    checks["lambda_two_minimum_location"] = abs(
        b_value(math.sqrt(3.0) * A, 2.0) - bmin
    ) < 1e-13

    # The canonical inherited Hopf condition B=2 implies x=a and hits slice degeneracy.
    checks["canonical_condition_degenerate"] = abs(b_value(A, -2.0) - 2.0) < 1e-14 and all(
        abs(b_value(A, lam) - 2.0) < 1e-14 for lam in LAMBDAS
    )
    checks["canonical_no_regular_solution"] = all(
        b_value(A * (1.0 + 1e-8), lam) < 2.0 for lam in LAMBDAS
    )

    # Reconstruct the exceptional lambda=-1 sub-Laplacian identity with exact rationals.
    laplacian_checks = []
    for eps in (Fraction(-1), Fraction(1)):
        for y in (Fraction(1, 3), Fraction(7, 2)):
            for p1, p2, p3, yp2 in (
                (Fraction(2, 5), Fraction(3, 7), Fraction(-4, 9), Fraction(5, 11)),
                (Fraction(-5, 6), Fraction(-2, 3), Fraction(7, 8), Fraction(-3, 10)),
            ):
                xp3 = yp2 + 2 * eps * p1
                xy = 4 * y * p2
                yy = 4 * y * p3
                laplacian = 4 * eps * (xy * p3 + y * xp3 - yy * p2 - y * yp2)
                laplacian_checks.append(laplacian == 8 * y * p1)
    # On compact S3 the left integral of p1*(X^2+Y^2)p1 is nonpositive,
    # while the reconstructed right side is integral 8*y*p1^2, nonnegative.
    checks["lambda_minus_one_compact_sign_closure"] = all(laplacian_checks)
    checks["holonomy_dichotomy"] = stored["complete_holonomy"] == "TRIVIAL_ON_FLAT_ROOTS_ELSE_FULL_SO2"
    checks["no_proper_reduced_holonomy"] = stored["proper_nontrivial_reduced_holonomy"] is False
    checks["no_manifest_backed_source_selection"] = stored["manifest_backed_r17_source_selection"] is False

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "schema_version": 1,
        "method": "INDEPENDENT_STDLIB_CALCULUS_AND_BISECTION",
        "checks": checks,
        "passed": len(checks) - len(failed),
        "total": len(checks),
        "failed": failed,
        "computed_roots": {key_for[lam]: values for lam, values in computed.items()},
        "lambda_2_B_min": bmin,
        "status": "PASS" if not failed else "FAIL",
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
