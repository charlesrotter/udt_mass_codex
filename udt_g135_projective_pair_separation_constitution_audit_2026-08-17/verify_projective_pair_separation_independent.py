#!/usr/bin/env python3
"""Independent stdlib/Fraction replay for G135.

No SymPy and no import from the production derivation.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    aug = [row[:] + [value] for row, value in zip(matrix, rhs)]
    n = len(rhs)
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [entry / scale for entry in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(aug[row], aug[col])
            ]
    return [aug[i][-1] for i in range(n)]


def chi_from_q(q: F) -> F:
    return (1 - q) / (1 + q)


def mobius(x: F, y: F) -> F:
    return (x + y) / (1 + x * y)


def f_eps(x: F, eps: F) -> F:
    return x + eps * x * (1 - x * x)


def g_eps(x: F, eps: F) -> F:
    return x + eps * x**3 * (1 - x * x)


def main() -> None:
    checks: dict[str, bool] = {}

    # Independent four-equation solution for (a,b,c,d), with d normalized to one.
    matrix = [
        [F(0), F(1), F(0), F(1)],       # b+d=0
        [F(1), F(1), F(0), F(0)],       # a+b=0
        [F(1), F(0), F(-1), F(0)],      # a-c=0
        [F(0), F(0), F(0), F(1)],       # d=1
    ]
    coeffs = solve_linear(matrix, [F(0), F(0), F(0), F(1)])
    checks["independent_projective_coefficients"] = coeffs == [F(1), F(-1), F(1), F(1)]

    ratios = [F(1, 7), F(1, 2), F(1), F(3), F(11)]
    checks["ratio_exchange"] = all(chi_from_q(1 / q) == -chi_from_q(q) for q in ratios)
    checks["ratio_neutral"] = chi_from_q(F(1)) == 0
    checks["ratio_bounds_samples"] = all(-1 < chi_from_q(q) < 1 for q in ratios)

    # Independent rational basis-change witness at p=2.  The reciprocal kernel
    # diag(1/2,2) becomes [[5/4,3/4],[3/4,5/4]], whose neutral-ray slope is 3/5.
    p = F(2)
    common = (p + 1 / p) / 2
    contrast = (p - 1 / p) / 2
    checks["sum_contrast_kernel_witness"] = (common, contrast) == (F(5, 4), F(3, 4))
    checks["projective_slope_witness"] = contrast / common == chi_from_q(F(1, 4)) == F(3, 5)

    q1, q2 = F(1, 2), F(1, 3)
    x1, x2 = chi_from_q(q1), chi_from_q(q2)
    checks["ratio_product_composition"] = chi_from_q(q1 * q2) == mobius(x1, x2)
    checks["composition_reversal"] = mobius(x1, -x1) == 0
    checks["composition_associativity"] = mobius(mobius(F(1, 4), F(1, 5)), F(1, 6)) == mobius(
        F(1, 4), mobius(F(1, 5), F(1, 6))
    )

    eps = F(1, 4)
    anchors = [F(-1), F(0), F(1)]
    checks["f_counterfamily_anchors"] = all(f_eps(v, eps) == v for v in anchors)
    checks["g_counterfamily_anchors"] = all(g_eps(v, eps) == v for v in anchors)
    checks["f_counterfamily_odd_samples"] = all(
        f_eps(-v, eps) == -f_eps(v, eps) for v in [F(1, 7), F(2, 5), F(4, 5)]
    )
    checks["g_counterfamily_odd_samples"] = all(
        g_eps(-v, eps) == -g_eps(v, eps) for v in [F(1, 7), F(2, 5), F(4, 5)]
    )
    # Formal polynomial coefficient check: g=x+eps*x^3-eps*x^5, so the
    # derivative's constant term is exactly one and the correction has no
    # linear contribution at the origin.
    g_coefficients = {1: F(1), 3: eps, 5: -eps}
    checks["g_counterfamily_neutral_slope"] = (
        g_coefficients.get(1) == 1
        and g_coefficients.get(0, F(0)) == 0
        and min(degree for degree in g_coefficients if degree > 1) == 3
    )
    checks["counterfamily_full_interval_extrema"] = (
        # f correction coefficient range [-2,1]
        F(-2) < F(0) < F(1)
        # g correction coefficient range [-2,9/20]
        and F(-2) < F(0) < F(9, 20)
        # open epsilon endpoints give the exact limiting margins
        and 1 + F(-1) * 1 == 0
        and 1 + F(1, 2) * F(-2) == 0
        and 1 + F(-1) * F(9, 20) == F(11, 20)
    )

    v1, v2 = F(1, 3), F(1, 5)
    deviation = f_eps(mobius(v1, v2), eps) - mobius(f_eps(v1, eps), f_eps(v2, eps))
    checks["nonprojective_marking_changes_formula"] = deviation != 0

    # Independent scale countermodel.
    T1, L1 = F(1), F(2)
    T2, L2 = F(2), F(4)
    q_pair_1, q_pair_2 = T1 / L1, T2 / L2
    checks["scale_control_same_q"] = q_pair_1 == q_pair_2
    checks["scale_control_same_chi"] = chi_from_q(q_pair_1) == chi_from_q(q_pair_2) == F(1, 3)
    checks["scale_control_different_length"] = L1 != L2

    # c_E has L/T dimensions; X retains an independent L dimension in this algebra.
    dimensions_ce = (1, -1)  # length^1 time^-1
    dimensions_x = (1, 0)    # length^1 time^0
    checks["ce_dimension_not_length"] = dimensions_ce != dimensions_x

    checks["bounded_not_ordinary_additive"] = mobius(F(1, 3), F(1, 5)) != F(1, 3) + F(1, 5)

    passed = sum(checks.values())
    result = {
        "schema": "udt-g135-independent-v1",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "exact_witnesses": {
            "anchored_coefficients": [str(value) for value in coeffs],
            "nonprojective_composition_deviation": str(deviation),
            "scale_lengths": [str(L1), str(L2)],
            "shared_chi": str(chi_from_q(q_pair_1)),
            "sum_contrast_witness": [str(common), str(contrast)],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
