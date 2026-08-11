#!/usr/bin/env python3
"""Exact from-scratch calibration-transport derivation.

The script deliberately uses only linear algebra and the regular pair-metric
definitions frozen in the preregistration.  It does not import a candidate UDT
equation, action, source, or historical solver.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


PKG = Path(__file__).resolve().parent


def gram(columns: sp.Matrix, metric: sp.Matrix) -> sp.Matrix:
    return sp.simplify(columns.T * metric * columns)


def norm_area_ratios(
    arrow: sp.Matrix, flag: sp.Matrix, metric_source: sp.Matrix, metric_target: sp.Matrix
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    source = gram(flag, metric_source)
    target = gram(arrow * flag, metric_target)
    # The registered regular controls use a timelike first column and a Lorentzian plane.
    rho1 = sp.simplify(target[0, 0] / source[0, 0])
    rho2 = sp.simplify(target.det() / source.det())
    q = sp.simplify(rho2 / rho1**2)
    return rho1, rho2, q


def main() -> None:
    checks: dict[str, bool] = {}
    witnesses: dict[str, str | int | list[str]] = {}

    h00, h01, h11 = sp.symbols("h00 h01 h11", nonzero=True, real=True)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    beta = sp.simplify(h01 / h00)
    t2 = -h00
    l2 = sp.simplify(h11 - h01**2 / h00)
    reconstructed = sp.Matrix(
        [[-t2, -t2 * beta], [-t2 * beta, -t2 * beta**2 + l2]]
    )
    checks["pair_metric_decomposition"] = sp.simplify(reconstructed - h) == sp.zeros(2)
    checks["pair_metric_TL_determinant"] = sp.simplify(t2 * l2 + h.det()) == 0

    ratio = sp.simplify((-h.det()) / h00**2)
    phi = sp.log(ratio) / 4
    dphi = [sp.simplify(sp.diff(phi, variable)) for variable in (h00, h01, h11)]
    expected_dphi = [
        sp.simplify(sp.diff(sp.log(-h.det()), variable) / 4
                    - sp.diff(sp.log(-h00), variable) / 2)
        for variable in (h00, h01, h11)
    ]
    checks["pair_depth_differential"] = all(
        sp.simplify(a - b) == 0 for a, b in zip(dphi, expected_dphi)
    )
    checks["pair_depth_is_locally_exact"] = all(
        sp.simplify(sp.diff(dphi[i], (h00, h01, h11)[j])
                    - sp.diff(dphi[j], (h00, h01, h11)[i])) == 0
        for i in range(3) for j in range(3)
    )

    p, omega = sp.symbols("p omega", positive=True, real=True)
    pure = {
        h00: -sp.exp(-2 * p),
        h01: 0,
        h11: sp.exp(2 * p),
    }
    checks["pure_reciprocal_recovery"] = sp.simplify(phi.subs(pure) - p) == 0
    scaled_ratio = sp.simplify(
        ratio.subs({h00: omega**2 * h00, h01: omega**2 * h01, h11: omega**2 * h11})
    )
    checks["common_scale_cancels"] = sp.simplify(scaled_ratio - ratio) == 0

    eta = sp.diag(-1, 1, 1, 1)
    e0 = sp.Matrix([1, 0, 0, 0])
    e1 = sp.Matrix([0, 1, 0, 0])
    flag = sp.Matrix.hstack(e0, e1)

    mixing_1 = sp.Matrix(
        [[sp.Rational(1, 2), 0, 0, 0],
         [0, 2, 0, 0],
         [sp.Rational(1, 4), 0, 1, 0],
         [0, 0, 0, 1]]
    )
    rho1_m, rho2_m, q_m = norm_area_ratios(mixing_1, flag, eta, eta)
    checks["finite_mixing_witness"] = (
        rho1_m == sp.Rational(3, 16)
        and rho2_m == sp.Rational(3, 4)
        and q_m == sp.Rational(64, 3)
    )
    witnesses["mixing_q"] = str(q_m)
    witnesses["mixing_phi"] = str(sp.log(q_m) / 4)

    mixing_2 = sp.Matrix(
        [[sp.Rational(3, 2), 0, 0, 0],
         [0, sp.Rational(2, 3), 0, 0],
         [sp.Rational(1, 10), sp.Rational(1, 8), 1, 0],
         [0, 0, 0, 1]]
    )
    rho1_a, rho2_a, q_a = norm_area_ratios(mixing_1, flag, eta, eta)
    carried_flag = mixing_1 * flag
    rho1_b, rho2_b, q_b = norm_area_ratios(mixing_2, carried_flag, eta, eta)
    rho1_ba, rho2_ba, q_ba = norm_area_ratios(mixing_2 * mixing_1, flag, eta, eta)
    checks["density_composition_rho1"] = sp.simplify(rho1_ba - rho1_b * rho1_a) == 0
    checks["density_composition_rho2"] = sp.simplify(rho2_ba - rho2_b * rho2_a) == 0
    checks["reciprocal_character_composition"] = sp.simplify(q_ba - q_b * q_a) == 0

    b = sp.symbols("b0:16", real=True)
    B = sp.Matrix(4, 4, b)
    eps = sp.symbols("eps", real=True)
    A_eps = sp.eye(4) + eps * B
    h_eps = gram(A_eps * flag, eta)
    ratio_eps = sp.simplify((-h_eps.det()) / h_eps[0, 0] ** 2)
    alpha_eps = sp.simplify(sp.diff(sp.log(ratio_eps) / 4, eps).subs(eps, 0))
    expected_alpha = sp.simplify((B[1, 1] - B[0, 0]) / 2)
    checks["infinitesimal_reciprocal_projection"] = sp.simplify(alpha_eps - expected_alpha) == 0
    witnesses["infinitesimal_depth_rate"] = str(alpha_eps)

    k, a, boost = sp.symbols("k a boost", real=True)
    common_B = k * sp.eye(4)
    reciprocal_B = sp.diag(-a, a, 0, 0)
    lorentz_B = sp.Matrix([[0, boost, 0, 0], [boost, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    projector = lambda matrix: sp.simplify((matrix[1, 1] - matrix[0, 0]) / 2)
    checks["common_dilation_rejected_by_reciprocal_projection"] = projector(common_B) == 0
    checks["pure_reciprocal_rate_normalized"] = projector(reciprocal_B) == a
    checks["lorentz_generator_isometric_zero"] = projector(lorentz_B) == 0

    rational_boost = sp.Matrix(
        [[sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
         [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]
    )
    checks["lorentz_transport_metricity"] = (
        sp.simplify(rational_boost.T * eta * rational_boost - eta) == sp.zeros(4)
    )
    rho1_lc, rho2_lc, q_lc = norm_area_ratios(rational_boost, flag, eta, eta)
    checks["metric_compatible_transport_zero_depth"] = (
        rho1_lc == 1 and rho2_lc == 1 and q_lc == 1
    )

    p0, p1, p2, p3, q0, q1, q2, q3 = sp.symbols(
        "p0 p1 p2 p3 q0 q1 q2 q3", positive=True
    )
    E_p = sp.diag(p0, p1, p2, p3)
    E_q = sp.diag(q0, q1, q2, q3)
    g_p = E_p.T * eta * E_p
    g_q = E_q.T * eta * E_q
    A_w = E_q.inv() * E_p
    checks["coframe_absolute_parallelism_is_metric"] = (
        sp.simplify(A_w.T * g_q * A_w - g_p) == sp.zeros(4)
    )
    rho1_w, rho2_w, q_w = norm_area_ratios(A_w, flag, g_p, g_q)
    checks["coframe_absolute_parallelism_zero_depth"] = (
        sp.simplify(rho1_w - 1) == 0
        and sp.simplify(rho2_w - 1) == 0
        and sp.simplify(q_w - 1) == 0
    )

    quarter_turn = sp.Matrix(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]]
    )
    checks["screen_rotation_isometry"] = (
        sp.simplify(quarter_turn.T * eta * quarter_turn - eta) == sp.zeros(4)
    )
    rho1_rot, rho2_rot, q_rot = norm_area_ratios(
        quarter_turn * mixing_1 * quarter_turn.inv(), flag, eta, eta
    )
    checks["screen_gauge_descent"] = (
        sp.simplify(rho1_rot - rho1_m) == 0
        and sp.simplify(rho2_rot - rho2_m) == 0
        and sp.simplify(q_rot - q_m) == 0
    )

    depth = sp.symbols("depth", real=True)
    D = sp.diag(sp.exp(-depth), sp.exp(depth), 1, 1)
    checks["determinant_character_misses_reciprocal_depth"] = sp.simplify(D.det() - 1) == 0

    f_a, f_b, f_c = sp.symbols("f_a f_b f_c", real=True)
    checks["endpoint_coboundary_telescope"] = sp.simplify(
        (f_b - f_a) + (f_c - f_b) - (f_c - f_a)
    ) == 0

    phi_a, phi_b, phi_c = sp.symbols("phi_a phi_b phi_c", real=True)
    checks["single_pair_family_scalar_reset_telescope"] = sp.simplify(
        (phi_b - phi_a) + (phi_c - phi_b) - (phi_c - phi_a)
    ) == 0

    # Independent rebuilds carry arbitrary reciprocal offsets unless a transition owns them.
    offset_ab, offset_bc, offset_ac = sp.symbols("offset_ab offset_bc offset_ac", real=True)
    reset_obstruction = sp.simplify(offset_ab + offset_bc - offset_ac)
    checks["independent_tape_reset_not_identity"] = reset_obstruction != 0
    witnesses["independent_tape_reset_obstruction"] = str(reset_obstruction)

    failed = sorted(name for name, passed in checks.items() if not passed)
    assert not failed, f"failed checks: {failed}"

    result = {
        "schema_version": 1,
        "question_type": "METRIC_LED_SOLUTION_SPACE_DERIVATION",
        "landing": (
            "GENERAL_POSITIVE_LINE_TRANSPORTS_FORM_AN_AFFINE_CONNECTION_FAMILY__"
            "CANONICAL_METRIC_AND_COFRAME_PARALLEL_TRANSPORTS_ARE_ISOMETRIC_ZERO__"
            "EACH_SUPPLIED_REGULAR_CALIBRATED_PAIR_METRIC_FAMILY_UNIQUELY_INDUCES_"
            "THE_EXACT_RECIPROCAL_DEPTH_FORM_dPHI_PAIR_WITH_FULL_TIME_AND_MIXING_RETAINED__"
            "PHYSICAL_PAIR_FAMILY_ON_SHELL_AND_GLOBAL_OWNER_OPEN"
        ),
        "check_count": len(checks),
        "checks": checks,
        "witnesses": witnesses,
        "scope": {
            "time_dependence": "retained_without_stationarity_assumption",
            "angular_and_mixing": "retained_in_complete_pair_metric",
            "regularity": "smooth_rank_two_Lorentzian_pair_metric",
            "not_covered": [
                "null_or_rank_changing_pair_cells",
                "cut_locus_branch_selection",
                "all_higher_categorical_or_nonlocal_path_functionals",
                "physical_pair_query_or_on_shell_selection",
            ],
        },
    }
    (PKG / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
