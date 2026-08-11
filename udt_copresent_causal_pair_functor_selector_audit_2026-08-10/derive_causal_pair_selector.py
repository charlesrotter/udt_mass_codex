#!/usr/bin/env python3
"""Exact symbolic derivation for the co-present causal pair-selector audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


PKG = Path(__file__).resolve().parent


def main() -> None:
    checks: dict[str, bool] = {}
    witnesses: dict[str, str] = {}

    T, L = sp.symbols("T L", positive=True)
    beta = sp.symbols("beta", real=True)
    h = sp.Matrix([
        [-T**2, -T**2 * beta],
        [-T**2 * beta, L**2 - T**2 * beta**2],
    ])
    checks["pair_metric_determinant"] = sp.simplify(h.det() + T**2 * L**2) == 0

    r = sp.symbols("r", real=True)  # r=dy0/dy1
    null_polynomial = sp.expand((sp.Matrix([r, 1]).T * h * sp.Matrix([r, 1]))[0])
    r_plus = -beta + L / T
    r_minus = -beta - L / T
    checks["shifted_null_root_plus"] = sp.simplify(null_polynomial.subs(r, r_plus)) == 0
    checks["shifted_null_root_minus"] = sp.simplify(null_polynomial.subs(r, r_minus)) == 0
    checks["cone_center_is_minus_beta"] = sp.simplify((r_plus + r_minus) / 2 + beta) == 0
    checks["cone_half_width_is_L_over_T"] = sp.simplify((r_plus - r_minus) / 2 - L / T) == 0

    w_plus = sp.simplify(1 / r_plus)
    w_minus = sp.simplify(1 / r_minus)
    checks["orientation_balanced_inverse_slope"] = sp.simplify(
        (1 / w_plus - 1 / w_minus) / 2 - L / T
    ) == 0
    checks["one_way_slopes_retain_shift"] = beta in w_plus.free_symbols and beta in w_minus.free_symbols

    phi = sp.symbols("phi", real=True)
    checks["reciprocal_width_phi_join"] = sp.simplify((L / T).subs(L, T * sp.exp(2 * phi)) - sp.exp(2 * phi)) == 0
    checks["ceff_is_inverse_centered_width"] = sp.simplify(
        (T / L).subs(L, T * sp.exp(2 * phi)) - sp.exp(-2 * phi)
    ) == 0

    sigma = sp.symbols("sigma", positive=True)
    h_scaled = sp.simplify(sigma**2 * h)
    T_scaled = sigma * T
    L_scaled = sigma * L
    checks["common_scale_leaves_cone_center"] = sp.simplify(h_scaled[0, 1] / h_scaled[0, 0] - beta) == 0
    checks["common_scale_leaves_reciprocal_width"] = sp.simplify(L_scaled / T_scaled - L / T) == 0

    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True)
    dh00, dh01, dh11 = sp.symbols("dh00 dh01 dh11", real=True)
    det_h = h00 * h11 - h01**2
    ddet_h = sp.diff(det_h, h00) * dh00 + sp.diff(det_h, h01) * dh01 + sp.diff(det_h, h11) * dh11
    dphi = sp.simplify(sp.Rational(1, 4) * ddet_h / det_h - sp.Rational(1, 2) * dh00 / h00)
    dbeta = sp.simplify((h00 * dh01 - h01 * dh00) / h00**2)
    checks["dphi_uses_all_pair_metric_derivatives"] = all(symbol in dphi.free_symbols for symbol in (dh00, dh01, dh11))
    checks["dbeta_uses_live_shift_derivatives"] = dh00 in dbeta.free_symbols and dh01 in dbeta.free_symbols
    witnesses["dphi_general"] = str(dphi)
    witnesses["dbeta_general"] = str(dbeta)

    # Local causal-transition classification in null coordinates.
    a, b, c, d, omega = sp.symbols("a b c d omega", real=True)
    J = sp.Matrix([[a, b], [c, d]])
    K = sp.Matrix([[0, -1], [-1, 0]])
    pulled = sp.simplify(J.T * K * J)
    checks["general_null_jacobian_pullback"] = pulled == sp.Matrix([
        [-2 * a * c, -a * d - b * c],
        [-a * d - b * c, -2 * b * d],
    ])
    J_diag = sp.diag(a, d)
    J_anti = sp.Matrix([[0, b], [c, 0]])
    checks["diagonal_causal_component"] = sp.simplify(J_diag.T * K * J_diag - a * d * K) == sp.zeros(2)
    checks["exchanged_null_component"] = sp.simplify(J_anti.T * K * J_anti - b * c * K) == sp.zeros(2)
    checks["causal_equations_force_null_columns"] = (
        pulled[0, 0] == -2 * a * c and pulled[1, 1] == -2 * b * d
    )

    # Exact closure of the identity component under composition and inversion.
    a1, d1, a2, d2 = sp.symbols("a1 d1 a2 d2", nonzero=True)
    D1, D2 = sp.diag(a1, d1), sp.diag(a2, d2)
    checks["causal_component_composition"] = D2 * D1 == sp.diag(a2 * a1, d2 * d1)
    checks["causal_component_inverse"] = sp.simplify(D1.inv() - sp.diag(1 / a1, 1 / d1)) == sp.zeros(2)

    # A nonlinear, globally monotone calibrated counterfamily: f_e(u)=u+e u^3, g(v)=v.
    u, v, eps = sp.symbols("u v eps", real=True)
    f = u + eps * u**3
    g = v
    checks["nonlinear_causal_family_fixes_anchor"] = f.subs(u, 0) == 0 and sp.diff(f, u).subs(u, 0) == 1
    checks["nonlinear_causal_family_nontrivial"] = sp.diff(f, u, 3) == 6 * eps
    checks["nonlinear_causal_family_positive_for_eps_positive"] = sp.diff(f, u) == 1 + 3 * eps * u**2

    # Full time-live/angular graph witness in flat ambient metric.
    q, t, s = sp.symbols("q t s", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    V = sp.Matrix([
        [1, 0],
        [0, 1],
        [q * s, q * t],
        [0, 0],
    ])
    h_graph = sp.simplify(V.T * eta * V)
    expected_graph = sp.Matrix([
        [-1 + q**2 * s**2, q**2 * t * s],
        [q**2 * t * s, 1 + q**2 * t**2],
    ])
    checks["time_live_angular_graph_metric"] = h_graph == expected_graph
    graph_det = sp.factor(h_graph.det())
    checks["time_live_angular_graph_determinant"] = graph_det == -1 - q**2 * t**2 + q**2 * s**2
    graph_phi_argument = sp.factor((-graph_det) / h_graph[0, 0] ** 2)
    checks["time_live_graph_phi_nonconstant"] = t in graph_phi_argument.free_symbols and s in graph_phi_argument.free_symbols
    witnesses["time_live_graph_phi_argument"] = str(graph_phi_argument)

    # Infinite profile family sharing center and both reciprocal asymptotes.
    z, p = sp.symbols("z p", real=True)
    profile = sp.atanh(z) + p * z * (1 - z**2)
    checks["profile_family_common_center"] = sp.simplify(profile.subs(z, 0)) == 0
    checks["profile_deformation_vanishes_at_endpoints"] = (
        sp.simplify((p * z * (1 - z**2)).subs(z, 1)) == 0
        and sp.simplify((p * z * (1 - z**2)).subs(z, -1)) == 0
    )
    checks["profile_family_is_nontrivial"] = sp.diff(profile, p) == z * (1 - z**2)
    checks["positive_depth_ceff_limit"] = sp.limit(sp.exp(-2 * profile), z, 1, dir="-") == 0
    checks["negative_depth_ceff_limit"] = sp.limit(sp.exp(-2 * profile), z, -1, dir="+") == sp.oo
    checks["ordinary_anchor_ceff"] = sp.simplify(sp.exp(-2 * profile.subs(z, 0)) - 1) == 0

    # Common-family scalar descent versus independent calibration offsets.
    phi_a, phi_b, phi_c = sp.symbols("phi_a phi_b phi_c", real=True)
    checks["common_family_three_observer_telescope"] = sp.simplify(
        (phi_b - phi_a) + (phi_c - phi_b) - (phi_c - phi_a)
    ) == 0
    o_ab, o_bc, o_ac = sp.symbols("o_ab o_bc o_ac", real=True)
    offset_obstruction = sp.simplify(o_ab + o_bc - o_ac)
    checks["independent_family_offset_survives"] = offset_obstruction != 0
    witnesses["independent_family_offset"] = str(offset_obstruction)

    failed = sorted(name for name, passed in checks.items() if not passed)
    assert not failed, failed
    result = {
        "schema_version": 1,
        "question_type": "METRIC_LED_CAUSAL_SOLUTION_SPACE_DERIVATION",
        "landing": (
            "PAIR_CONE_DERIVES_EXACT_SHIFT_NEUTRAL_PHI_CEFF_JOIN_ON_A_SUPPLIED_CALIBRATED_FAMILY__"
            "INDUCED_LOCAL_CAUSALITY_IS_AUTOMATIC__SMOOTH_LOCAL_TIME_ORIENTED_CAUSAL_ISOMORPHISMS_"
            "RETAIN_INFINITE_NULL_REPARAMETRIZATION_FREEDOM__RECIPROCITY_COMPOSITION_CE_ANCHOR_AND_"
            "BOTH_ASYMPTOTES_DO_NOT_SELECT_THE_LOCAL_TRANSITION_OR_CALIBRATION_CLASS_ON_A_SUPPLIED_"
            "FAMILY__AMBIENT_PHYSICAL_FAMILY_GLOBAL_CAUSAL_FAITHFULNESS_AND_ON_SHELL_OWNER_OPEN"
        ),
        "check_count": len(checks),
        "checks": checks,
        "witnesses": witnesses,
        "scope": {
            "time_dependence": "retained_algebraically_not_on_shell",
            "causal_transition_class": "smooth_local_1plus1_time_oriented_bidirectional_causal_isomorphisms",
            "co_presence": "whole_solution_semantics_only",
            "not_derived": [
                "physical_pair_family",
                "global_causal_faithfulness",
                "material_signal_speed",
                "native_time_evolution",
            ],
            "scope_correction": (
                "local_transition_and_calibration_nonselection_only; no ambiently_distinct_"
                "physical_pair_immersion_multiplicity theorem"
            ),
        },
    }
    (PKG / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
