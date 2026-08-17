#!/usr/bin/env python3
"""Independent stdlib/Fraction verification for G133; does not import production code."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


Matrix = list[list[F]]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def det2(a: Matrix) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def congruence(j: Matrix, h: Matrix) -> Matrix:
    return matmul(transpose(j), matmul(h, j))


def equal(a: Matrix, b: Matrix) -> bool:
    return a == b


def dot(g: Matrix, u: list[F], v: list[F]) -> F:
    return sum((u[i] * g[i][j] * v[j] for i in range(len(u)) for j in range(len(v))), F(0))


def gram_area(g: Matrix, u: list[F], v: list[F]) -> F:
    return dot(g, u, u) * dot(g, v, v) - dot(g, u, v) ** 2


def scale_matrix(a: Matrix, factor: F) -> Matrix:
    return [[factor * x for x in row] for row in a]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("INDEPENDENT_VERIFICATION.json"))
    args = parser.parse_args()

    K = [[F(0), F(1)], [F(1), F(0)]]
    # Rational reciprocal controls replace exponentials by z and 1/z.
    z1, z2 = F(3, 2), F(5, 3)
    D1 = [[1 / z1, F(0)], [F(0), z1]]
    D2 = [[1 / z2, F(0)], [F(0), z2]]
    D21 = matmul(D2, D1)

    h = [[F(-3, 2), F(1, 3)], [F(1, 3), F(5, 4)]]
    J = [[F(2), F(1)], [F(0), F(1)]]
    h_new = congruence(J, h)

    h_c = [[F(-5, 4), F(1, 5)], [F(1, 5), F(7, 6)]]
    J_ab = [[F(2), F(1)], [F(0), F(1)]]
    J_bc = [[F(1), F(0)], [F(1), F(3)]]
    # Declared directly, not manufactured by multiplying J_bc and J_ab.
    J_ac_direct = [[F(2), F(1)], [F(2), F(4)]]
    J_ac_bad = [[F(2), F(1)], [F(2), F(5)]]
    h_b = congruence(J_bc, h_c)
    h_a_composite = congruence(J_ab, h_b)
    h_a_direct = congruence(J_ac_direct, h_c)
    h_a_bad = congruence(J_ac_bad, h_c)

    J_scale = [[F(2), F(0)], [F(0), F(1)]]
    J_shear = [[F(1), F(1)], [F(0), F(1)]]

    eta = [
        [F(-1), F(0), F(0), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    e0 = [F(1), F(0), F(0), F(0)]
    e1 = [F(0), F(1), F(0), F(0)]
    e2 = [F(0), F(0), F(1), F(0)]
    ruler_sum = [F(0), F(1), F(1), F(0)]
    area01 = gram_area(eta, e0, e1)
    area02 = gram_area(eta, e0, e2)
    area0sum = gram_area(eta, e0, ruler_sum)
    eta_scaled = scale_matrix(eta, F(9))
    area01_scaled = gram_area(eta_scaled, e0, e1)

    h_q = [[F(-7, 5), F(2, 7)], [F(2, 7), F(9, 8)]]
    h_p_recharted = h
    h_q_recharted = congruence(J_scale, h_q)
    density_ratio_squared = det2(h_q) / det2(h)
    density_ratio_squared_recharted = det2(h_q_recharted) / det2(h_p_recharted)

    checks = {
        "rational_D1_preserves_K": equal(congruence(D1, K), K),
        "rational_D2_preserves_K": equal(congruence(D2, K), K),
        "rational_Ds_have_unit_determinant": det2(D1) == 1 and det2(D2) == 1,
        "rational_reciprocal_composition_closes": equal(congruence(D21, K), K),
        "pair_metric_is_lorentzian": det2(h) < 0 and h[0][0] < 0,
        "pair_determinant_weight_two_in_J": det2(h_new) == det2(J) ** 2 * det2(h),
        "direct_triple_jacobian_matches_independent_composite": J_ac_direct == matmul(J_bc, J_ab),
        "direct_triple_metric_matches_independent_composite": h_a_direct == h_a_composite,
        "direct_triple_determinant_weight_closes": det2(h_a_direct) == det2(J_ac_direct) ** 2 * det2(h_c),
        "direct_triple_determinants_multiply": det2(J_ac_direct) == det2(J_bc) * det2(J_ab),
        "corrupted_direct_overlap_is_rejected": (
            J_ac_bad != matmul(J_bc, J_ab) and h_a_bad != h_a_composite
        ),
        "scale_transition_changes_numeric_K": congruence(J_scale, K) != K,
        "scale_transition_gives_two_K": congruence(J_scale, K) == [[F(0), F(2)], [F(2), F(0)]],
        "shear_preserves_determinant_line": det2(J_shear) == 1,
        "shear_does_not_preserve_K": congruence(J_shear, K) != K,
        "K_is_symmetric": transpose(K) == K,
        "K_is_not_alternating": transpose(K) != [[-x for x in row] for row in K],
        "minkowski_gram_area_e0e1": area01 == -1,
        "minkowski_gram_area_e0e2": area02 == -1,
        "minkowski_gram_area_unnormalized_diagonal": area0sum == -2,
        # omega(e0,e1)=omega(e0,e2)=1 forces omega(e0,e1+e2)=2, whose square 4
        # does not equal the metric area magnitude 2 of that unnormalized plane.
        "two_form_linearity_contradicts_third_area": F(2) ** 2 != -area0sum,
        "ambient_area_bilinear_conformal_weight_four": area01_scaled == F(9) ** 2 * area01,
        "ambient_area_norm_conformal_weight_two": -area01_scaled == F(9) ** 2 * (-area01),
        # Rechart only q by determinant 2: the squared density ratio changes by 4.
        "endpoint_density_ratio_needs_matched_trivialization": density_ratio_squared_recharted
        == det2(J_scale) ** 2 * density_ratio_squared,
        "endpoint_density_ratio_really_changes": density_ratio_squared_recharted != density_ratio_squared,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passed": sum(checks.values()),
        "total": len(checks),
        "checks": checks,
        "exact": {
            "det_h": str(det2(h)),
            "det_J": str(det2(J)),
            "det_h_new": str(det2(h_new)),
            "det_J_ab": str(det2(J_ab)),
            "det_J_bc": str(det2(J_bc)),
            "det_J_ac_direct": str(det2(J_ac_direct)),
            "det_J_ac_bad": str(det2(J_ac_bad)),
            "scaled_K": str(congruence(J_scale, K)),
            "sheared_K": str(congruence(J_shear, K)),
            "area01": str(area01),
            "area02": str(area02),
            "area0sum": str(area0sum),
            "area01_scaled": str(area01_scaled),
            "density_ratio_squared": str(density_ratio_squared),
            "density_ratio_squared_recharted": str(density_ratio_squared_recharted),
        },
        "implementation": "stdlib Fraction only; no production-module import",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if result["status"] == "PASS":
        print(f"PASS: {result['passed']}/{result['total']} independent G133 checks")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
