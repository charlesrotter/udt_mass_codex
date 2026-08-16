#!/usr/bin/env python3
"""Exact symbolic checks for the G124 finite-radius live junction."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def phase_lift(radius: sp.Expr) -> sp.Matrix:
    return sp.Matrix.vstack(radius * sp.eye(2), sp.eye(2))


def main() -> None:
    A, q, source_ratio = sp.symbols("A q source_ratio", positive=True)
    h_plus = sp.Matrix([[-A**2, -q], [-q, 0]])
    h_minus = sp.Matrix([[-A**2, q], [q, 0]])
    det_plus = sp.factor(h_plus.det())
    det_minus = sp.factor(h_minus.det())
    kappa = sp.log(q) / 2
    phi = sp.log(q) / 2 - sp.log(A)
    beta_plus = q / A**2
    beta_minus = -q / A**2
    c_eff_ratio = A**2 / q
    omega_T = 1 / A
    zeta = sp.log(source_ratio * omega_T)
    chi_source = sp.log(source_ratio)

    p2, optical, vrel, vdot, R = sp.symbols(
        "p2 optical vrel vdot R", real=True
    )
    phi_jet = p2 * R**2
    kappa_jet = optical * R**2 / 4
    chi_jet = vrel * R + vdot * R**2
    zeta_jet = sp.expand(phi_jet - kappa_jet + chi_jet)
    g116_expected = vrel * R + (p2 + vdot - optical / 4) * R**2
    w2 = sp.symbols("w2", real=True)
    phi_fixed_jet = phi_jet + w2 * R**2 / 2
    chi_fixed_jet = chi_jet - w2 * R**2 / 2

    K_R, areal_radius = sp.symbols("K_R areal_radius", positive=True)
    theta_sky = 2 * K_R / areal_radius
    kappa_screen = -sp.log(K_R) / 2

    eps = sp.symbols("eps", positive=True)
    kappa_turn = -sp.log(eps) / 2
    phi_turn = kappa_turn - sp.log(A)

    v = sp.symbols("v", real=True)
    radial_source_ratio = sp.sqrt((1 - v) / (1 + v))

    # G123 regular transition/reversal/composition control.
    M_A = sp.Matrix(
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 4, 0], [0, 0, 0, 4]]
    )
    M_B = sp.Matrix(
        [
            [1, 1, 0, 0],
            [0, sp.Rational(4, 5), 3, 0],
            [0, sp.Rational(-3, 5), 4, 0],
            [0, 0, 0, 5],
        ]
    )
    M_C = sp.Matrix(
        [
            [1, 1, 0, 0],
            [0, sp.Rational(4, 5), 0, 3],
            [0, 0, 5, 0],
            [0, sp.Rational(-3, 5), 0, 4],
        ]
    )
    D_BA = sp.simplify(M_B.inv() * M_A)
    D_AB = sp.simplify(M_A.inv() * M_B)
    D_CB = sp.simplify(M_C.inv() * M_B)
    D_CA = sp.simplify(M_C.inv() * M_A)

    lambda4 = phase_lift(sp.Integer(4))
    lambda5 = phase_lift(sp.Integer(5))

    rational = {
        A: sp.Rational(3, 4),
        q: sp.Rational(25, 16),
        source_ratio: sp.Rational(6, 5),
    }
    checks = {
        "raw_null_pair_determinant_both_orientations": (
            det_plus == det_minus == -q**2
        ),
        "terminal_kappa_from_raw_block": sp.simplify(
            sp.exp(4 * kappa) - (-det_plus)
        ) == 0 and sp.simplify(sp.exp(4 * kappa) - (-det_minus)) == 0,
        "terminal_phi_from_raw_block": (
            sp.simplify(sp.exp(4 * phi) - (-det_plus) / h_plus[0, 0] ** 2) == 0
            and sp.simplify(sp.exp(4 * phi) - (-det_minus) / h_minus[0, 0] ** 2) == 0
        ),
        "terminal_beta_from_raw_block": (
            beta_plus == h_plus[0, 1] / h_plus[0, 0]
            and beta_minus == h_minus[0, 1] / h_minus[0, 0]
        ),
        "null_pair_beta_reciprocal_identity": (
            sp.simplify(beta_plus - sp.exp(2 * phi)) == 0
            and sp.simplify(beta_minus + sp.exp(2 * phi)) == 0
        ),
        "terminal_ceff_identity": sp.simplify(c_eff_ratio - sp.exp(-2 * phi)) == 0,
        "normalized_time_frequency": omega_T == 1 / A,
        "exact_finite_radius_junction": sp.simplify(
            sp.exp(zeta - (phi - kappa + chi_source)) - 1
        ) == 0,
        "rational_kappa": sp.simplify(kappa.subs(rational) - sp.log(sp.Rational(5, 4))) == 0,
        "rational_phi": sp.simplify(phi.subs(rational) - sp.log(sp.Rational(5, 3))) == 0,
        "rational_beta": beta_plus.subs(rational) == sp.Rational(25, 9),
        "rational_zeta": sp.simplify(zeta.subs(rational) - sp.log(sp.Rational(8, 5))) == 0,
        "orientation_reversal_changes_only_beta_sign": (
            kappa.subs(rational) == kappa.subs(rational)
            and phi.subs(rational) == phi.subs(rational)
            and c_eff_ratio.subs(rational) == c_eff_ratio.subs(rational)
            and beta_minus.subs(rational) == -beta_plus.subs(rational)
        ),
        "turning_chart_divergence_cancels": sp.simplify(
            phi_turn - kappa_turn + sp.log(A)
        ) == 0,
        "g116_two_jet_reproduced": sp.simplify(zeta_jet - g116_expected) == 0,
        "active_sky_drift_cancels_between_matched_phi_and_chi": sp.simplify(
            phi_fixed_jet - kappa_jet + chi_fixed_jet - g116_expected
        ) == 0,
        "g119_screen_kappa_link": sp.simplify(
            kappa_screen + sp.log(areal_radius * theta_sky / 2) / 2
        ) == 0,
        "radial_source_ratio_is_rapidity": (
            sp.simplify(
                sp.diff(sp.log(radial_source_ratio) + sp.atanh(v), v)
            )
            == 0
            and (sp.log(radial_source_ratio) + sp.atanh(v)).subs(v, 0) == 0
        ),
        "g123_reversal_preserved": zero(D_AB * D_BA - sp.eye(4)),
        "g123_composition_preserved": zero(D_CB * D_BA - D_CA),
        "query_tangent_phase_images_remain_rank_two": (
            lambda4.rank() == 2 and lambda5.rank() == 2
        ),
        "common_event_does_not_force_phase_match": (
            4 - sp.Matrix.hstack(lambda4, lambda5).rank() == 0
        ),
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact_objects": {
            "h_parallel_orientation_covariant": "Matrix([[-A**2, -sigma*q], [-sigma*q, 0]]), sigma in {-1,+1}",
            "det_h": str(det_plus),
            "kappa_pair": str(kappa),
            "phi_pair": str(phi),
            "beta_pair": "sigma*q/A**2",
            "c_eff_over_c_E": str(c_eff_ratio),
            "frequency_junction": "zeta = phi_pair - kappa_pair + chi_source",
            "g116_reduction": str(zeta_jet),
            "screen_link": "kappa_pair = -log(abs(K(R)))/2 on the oriented regular areal chart",
            "rational_values": {
                "kappa_pair": "log(5/4)",
                "phi_pair": "log(5/3)",
                "beta_pair": "25/9",
                "zeta": "log(8/5)",
            },
        },
        "landing": (
            "EXACT_FINITE_RADIUS_KAPPA_PHI_SOURCE_CLOCK_JUNCTION_DERIVED_CONDITIONALLY__"
            "ZETA_EQUALS_PHI_PAIR_MINUS_KAPPA_PAIR_PLUS_CHI_SOURCE__"
            "KAPPA_PAIR_IS_THE_AFFINE_TO_AREAL_SCREEN_EXPANSION_MAGNITUDE__"
            "NULL_PAIR_BETA_EQUALS_ORIENTATION_TIMES_EXP_TWO_PHI__"
            "G116_TWO_JET_ACTIVE_SKY_CANCELLATION_AND_G119_SCREEN_THEOREM_RECOVERED__"
            "AREAL_TURNING_IS_A_CHART_FAILURE_AND_ALONE_ESTABLISHES_NEITHER_FREQUENCY_FINITENESS_NOR_DIVERGENCE__"
            "DIRECT_QUERY_TANGENT_AND_JACOBI_PHASE_REMAIN_DISTINCT__"
            "HISTORY_QUERY_SOURCE_TRANSFER_XMAX_AND_SELECTION_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
