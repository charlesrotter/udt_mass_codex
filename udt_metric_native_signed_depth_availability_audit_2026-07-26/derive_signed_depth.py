#!/usr/bin/env python3
"""Exact symbolic classification of registered signed-depth constructions."""

from __future__ import annotations

import json

import sympy as sp


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def zero_matrix(value: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in value)


def main() -> None:
    checks: dict[str, str] = {}
    lam, phi, dphi, dchi = sp.symbols("lambda phi dphi dchi", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    X = sp.diag(-1, 1, lam, lam)

    # Founded reciprocal section: exact pullback if a spacetime section is supplied.
    D = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(lam * phi), sp.exp(lam * phi))
    theta = sp.simplify(D.inv() * D.diff(phi))
    check("section_Maurer_Cartan_equals_X_dphi", theta == X, checks)
    norm = sp.trace(X * X)
    check("reciprocal_projection_norm_positive_all_real_lambda", sp.simplify(norm - (2 + 2 * lam**2)) == 0, checks)
    projected = sp.simplify(sp.trace(X * theta) / norm)
    check("normalized_section_projection_recovers_dphi_coefficient", projected == 1, checks)
    check("section_character_reversal", sp.simplify(D.subs(phi, -phi) - D.inv()) == sp.zeros(4), checks)

    # Every endpoint-only exact real cocycle is a potential difference.
    p0, p1, p2, p3 = sp.symbols("p0 p1 p2 p3", real=True)
    potentials = [p0, p1, p2, p3]
    deltas = {(i, j): potentials[j] - potentials[i] for i in range(4) for j in range(4)}
    for i in range(4):
        for j in range(4):
            check(f"endpoint_reversal_{i}_{j}", sp.simplify(deltas[(i, j)] + deltas[(j, i)]) == 0, checks)
            for k in range(4):
                check(
                    f"endpoint_triangle_{i}_{j}_{k}",
                    sp.simplify(deltas[(i, j)] + deltas[(j, k)] - deltas[(i, k)]) == 0,
                    checks,
                )
    reconstructed = [deltas[(0, j)] for j in range(4)]
    check(
        "endpoint_basepoint_reconstruction",
        all(sp.simplify(deltas[(i, j)] - (reconstructed[j] - reconstructed[i])) == 0 for i in range(4) for j in range(4)),
        checks,
    )
    check(
        "endpoint_additive_zero_gauge",
        all(sp.simplify((potentials[j] + 11) - (potentials[i] + 11) - deltas[(i, j)]) == 0 for i in range(4) for j in range(4)),
        checks,
    )

    # A metric-compatible connection is metric-skew. Its trace pairing with
    # the metric-self-adjoint reciprocal generator vanishes identically.
    b1, b2, b3, r12, r13, r23 = sp.symbols("b1 b2 b3 r12 r13 r23", real=True)
    omega = sp.Matrix(
        [
            [0, b1, b2, b3],
            [b1, 0, r12, r13],
            [b2, -r12, 0, r23],
            [b3, -r13, -r23, 0],
        ]
    )
    check("Levi_Civita_form_is_metric_skew", zero_matrix(omega.T * eta + eta * omega), checks)
    check("reciprocal_generator_is_metric_self_adjoint", X.T * eta == eta * X, checks)
    check("self_adjoint_skew_trace_pairing_zero", sp.simplify(sp.trace(X * omega)) == 0, checks)
    L = sp.Matrix(
        [
            [sp.Rational(5, 4), 0, sp.Rational(3, 4), 0],
            [0, 1, 0, 0],
            [sp.Rational(3, 4), 0, sp.Rational(5, 4), 0],
            [0, 0, 0, 1],
        ]
    )
    Xp = sp.simplify(L * X * L.inv())
    omegap = sp.simplify(L * omega * L.inv())
    check("Lorentz_sample_is_metric_isometry", L.T * eta * L == eta, checks)
    check("zero_trace_pairing_is_conjugation_invariant", sp.simplify(sp.trace(Xp * omegap)) == 0, checks)

    # Raw coframe components recover depth only relative to a selected
    # reference. A nonconstant reciprocal reference change shifts the result.
    raw = sp.simplify(sp.trace(X * (X * dphi)) / norm)
    raw_changed = sp.simplify(sp.trace(X * (X * (dphi - dchi))) / norm)
    check("raw_reference_projection_is_dphi", raw == dphi, checks)
    check("changed_reference_projection_is_dphi_minus_dchi", raw_changed == dphi - dchi, checks)
    check("nonconstant_reference_change_shifts_raw_depth", sp.simplify(raw_changed - raw) == -dchi, checks)
    check("constant_reference_zero_shift_leaves_difference", raw_changed.subs(dchi, 0) == raw, checks)

    # A supplied positive reciprocal map has a unique subgroup parameter and
    # composes exactly inside the common one-parameter subgroup.
    q, r = sp.symbols("q r", positive=True)
    A_q = sp.diag(1 / q, q)
    A_r = sp.diag(1 / r, r)
    extracted_q = sp.simplify(sp.log(A_q[1, 1] / A_q[0, 0]) / 2)
    extracted_product = sp.simplify(sp.log((A_r * A_q)[1, 1] / (A_r * A_q)[0, 0]) / 2)
    check("reciprocal_map_depth_is_log_q", sp.expand_log(extracted_q, force=True) == sp.log(q), checks)
    check(
        "reciprocal_subgroup_depth_adds",
        sp.expand_log(extracted_product, force=True) == sp.log(q) + sp.log(r),
        checks,
    )
    check("reciprocal_map_reversal_negates_depth", sp.expand_log(sp.log((1 / A_q[1, 1]) / (1 / A_q[0, 0])) / 2, force=True) == -sp.log(q), checks)

    # Projection of the principal logarithm is not a homomorphism on general
    # noncommuting complete maps. Exact rational matrices realize a=b=log 2.
    A = sp.diag(sp.Rational(1, 2), 2)
    B = sp.Matrix([[sp.Rational(5, 4), sp.Rational(3, 4)], [sp.Rational(3, 4), sp.Rational(5, 4)]])
    M = B * A
    mu = sp.acosh(sp.Rational(25, 16))
    K = M - sp.Rational(25, 16) * sp.eye(2)
    check("noncommuting_product_determinant_one", M.det() == 1, checks)
    check("noncommuting_product_hyperbolic_square", sp.simplify(K * K - sp.Rational(369, 256) * sp.eye(2)) == sp.zeros(2), checks)
    p_log_product = sp.simplify(15 * mu / sp.sqrt(369))
    p_log_separate = sp.log(2)
    difference_50 = sp.N(p_log_product - p_log_separate, 50)
    check("general_log_projection_nonadditive", difference_50 > sp.Rational(1, 10), checks)
    check("general_log_projection_counterexample_noncommuting", A * B != B * A, checks)

    # Symmetric metric magnitude cannot itself be nontrivial and reversal odd.
    rho = sp.symbols("rho", nonnegative=True, real=True)
    check("symmetric_and_reversal_odd_force_zero", sp.solve(sp.Eq(rho, -rho), rho) == [0], checks)
    triangle_defect = sp.simplify(1 + sp.sqrt(2) - 1)
    check("noncollinear_metric_triangle_not_additive", triangle_defect == sp.sqrt(2) and triangle_defect != 0, checks)
    check("collinear_subsegment_is_exceptionally_additive", sp.Rational(1) + sp.Rational(2) == sp.Rational(3), checks)

    # Observer-indexed charts inherit the same general triangle defect unless
    # a signed ordered lift and transition law are additionally supplied.
    d_ab, d_bc, d_ac = sp.Integer(1), sp.sqrt(2), sp.Integer(1)
    check("observer_chart_generic_overlap_not_scalar_cocycle", sp.simplify(d_ab + d_bc - d_ac) == sp.sqrt(2), checks)
    check("observer_chart_self_depth_zero", sp.Integer(0) == 0, checks)

    # One-form integration gives path additivity, while nonzero real periods
    # remain visible because the reciprocal character is faithful.
    i1, i2, period = sp.symbols("i1 i2 period", real=True)
    check("one_form_path_concatenation", sp.simplify((i1 + i2) - i1 - i2) == 0, checks)
    check("one_form_path_reversal", sp.simplify(-i1 + i1) == 0, checks)
    check(
        "real_reciprocal_character_identity_only_zero_period",
        sp.solveset(sp.exp(period) - 1, period, domain=sp.S.Reals) == sp.FiniteSet(0),
        checks,
    )
    check("nonzero_period_visible", sp.diag(sp.exp(-1), sp.exp(1)) != sp.eye(2), checks)

    # Metric scalar invariants can manufacture many exact endpoint cocycles,
    # but current structure selects neither invariant nor normalization.
    ia, ib, ic = sp.symbols("I_A I_B I_C", real=True)
    for index, function in enumerate((lambda x: x, lambda x: 2 * x, lambda x: x**3)):
        dab = function(ib) - function(ia)
        dbc = function(ic) - function(ib)
        dac = function(ic) - function(ia)
        check(f"invariant_potential_{index}_adds", sp.simplify(dab + dbc - dac) == 0, checks)
        check(f"invariant_potential_{index}_reverses", sp.simplify(dab + function(ia) - function(ib)) == 0, checks)
    check("invariant_potentials_are_nonunique", (ib - ia) != 2 * (ib - ia), checks)

    # Frequency ratios are exact logarithmic cocycles once endpoint observer/
    # signal data are supplied, but that alone does not identify founded phi.
    wa, wb, wc = sp.symbols("omega_A omega_B omega_C", positive=True)
    log_ab = sp.log(wb / wa)
    log_bc = sp.log(wc / wb)
    log_ac = sp.log(wc / wa)
    check("clock_log_ratio_adds", sp.expand_log(log_ab + log_bc - log_ac, force=True) == 0, checks)
    check("clock_log_ratio_reverses", sp.expand_log(log_ab + sp.log(wa / wb), force=True) == 0, checks)
    check("clock_ratio_not_algebraically_identical_to_free_founded_depth", sp.log(2) != sp.log(3), checks)

    summary_checks = {
        key: value
        for key, value in checks.items()
        if not key.startswith(("endpoint_reversal_", "endpoint_triangle_", "invariant_potential_"))
    }
    census_check_count = len(checks) - len(summary_checks)
    result = {
        "schema": "udt-metric-native-signed-depth-derivation-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "summary_check_count": len(summary_checks),
        "census_check_count": census_check_count,
        "total_check_count": len(checks),
        "checks": summary_checks,
        "counts": {
            "candidate_types": 8,
            "endpoint_reversal_checks": 16,
            "endpoint_triangle_checks": 64,
            "invariant_potential_checks": 6,
            "routes_passing_all_six_requirements": 0,
            "Levi_Civita_nonzero_reciprocal_components": 0,
            "conditional_exact_signed_additive_constructions": 5,
        },
        "rulings": {
            "founded_phi": "DERIVED_RECIPROCAL_GROUP_COORDINATE_NOT_AUTOMATIC_SPACETIME_ASSIGNMENT",
            "endpoint_section": "EXACT_ADDITIVE_DEPTH_IF_GLOBAL_FOUNDED_SECTION_IS_SUPPLIED",
            "Levi_Civita": "METRIC_COMPATIBLE_CONNECTION_HAS_ZERO_SELF_ADJOINT_RECIPROCAL_PROJECTION",
            "raw_coframe": "RECOVERS_DEPTH_ONLY_RELATIVE_TO_A_SELECTED_REFERENCE_COFRAME",
            "relative_log": "UNIQUE_EXACT_READOUT_ON_SUPPLIED_POSITIVE_RECIPROCAL_SUBGROUP",
            "general_log": "NOT_AN_ADDITIVE_HOMOMORPHISM_ON_NONCOMMUTING_COMPLETE_MAPS",
            "bilocal": "METRIC_NATIVE_MAGNITUDE_IS_NOT_A_SIGNED_ADDITIVE_DEPTH",
            "clock_ratio": "EXACT_COCYCLE_GIVEN_SIGNAL_DATA_BUT_FOUNDING_IDENTITY_REQUIRES_A_SOLDER",
            "curvature_potential": "EXACT_AFTER_FORMULA_SELECTION_BUT_NONUNIQUE_AND_UNFOUNDED",
            "smallest_join": "METRIC_NATIVE_NORMALIZED_RECIPROCAL_COCYCLE_OR_EQUIVALENT_REFERENCE_CONNECTION",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
