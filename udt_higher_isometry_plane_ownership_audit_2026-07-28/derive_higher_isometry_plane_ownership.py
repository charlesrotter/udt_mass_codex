#!/usr/bin/env python3
"""Exact higher-isometry orbit-plane ownership classification."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def require(name: str, condition: object, checks: list[dict[str, str]]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks.append({"id": name, "status": "PASS"})


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def canonical_line(v: tuple[int, int]) -> tuple[int, int]:
    x, y = v
    divisor = math.gcd(abs(x), abs(y))
    if divisor == 0:
        raise ValueError("zero vector has no primitive line")
    x //= divisor
    y //= divisor
    if x < 0 or (x == 0 and y < 0):
        x, y = -x, -y
    return x, y


def det2(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def main() -> None:
    checks: list[dict[str, str]] = []
    c, u, b = sp.symbols("c_E u b", positive=True, real=True)
    alpha, f = sp.symbols("alpha f", real=True)
    chi, df, db = sp.symbols("chi df db", real=True)
    # Matrix.charpoly constructs an assumption-free generator; use the same
    # kind of symbol so exact polynomial comparisons do not compare two
    # visually identical symbols with different assumption dictionaries.
    lam = sp.Symbol("lambda")

    # Orbit algebra basis (K,V,Y), where A(V)=1, A(Y)=f and
    # H=Y-fV is horizontal with q_B(H,H)=b>0.
    q_vertical = 1 / u - alpha**2 * u
    G = sp.Matrix(
        [
            [-c**2 * u, -c * alpha * u, -c * alpha * u * f],
            [-c * alpha * u, q_vertical, q_vertical * f],
            [-c * alpha * u * f, q_vertical * f, q_vertical * f**2 + b],
        ]
    )
    require("A01_full_orbit_Gram_determinant", sp.factor(G.det()) == -b * c**2, checks)

    change = sp.Matrix([[1, 0, 0], [0, 1, -f], [0, 0, 1]])
    block = sp.Matrix(
        [
            [-c**2 * u, -c * alpha * u, 0],
            [-c * alpha * u, q_vertical, 0],
            [0, 0, b],
        ]
    )
    require("A02_horizontal_congruence_block", sp.simplify(change.T * G * change - block) == sp.zeros(3), checks)
    require("A03_orbit_inertia_is_one_minus_two_plus", sp.factor(block[:2, :2].det()) == -c**2, checks)

    def X(expr: sp.Expr) -> sp.Expr:
        return sp.diff(expr, u) * (-2 * u * chi) + sp.diff(expr, f) * df + sp.diff(expr, b) * db

    XG = G.applyfunc(X)
    D = sp.simplify(G.inv() * XG)
    expected_D = sp.Matrix(
        [
            [-2 * chi, -4 * alpha * chi / c, -4 * alpha * chi * f / c],
            [
                alpha * c * df * f * u / b,
                (alpha**2 * df * f * u**2 + 2 * b * chi * u - df * f) / (b * u),
                (
                    alpha**2 * df * f**2 * u**2
                    + 2 * b * chi * f * u
                    + b * df * u
                    - db * f * u
                    - df * f**2
                )
                / (b * u),
            ],
            [
                -alpha * c * df * u / b,
                -df * (alpha * u - 1) * (alpha * u + 1) / (b * u),
                -(alpha**2 * df * f * u**2 - db * u - df * f) / (b * u),
            ],
        ]
    )
    require("A04_exact_full_orbit_Gram_response", sp.simplify(D - expected_D) == sp.zeros(3), checks)
    require("A05_response_trace_is_horizontal_log_rate", sp.simplify(sp.trace(D) - db / b) == 0, checks)
    require("A06_response_is_Gram_self_adjoint", sp.simplify(G * D - (G * D).T) == sp.zeros(3), checks)

    charpoly = sp.factor(D.charpoly(lam).as_expr())
    expected_charpoly = sp.factor(
        lam**3
        - (db / b) * lam**2
        + (alpha**2 * df**2 * u / b - df**2 / (b * u) - 4 * chi**2) * lam
        - 2 * alpha**2 * df**2 * u * chi / b
        + 4 * db * chi**2 / b
        - 2 * df**2 * chi / (b * u)
    )
    require("A07_exact_response_characteristic_polynomial", sp.simplify(charpoly - expected_charpoly) == 0, checks)
    require("A08_minus_reciprocal_rate_obstruction", sp.factor(charpoly.subs(lam, -2 * chi)) == -4 * alpha**2 * df**2 * u * chi / b, checks)
    require("A09_plus_reciprocal_rate_obstruction", sp.factor(charpoly.subs(lam, 2 * chi)) == -4 * df**2 * chi / (b * u), checks)
    require(
        "A10_df_zero_response_factorization",
        sp.factor(charpoly.subs(df, 0) - (lam + 2 * chi) * (lam - 2 * chi) * (lam - db / b)) == 0,
        checks,
    )

    # Leakage of the registered plane span(K,V) into Y. Both columns must
    # have zero Y component for the plane to be invariant.
    require("A11_K_leakage_from_variable_moment", sp.factor(D[2, 0]) == -alpha * c * df * u / b, checks)
    require(
        "A12_V_leakage_from_variable_moment",
        sp.simplify(D[2, 1] + df * (alpha**2 * u**2 - 1) / (b * u)) == 0,
        checks,
    )
    require(
        "A13_registered_plane_invariant_when_df_zero",
        sp.simplify(D.subs(df, 0)[2, 0]) == 0 and sp.simplify(D.subs(df, 0)[2, 1]) == 0,
        checks,
    )
    # If df!=0, the first leakage can vanish only at alpha=0, when the
    # second is df/(bu), so both cannot vanish together.
    require("A14_no_simultaneous_leakage_cancellation_for_df_nonzero", sp.simplify(D[2, 1].subs(alpha, 0) - df / (b * u)) == 0, checks)

    # Scan every two-plane generated by a noncompact helix
    # T=K+rV+sY and a compact torus line Z=mV+nY.
    r, s, m, n = sp.symbols("r s m n", real=True)
    plane_basis = sp.Matrix([[1, 0], [r, m], [s, n]])
    plane_gram = sp.simplify(plane_basis.T * G * plane_basis)
    delta = sp.factor(r * n - m * s)
    moment_z = sp.factor(m + n * f)
    time_wedge = sp.factor(c * n + alpha * delta)
    expected_plane_det = sp.factor(b * delta**2 / u - c**2 * moment_z**2 - u * b * time_wedge**2)
    require("A15_all_symmetry_plane_Gram_determinants", sp.simplify(plane_gram.det() - expected_plane_det) == 0, checks)
    require("A16_family_identity_f_derivative_forces_vertical_compact_line", sp.factor(sp.diff(expected_plane_det, f)) == -2 * c**2 * n * moment_z, checks)
    f_derivative_poly = sp.Poly(sp.diff(expected_plane_det, f), f)
    require(
        "A16b_family_identity_has_n_squared_leading_coefficient",
        sp.factor(f_derivative_poly.coeff_monomial(f)) == -2 * c**2 * n**2,
        checks,
    )
    det_after_n0 = sp.factor(expected_plane_det.subs(n, 0))
    require(
        "A17_after_vertical_line_horizontal_helix_term",
        det_after_n0 == sp.factor(m**2 * (-c**2 + b * s**2 * (1 / u - alpha**2 * u))),
        checks,
    )
    family_identity_b_coefficient = sp.factor(u * sp.diff(det_after_n0, b))
    require(
        "A17b_family_identity_after_n_zero_forces_s_zero",
        sp.simplify(family_identity_b_coefficient - m**2 * s**2 * (1 - alpha**2 * u**2)) == 0,
        checks,
    )
    require("A18_registered_plane_has_constant_reciprocal_area", sp.factor(det_after_n0.subs(s, 0)) == -c**2 * m**2, checks)

    # All-projective founded clock-norm response. This is a diagnostic using
    # the founded phi; it is not by itself a metric-only plane selector.
    t, p, q = sp.symbols("t p q", real=True)
    spatial_moment = p + q * f
    W_norm = sp.factor(-u * (c * t + alpha * spatial_moment) ** 2 + spatial_moment**2 / u + q**2 * b)
    clock_residual = sp.factor(X(W_norm) + 2 * chi * W_norm)
    expected_clock_residual = sp.factor(
        (
            -2 * alpha**2 * df * f * q**2 * u**2
            - 2 * alpha**2 * df * p * q * u**2
            - 2 * alpha * c * df * q * t * u**2
            + 2 * b * chi * q**2 * u
            + 4 * chi * f**2 * q**2
            + 8 * chi * f * p * q
            + 4 * chi * p**2
            + db * q**2 * u
            + 2 * df * f * q**2
            + 2 * df * p * q
        )
        / u
    )
    require("A19_all_projective_clock_response_residual", sp.simplify(clock_residual - expected_clock_residual) == 0, checks)
    require("A20_founded_K_always_has_clock_response", sp.simplify(clock_residual.subs({p: 0, q: 0})) == 0, checks)
    require("A21_family_identity_db_coefficient_forces_no_horizontal_component", sp.factor(sp.diff(clock_residual, db)) == q**2, checks)
    require("A22_after_q_zero_nonconstant_depth_forces_no_vertical_helix", sp.factor(clock_residual.subs(q, 0)) == 4 * chi * p**2 / u, checks)

    # Exact smooth nonconstant-depth twist-off countercontrol. With a standard
    # toric S3 connection f=cos(theta), choose the horizontal norm
    # b=(1-f^2)/u. Then both Hopf and anti-Hopf free circles have norm 1/u.
    b_double = (1 - f**2) / u
    G_twist_off = sp.simplify(G.subs({alpha: 0, b: b_double}))
    KV = G_twist_off.extract([0, 1], [0, 1])
    KY = G_twist_off.extract([0, 2], [0, 2])
    reciprocal_pair = sp.diag(-c**2 * u, 1 / u)
    require("A23_registered_Hopf_plane_exact_in_double_witness", sp.simplify(KV - reciprocal_pair) == sp.zeros(2), checks)
    require("A24_anti_Hopf_plane_exact_in_double_witness", sp.simplify(KY - reciprocal_pair) == sp.zeros(2), checks)
    epsilon = sp.symbols("epsilon", positive=True, real=True)
    u_witness = 1 + epsilon * (1 - f**2)
    require(
        "A25_double_witness_positive_horizontal_interior",
        sp.simplify(b_double.subs(u, u_witness) - (1 - f**2) / (1 + epsilon * (1 - f**2))) == 0,
        checks,
    )

    # Turning on alpha preserves the alternative plane's constant determinant
    # but shifts its response rates whenever the connection moment varies.
    KY_twisted = sp.simplify(plane_gram.subs({r: 0, s: 0, m: 0, n: 1, b: b_double}))
    X_KY_twisted = KY_twisted.applyfunc(lambda expr: sp.diff(expr, u) * (-2 * u * chi) + sp.diff(expr, f) * df)
    D_KY_twisted = sp.simplify(KY_twisted.inv() * X_KY_twisted)
    require("A26_twisted_anti_Hopf_plane_constant_area", sp.factor(KY_twisted.det()) == -c**2, checks)
    require(
        "A27_twisted_anti_Hopf_rate_shift",
        sp.factor(D_KY_twisted.det() + 4 * chi**2) == alpha**2 * df**2 * u**2,
        checks,
    )

    # Exhaust all small unimodular cap bases. The symbolic proof is that in
    # the cap basis freeness forces both coefficients to be +/-1. Enumeration
    # is a catch against sign, orientation, and primitive-line errors.
    cap_rows: list[dict[str, object]] = []
    cap_pair_count = 0
    for a1 in range(-2, 3):
        for a2 in range(-2, 3):
            v_minus = (a1, a2)
            if math.gcd(abs(a1), abs(a2)) != 1:
                continue
            for b1 in range(-2, 3):
                for b2 in range(-2, 3):
                    v_plus = (b1, b2)
                    cap_det = det2(v_minus, v_plus)
                    if abs(cap_det) != 1:
                        continue
                    cap_pair_count += 1
                    actual: set[tuple[int, int]] = set()
                    for w1 in range(-5, 6):
                        for w2 in range(-5, 6):
                            if (w1, w2) == (0, 0) or math.gcd(abs(w1), abs(w2)) != 1:
                                continue
                            w = (w1, w2)
                            if abs(det2(v_minus, w)) == 1 and abs(det2(v_plus, w)) == 1:
                                actual.add(canonical_line(w))
                    expected = {
                        canonical_line((v_minus[0] + v_plus[0], v_minus[1] + v_plus[1])),
                        canonical_line((v_minus[0] - v_plus[0], v_minus[1] - v_plus[1])),
                    }
                    require(f"T{cap_pair_count:04d}_two_free_lines", actual == expected and len(actual) == 2, checks)
                    cap_rows.append(
                        {
                            "id": f"C{cap_pair_count:04d}",
                            "v_minus": f"{v_minus[0]},{v_minus[1]}",
                            "v_plus": f"{v_plus[0]},{v_plus[1]}",
                            "cap_determinant": cap_det,
                            "free_unoriented_line_1": f"{sorted(actual)[0][0]},{sorted(actual)[0][1]}",
                            "free_unoriented_line_2": f"{sorted(actual)[1][0]},{sorted(actual)[1][1]}",
                            "free_line_count": 2,
                        }
                    )
    require("A28_cap_enumeration_nonempty", cap_pair_count > 0, checks)
    standard_minus = (1, 0)
    standard_plus = (0, 1)
    standard_actual: set[tuple[int, int]] = set()
    for w1 in range(-3, 4):
        for w2 in range(-3, 4):
            if (w1, w2) == (0, 0) or math.gcd(abs(w1), abs(w2)) != 1:
                continue
            w = (w1, w2)
            if abs(det2(standard_minus, w)) == 1 and abs(det2(standard_plus, w)) == 1:
                standard_actual.add(canonical_line(w))
    require("A29_standard_S3_has_Hopf_and_anti_Hopf_free_lines", standard_actual == {(1, 1), (1, -1)}, checks)

    strata_rows = [
        {"id": "S01", "stratum": "exact_RxS1_nonconstant_phi", "higher_isometry": "NONE", "plane_scan": "ONLY_REGISTERED_ORBIT_PLANE_EXISTS", "full_response": "PAIR_EIGENLINES_K_AND_V-alpha_over_cK", "topology": "ONE_REGISTERED_COMPACT_LINE", "classification": "UNIQUE_CONDITIONAL_ON_ISOMETRY_RANK"},
        {"id": "S02", "stratum": "RxT2_formal_family_identity_test", "higher_isometry": "EXTRA_COMPACT_Y", "plane_scan": "ONLY_span_KV_IS_ROBUST_UNDER_INDEPENDENT_FAMILY_VARIATION", "full_response": "span_KV_NOT_INVARIANT_WHERE_df_NONZERO", "topology": "TWO_FREE_S1_LINES_FOR_S3_CAPS", "classification": "FAMILY_IDENTITY_RESULT__FIXED_METRIC_UNIQUENESS_OPEN"},
        {"id": "S03", "stratum": "RxT2_nonconstant_phi_alpha_zero_conformally_round_spatial", "higher_isometry": "TWO_TORIC_CIRCLES", "plane_scan": "span_KV_AND_span_KY_BOTH_EXACT_RECIPROCAL", "full_response": "K_REMAINS_FULL_RESPONSE_EIGENLINE_BUT_RULER_PLANE_MULTIPLE", "topology": "HOPF_AND_ANTI_HOPF_BOTH_FREE", "classification": "MULTIPLE_EQUIVALENT_RECIPROCAL_PLANES"},
        {"id": "S04", "stratum": "same_double_witness_alpha_nonzero_df_nonzero", "higher_isometry": "TWO_TORIC_CIRCLES", "plane_scan": "BOTH_CONSTANT_AREA_BUT_ANTI_HOPF_RATE_SHIFTED", "full_response": "REGISTERED_PLANE_MIXES_IN_FULL_3x3_D", "topology": "TWO_FREE_LINES_REMAIN", "classification": "REGISTERED_PAIR_RATE_DISTINGUISHED_IN_THIS_WITNESS"},
        {"id": "S05", "stratum": "constant_phi_RxT2", "higher_isometry": "EXTRA_COMPACT_Y", "plane_scan": "RECIPROCAL_DEPTH_RATE_ZERO", "full_response": "NO_DEPTH_SELECTOR", "topology": "TWO_FREE_LINES_GENERIC_S3_TORUS", "classification": "DEGENERATE_OR_METRIC_SHAPE_DEPENDENT"},
        {"id": "S06", "stratum": "constant_phi_Berger_U2_alpha_nonzero", "higher_isometry": "UNVERIFIED_CONTROL_LABEL", "plane_scan": "NOT_DERIVED_IN_THIS_PACKAGE", "full_response": "NOT_DERIVED_IN_THIS_PACKAGE", "topology": "NOT_DERIVED_IN_THIS_PACKAGE", "classification": "UNVERIFIED_ILLUSTRATION_NOT_EVIDENCE"},
        {"id": "S07", "stratum": "constant_phi_round_alpha_zero", "higher_isometry": "UNVERIFIED_CONTROL_LABEL", "plane_scan": "NOT_DERIVED_IN_THIS_PACKAGE", "full_response": "NOT_DERIVED_IN_THIS_PACKAGE", "topology": "NOT_DERIVED_IN_THIS_PACKAGE", "classification": "UNVERIFIED_ILLUSTRATION_NOT_EVIDENCE"},
        {"id": "S08", "stratum": "higher_isometry_not_preserving_registered_Hopf_bundle", "higher_isometry": "UNCLASSIFIED_NONCENTRAL_OR_EXOTIC", "plane_scan": "NOT_EXHAUSTED", "full_response": "NOT_EXHAUSTED", "topology": "OTHER_COMPLETIONS_OPEN", "classification": "OPEN_OUTSIDE_BOUNDED_FAMILY"},
    ]
    status_rows = [
        {"claim_id": "R01", "object": "full_RxT2_orbit_Gram", "status": "DERIVED", "scope": "stationary_descended_block_screen_principal_orbits_b_positive", "statement": "det_G3=-b*c_E^2_and_inertia_is_Lorentzian"},
        {"claim_id": "R02", "object": "full_Gram_response", "status": "DERIVED", "scope": "principal_orbits_b_positive_with_arbitrary_formal_first_jets_chi_df_db", "statement": "variable_connection_moment_mixes_registered_plane"},
        {"claim_id": "R03", "object": "family_identity_plane_scan", "status": "DERIVED_IDENTITY_LEVEL_ONLY", "scope": "polynomial_identity_under_independent_family_variation_of_u_f_b", "statement": "only_span_KV_has_constant_reciprocal_area_robustly_across_the_whole_free_family"},
        {"claim_id": "R04", "object": "family_identity_clock_response", "status": "DERIVED_IDENTITY_LEVEL_ONLY", "scope": "polynomial_identity_under_independent_family_variation_with_nonzero_depth_jet", "statement": "only_K_has_founded_clock_norm_response_robustly_across_the_whole_free_family"},
        {"claim_id": "R05", "object": "S3_toric_topology", "status": "DERIVED", "scope": "smooth_unimodular_two_cap_T2_completion", "statement": "exactly_two_unoriented_primitive_free_circle_lines"},
        {"claim_id": "R06", "object": "nonconstant_depth_double_plane_control", "status": "DERIVED_EXISTENCE", "scope": "alpha_zero_conformally_round_spatial_toric_S3", "statement": "Hopf_and_anti_Hopf_planes_both_have_exact_founded_reciprocal_Gram_form"},
        {"claim_id": "R07", "object": "universal_plane_selection", "status": "REFUTED_BOUNDED", "scope": "admitted_stationary_higher_isometry_family", "statement": "exact_smooth_nonconstant_depth_R06_control_retains_two_isometry_equivalent_reciprocal_planes"},
        {"claim_id": "R08", "object": "generic_fixed_metric_plane_selection", "status": "OPEN", "scope": "fixed_cohomogeneity_one_profiles", "statement": "requires_necessary_and_sufficient_profile_classification_or_valid_transversality_theorem"},
        {"claim_id": "R09", "object": "full_D_eigenplane_selection", "status": "REFUTED_WHERE_df_NONZERO_ON_PRINCIPAL_ORBITS", "scope": "bundle_preserving_extra_circle_with_nontrivial_moment_and_b_positive", "statement": "restricted_plane_scan_and_full_orbit_eigenplane_are_not_the_same_operation"},
        {"claim_id": "R10", "object": "macro_micro_or_mass_assignment", "status": "OPEN", "scope": "not_tested", "statement": "no_physical_regime_assignment"},
        {"claim_id": "R11", "object": "action_source_carrier_density_dynamics", "status": "OPEN", "scope": "not_loaded", "statement": "unchanged"},
    ]
    circle_rows = [
        {"id": "L01", "cap_basis": "v_minus,v_plus_with_abs_det_1", "circle": "v_minus+v_plus", "primitive": "YES", "free_at_both_caps": "YES", "orientation": "UNORIENTED_LINE_1", "metric_selection": "NOT_FROM_TOPOLOGY"},
        {"id": "L02", "cap_basis": "v_minus,v_plus_with_abs_det_1", "circle": "v_minus-v_plus", "primitive": "YES", "free_at_both_caps": "YES", "orientation": "UNORIENTED_LINE_2", "metric_selection": "NOT_FROM_TOPOLOGY"},
        {"id": "L03", "cap_basis": "standard_(1,0),(0,1)", "circle": "(1,1)", "primitive": "YES", "free_at_both_caps": "YES", "orientation": "HOPF_LABEL_CONDITIONAL", "metric_selection": "REGISTERED_BY_CHOSEN_A"},
        {"id": "L04", "cap_basis": "standard_(1,0),(0,1)", "circle": "(1,-1)", "primitive": "YES", "free_at_both_caps": "YES", "orientation": "ANTI_HOPF_LABEL_CONDITIONAL", "metric_selection": "EQUIVALENT_IN_DOUBLE_WITNESS"},
    ]
    write_tsv("HIGHER_ISOMETRY_STRATA.tsv", strata_rows)
    write_tsv("STATUS_LEDGER.tsv", status_rows)
    write_tsv("FREE_CIRCLE_CLASSES.tsv", circle_rows)
    write_tsv("TORIC_CAP_ENUMERATION.tsv", cap_rows)

    result = {
        "schema": "udt-higher-isometry-plane-ownership-1.0",
        "base": "99cbec700add7f72f3ff9e67f3bdfaa89cfd1724",
        "preregistration_commit": "3e3eecc",
        "checks": checks,
        "check_count": len(checks),
        "symbolic_check_count": 31,
        "toric_cap_pair_count": cap_pair_count,
        "toric_enumeration_check_count": cap_pair_count,
        "orbit_gram": {
            "basis": ["K", "V", "Y"],
            "determinant": "-b*c_E^2",
            "inertia": "one_negative_two_positive",
            "connection_moment": "f=A(Y)",
            "horizontal_norm": "b=q_B(Y-fV,Y-fV)",
        },
        "full_response": {
            "trace": "X(b)/b",
            "registered_plane_invariant_iff_within_nonzero_df_analysis": "df=0",
            "plus_2chi_eigenvalue_when_chi_df_nonzero": False,
            "minus_2chi_eigenvalue_when_chi_df_alpha_nonzero": False,
            "important_distinction": "full_orbit_D_eigenplane_is_not_the_restricted_two_plane_scan",
        },
        "plane_scan": {
            "general_plane": "span(K+rV+sY,mV+nY)",
            "gram_determinant": str(expected_plane_det),
            "family_identity_robust_constant_area_plane": "span(K,V)",
            "generic_fixed_metric_unique_constant_area_plane": "OPEN",
            "exceptional_locus": "functional_relations_among_u_f_b_can_create_additional_constant_area_or_reciprocal_planes",
        },
        "topology": {
            "smooth_S3_unimodular_caps_free_unoriented_circle_count": 2,
            "topology_selects_registered_V": False,
        },
        "countercontrol": {
            "alpha": 0,
            "u": "1+epsilon*(1-f^2)",
            "b": "(1-f^2)/u",
            "phi_nonconstant": True,
            "reciprocal_planes": ["span(K,V)", "span(K,Y)"],
            "V_and_Y": "Hopf_and_anti_Hopf_primitive_free_circles",
        },
        "primary_classification": "UNIVERSAL_SELECTION_REFUTED__FAMILY_IDENTITY_ROBUSTNESS_DERIVED__GENERIC_FIXED_METRIC_SELECTION_OPEN",
        "universal_registered_plane_selection": "REFUTED_WITHIN_BOUNDED_FAMILY",
        "generic_registered_plane_selection": "OPEN_QUANTIFIER_CORRECTION_REQUIRED_FIXED_PROFILE_CLASSIFICATION",
        "family_identity_registered_plane_robustness": "DERIVED_UNDER_INDEPENDENT_CONFIGURATION_FAMILY_VARIATION",
        "macro_micro_assignment": "OPEN_NOT_TESTED",
        "maximum_conclusion": "UNIVERSAL_PLANE_SELECTION_IS_REFUTED_BY_AN_EXACT_SMOOTH_NONCONSTANT_DEPTH_COUNTERCONTROL;THE_ORBIT_ALGEBRA_TOPOLOGY_THEOREM_AND_FAMILY_IDENTITY_ROBUSTNESS_OF_span_KV_ARE_DERIVED;GENERIC_FIXED_METRIC_SELECTION_AND_THE_COMPLETE_RESPONSE_DEGENERACY_ATLAS_REMAIN_OPEN;NO_PHYSICAL_BRANCH_OR_MACRO_MICRO_ASSIGNMENT_IS_DERIVED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
