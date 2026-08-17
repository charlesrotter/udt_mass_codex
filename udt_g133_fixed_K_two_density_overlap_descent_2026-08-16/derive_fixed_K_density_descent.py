#!/usr/bin/env python3
"""Exact symbolic derivation for G133 fixed-K density and overlap descent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def area_bilinear(g: sp.Matrix, u: sp.Matrix, v: sp.Matrix, w: sp.Matrix, z: sp.Matrix) -> sp.Expr:
    return sp.expand((u.T * g * w)[0] * (v.T * g * z)[0] - (u.T * g * z)[0] * (v.T * g * w)[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("DERIVATION_RESULT.json"))
    args = parser.parse_args()

    delta, a, b, omega = sp.symbols("delta a b Omega", real=True)
    K = sp.Matrix([[0, 1], [1, 0]])
    D = sp.diag(sp.exp(-delta), sp.exp(delta))
    Da = sp.diag(sp.exp(-a), sp.exp(a))
    Db = sp.diag(sp.exp(-b), sp.exp(b))

    # A full non-diagonal regular Lorentzian pair metric and a positive-determinant recharting.
    h = sp.Matrix([[sp.Rational(-3, 2), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(5, 4)]])
    J = sp.Matrix([[2, 1], [0, 1]])
    h_new = J.T * h * J

    # Genuine three-chart overlap, using the convention h_A=J_AB^T h_B J_AB.
    # The direct A<-C map is specified independently from the A<-B<-C composite.
    # A nearby corrupted direct map is retained as a falsification witness.
    h_c = sp.Matrix([[sp.Rational(-5, 4), sp.Rational(1, 5)], [sp.Rational(1, 5), sp.Rational(7, 6)]])
    x0, x1, z0, z1 = sp.symbols("x0 x1 z0 z1", real=True)
    psi_ab = sp.Matrix([2 * x0 + x1, x1])
    psi_bc = sp.Matrix([z0, z0 + 3 * z1])
    psi_ac_direct = sp.Matrix([2 * x0 + x1, 2 * x0 + 4 * x1])
    psi_ac_composite = psi_bc.subs({z0: psi_ab[0], z1: psi_ab[1]}, simultaneous=True)
    J_ab = psi_ab.jacobian([x0, x1])
    J_bc = psi_bc.jacobian([z0, z1])
    J_ac_direct = psi_ac_direct.jacobian([x0, x1])
    J_ac_bad = sp.Matrix([[2, 1], [2, 5]])
    h_b = J_bc.T * h_c * J_bc
    h_a_composite = J_ab.T * h_b * J_ab
    h_a_direct = J_ac_direct.T * h_c * J_ac_direct
    h_a_bad = J_ac_bad.T * h_c * J_ac_bad

    # Two calibration mismatches: one changes determinant density, one preserves determinant only.
    J_scale = sp.diag(2, 1)
    J_shear = sp.Matrix([[1, 1], [0, 1]])

    # Ambient Lorentz metric and simple bivector tests.
    g = sp.diag(-1, 1, 1, 1)
    e0 = sp.Matrix([1, 0, 0, 0])
    e1 = sp.Matrix([0, 1, 0, 0])
    e2 = sp.Matrix([0, 0, 1, 0])
    r12 = (e1 + e2) / sp.sqrt(2)
    area01 = area_bilinear(g, e0, e1, e0, e1)
    area02 = area_bilinear(g, e0, e2, e0, e2)
    area0r = area_bilinear(g, e0, r12, e0, r12)
    scaled_area0r = area_bilinear(omega**2 * g, e0, r12, e0, r12)

    # If an alternating two-form gave unit oriented area on (e0,e1) and (e0,e2), linearity forces
    # sqrt(2) on the normalized diagonal ruler, while the metric area remains one.
    forced_two_form_value = (sp.Integer(1) + sp.Integer(1)) / sp.sqrt(2)

    det_h = sp.factor(h.det())
    det_h_new = sp.factor(h_new.det())
    det_h_a_composite = sp.factor(h_a_composite.det())
    det_h_a_direct = sp.factor(h_a_direct.det())
    det_h_b = sp.factor(h_b.det())
    det_h_c = sp.factor(h_c.det())

    checks = {
        "D_preserves_fixed_K": sp.simplify(D.T * K * D - K) == sp.zeros(2),
        "D_has_unit_determinant": sp.simplify(D.det() - 1) == 0,
        "D_acts_trivially_on_determinant_line": sp.simplify(D.det()) == 1,
        "K_is_symmetric_not_alternating": K.T == K and K.T != -K,
        "pair_metric_is_regular_lorentzian": det_h < 0 and h[0, 0] < 0,
        "pair_determinant_recharts_with_detJ_squared": sp.simplify(det_h_new - J.det() ** 2 * det_h) == 0,
        "pair_volume_coefficient_recharts_with_abs_detJ": sp.simplify(
            sp.sqrt(-det_h_new) - abs(J.det()) * sp.sqrt(-det_h)
        ) == 0,
        "kappa_coefficient_shifts_by_half_log_detJ": sp.simplify(
            sp.log(-det_h_new) / 4 - sp.log(-det_h) / 4 - sp.log(abs(J.det())) / 2
        ) == 0,
        "triple_overlap_direct_map_matches_composite": sp.simplify(psi_ac_direct - psi_ac_composite) == sp.zeros(2, 1),
        "triple_overlap_direct_jacobian_matches_composite": J_ac_direct == J_bc * J_ab,
        "triple_overlap_direct_metric_matches_composite": sp.simplify(h_a_direct - h_a_composite) == sp.zeros(2),
        "triple_overlap_density_weight_closes": sp.simplify(
            sp.sqrt(-det_h_a_composite) - abs(J_ab.det()) * abs(J_bc.det()) * sp.sqrt(-det_h_c)
        ) == 0,
        "triple_overlap_direct_density_matches_composite": sp.simplify(
            sp.sqrt(-det_h_a_direct) - abs(J_ac_direct.det()) * sp.sqrt(-det_h_c)
        ) == 0,
        "corrupted_direct_overlap_is_rejected": (
            J_ac_bad != J_bc * J_ab
            and sp.simplify(h_a_bad - h_a_composite) != sp.zeros(2)
        ),
        "scale_transition_does_not_preserve_numeric_K": sp.simplify(J_scale.T * K * J_scale - K) != sp.zeros(2),
        "scale_transition_changes_K_by_factor_two": sp.simplify(J_scale.T * K * J_scale - 2 * K) == sp.zeros(2),
        "unit_determinant_shear_preserves_determinant_line": J_shear.det() == 1,
        "unit_determinant_shear_does_not_preserve_K": sp.simplify(J_shear.T * K * J_shear - K) != sp.zeros(2),
        "K_isometries_close_under_composition": sp.simplify((Db * Da).T * K * (Db * Da) - K) == sp.zeros(2),
        "reciprocal_composition_is_additive": sp.simplify(Db * Da - sp.diag(sp.exp(-(a + b)), sp.exp(a + b))) == sp.zeros(2),
        "ambient_area_equals_pair_Gram_determinant_01": area01 == -1,
        "ambient_area_equals_pair_Gram_determinant_02": area02 == -1,
        "ambient_area_is_unit_on_normalized_diagonal_ruler": sp.simplify(area0r + 1) == 0,
        "ambient_area_bilinear_has_conformal_weight_four": sp.simplify(scaled_area0r - omega**4 * area0r) == 0,
        "ambient_area_norm_has_conformal_weight_two": sp.simplify(
            sp.sqrt(-scaled_area0r) - omega**2 * sp.sqrt(-area0r)
        ) == 0,
        "no_single_two_form_matches_three_unit_plane_areas": sp.simplify(forced_two_form_value**2 - 1) != 0,
    }

    # Explicit endpoint retrivialization witness: only q is recharted by det(J)=2.
    h_q = sp.Matrix([[sp.Rational(-7, 5), sp.Rational(2, 7)], [sp.Rational(2, 7), sp.Rational(9, 8)]])
    h_q_recharted = J_scale.T * h_q * J_scale
    density_ratio_squared = sp.factor(h_q.det() / h.det())
    density_ratio_squared_recharted = sp.factor(h_q_recharted.det() / h.det())
    delta_kappa = sp.log(-h_q.det()) / 4 - sp.log(-h.det()) / 4
    delta_kappa_recharted = sp.log(-h_q_recharted.det()) / 4 - sp.log(-h.det()) / 4
    checks.update(
        {
            "endpoint_rechart_scales_squared_density_ratio_by_detJ_squared": sp.simplify(
                density_ratio_squared_recharted - J_scale.det() ** 2 * density_ratio_squared
            ) == 0,
            "endpoint_rechart_shifts_delta_kappa_by_half_log_detJ": sp.simplify(
                delta_kappa_recharted - delta_kappa - sp.log(abs(J_scale.det())) / 2
            ) == 0,
            "endpoint_rechart_really_changes_unmatched_delta_kappa": sp.simplify(
                delta_kappa_recharted - delta_kappa
            ) != 0,
        }
    )

    checks = {name: bool(value) for name, value in checks.items()}
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passed": sum(checks.values()),
        "total": len(checks),
        "checks": checks,
        "exact": {
            "D_transpose_K_D": str(sp.simplify(D.T * K * D)),
            "det_D": str(D.det()),
            "det_h": str(det_h),
            "det_J": str(J.det()),
            "det_h_new": str(det_h_new),
            "kappa_rechart_shift": str(sp.log(abs(J.det())) / 2),
            "J_scale_transpose_K_J_scale": str(J_scale.T * K * J_scale),
            "J_shear_transpose_K_J_shear": str(J_shear.T * K * J_shear),
            "triple_det_J_ab": str(J_ab.det()),
            "triple_det_J_bc": str(J_bc.det()),
            "triple_det_J_ac_direct": str(J_ac_direct.det()),
            "triple_det_J_ac_bad": str(J_ac_bad.det()),
            "density_ratio_squared": str(density_ratio_squared),
            "density_ratio_squared_recharted": str(density_ratio_squared_recharted),
            "delta_kappa_endpoint_rechart_shift": str(sp.simplify(delta_kappa_recharted - delta_kappa)),
            "ambient_area_01": str(area01),
            "ambient_area_0r": str(area0r),
            "forced_two_form_diagonal_value": str(forced_two_form_value),
            "forced_two_form_diagonal_value_squared": str(sp.simplify(forced_two_form_value**2)),
        },
        "landing": (
            "FIXED_K_INTERNAL_UNIMODULAR_DENSITY_DERIVED__"
            "SUPPLIED_PAIR_VOLUME_DENSITY_DESCENDS_ON_GENUINE_COMMON_ATLAS__"
            "KAPPA_IS_A_LOG_DENSITY_COEFFICIENT_REQUIRING_MATCHED_CALIBRATION__"
            "AMBIENT_AREA_BILINEAR_REQUIRES_FULL_g__"
            "NO_FIXED_K_ONLY_QUERY_INDEPENDENT_BASE_TWO_FORM_OR_PHYSICAL_VALUE_LAW"
        ),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if result["status"] == "PASS":
        print(f"PASS: {result['passed']}/{result['total']} exact G133 production checks")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
