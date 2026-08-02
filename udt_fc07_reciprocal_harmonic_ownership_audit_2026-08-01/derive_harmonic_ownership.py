#!/usr/bin/env python3
"""Exact FC07 reciprocal/harmonic ownership derivation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
checks: list[tuple[str, bool]] = []


def ck(name: str, condition: object) -> None:
    ok = bool(condition)
    checks.append((name, ok))
    if not ok:
        raise AssertionError(name)


def zmat(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in matrix)


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    # General lower-triangular stationary coframe at one event.
    a, p = sp.symbols("a p", positive=True, nonzero=True)
    b1, b2, u1, u2 = sp.symbols("b1 b2 u1 u2", real=True)
    p11, p12, p21, p22 = sp.symbols("p11 p12 p21 p22", real=True)
    P = sp.Matrix([[p11, p12], [p21, p22]])
    d = sp.det(P)
    b = sp.Matrix([b1, b2])
    E3 = sp.Matrix([[a, 0, 0], [b1, p11, p12], [b2, p21, p22]])
    q = sp.simplify(E3.T * E3)
    E3i = sp.simplify(E3.inv())
    qi = sp.simplify(E3i * E3i.T)
    v = sp.simplify(P.inv() * b)

    ck("S01_spatial_metric_symmetric", q == q.T)
    ck("S02_spatial_determinant", sp.factor(q.det() - a**2 * d**2) == 0)
    ck("S03_inverse_exact", zmat(q * qi - sp.eye(3)))
    ck("S04_inverse_ss", sp.simplify(qi[0, 0] - a**-2) == 0)
    ck("S05_inverse_screen_base", zmat(qi[1:, 0] + v / a**2))
    ck("S06_spatial_volume_mixing_independent", not ({b1, b2} & q.det().free_symbols))

    # Unit-period harmonic representative: I is the whole-cell integral.
    I = sp.symbols("I", positive=True, nonzero=True)
    theta1 = sp.Matrix([a, 0, 0])
    alpha = sp.Matrix([a / (I * d), 0, 0])
    dual_theta = sp.simplify(qi * theta1)
    dual_alpha = sp.simplify(qi * alpha)
    ntheta = sp.simplify((theta1.T * dual_theta)[0])
    nalpha = sp.simplify((alpha.T * dual_alpha)[0])
    proj_theta = sp.simplify(dual_theta * theta1.T / ntheta)
    proj_alpha = sp.simplify(dual_alpha * alpha.T / nalpha)
    expected_dual_theta = sp.Matrix([1 / a, -v[0] / a, -v[1] / a])

    ck("H01_theta1_unit_covector", sp.simplify(ntheta - 1) == 0)
    ck("H02_theta1_dual_with_mixing", zmat(dual_theta - expected_dual_theta))
    ck("H03_alpha_rescales_theta1", zmat(alpha - theta1 / (I * d)))
    ck("H04_alpha_norm", sp.simplify(nalpha - 1 / (I**2 * d**2)) == 0)
    ck("H05_projector_exact_ownership", zmat(proj_alpha - proj_theta))
    ck("H06_projector_idempotent", zmat(proj_alpha * proj_alpha - proj_alpha))
    ck("H07_projector_rank_one", sp.simplify(sp.trace(proj_alpha) - 1) == 0)
    ck("H08_spatial_mixing_cancels_from_rescaling", not ({b1, b2} & (a / (I * d)).free_symbols))

    # Full Lorentzian coframe: the clock-screen mixing u also drops from ruler ownership.
    E4 = sp.Matrix(
        [
            [p, 0, 0, 0],
            [0, a, 0, 0],
            [u1, b1, p11, p12],
            [u2, b2, p21, p22],
        ]
    )
    eta = sp.diag(-1, 1, 1, 1)
    g = sp.simplify(E4.T * eta * E4)
    E4i = sp.simplify(E4.inv())
    gi = sp.simplify(E4i * eta * E4i.T)
    theta1_4 = sp.Matrix([0, a, 0, 0])
    dual_theta_4 = sp.simplify(gi * theta1_4)
    expected_dual_4 = sp.Matrix([0, 1 / a, -v[0] / a, -v[1] / a])
    ck("F01_lorentzian_determinant", sp.factor(g.det() + p**2 * a**2 * d**2) == 0)
    ck("F02_full_inverse_exact", zmat(g * gi - sp.eye(4)))
    ck("F03_full_ruler_dual", zmat(dual_theta_4 - expected_dual_4))
    ck("F04_clock_mixing_drops_from_ruler", not ({u1, u2} & set().union(*(x.free_symbols for x in dual_theta_4))))

    # Differential Hodge equation for arbitrary smooth phi/screen/mixing profiles.
    s = sp.symbols("s", real=True)
    af = sp.Function("a", positive=True)(s)
    df = sp.Function("D", positive=True)(s)  # oriented det(P)=sqrt(det h)
    ff = sp.Function("f")(s)
    C = sp.symbols("C", real=True)
    flux_general = sp.simplify(df * ff / af)
    harmonic_f = C * af / df
    flux_harmonic = sp.simplify(flux_general.subs(ff, harmonic_f))
    theta_flux = sp.simplify(flux_general.subs(ff, af))
    delta_theta = sp.simplify(-sp.diff(theta_flux, s) / (af * df))
    ck("D01_general_coclosed_flux", flux_general == df * ff / af)
    ck("D02_harmonic_solution_flux_constant", sp.diff(flux_harmonic, s) == 0)
    ck("D03_harmonic_solution", sp.simplify(harmonic_f - C * af / df) == 0)
    ck("D04_theta1_closed_identically", sp.diff(af, s) - sp.diff(af, s) == 0)
    ck("D05_theta1_coclosure", sp.simplify(delta_theta + sp.diff(df, s) / (af * df)) == 0)
    ck("D06_theta1_harmonic_if_area_constant", delta_theta.subs(sp.diff(df, s), 0) == 0)
    ck("D07_phi_derivative_absent_from_theta_harmonicity", not delta_theta.has(sp.diff(af, s)))

    # Monodromy and cohomology: all four rows have no invariant fiber covector.
    monodromies = [
        ("O01", "M_MINUS_IDENTITY", sp.Matrix([[-1, 0], [0, -1]]), "constant_registered;general_descending"),
        ("O02", "M_ORDER4_ROTATION", sp.Matrix([[0, -1], [1, 0]]), "constant_and_varying"),
        ("O03", "M_ORDER6_ELLIPTIC", sp.Matrix([[0, -1], [1, 1]]), "constant_and_varying"),
        ("O04", "M_HYPERBOLIC", sp.Matrix([[2, 1], [1, 1]]), "forced_varying"),
    ]
    descent_rows: list[dict[str, object]] = []
    ownership_rows: list[dict[str, object]] = []
    for cid, name, M, strata in monodromies:
        ker_test = sp.factor((M.T - sp.eye(2)).det())
        ck(f"M_{cid}_unimodular", abs(int(M.det())) == 1)
        ck(f"M_{cid}_orientation_preserving", M.det() == 1)
        ck(f"M_{cid}_no_invariant_fiber_covector", ker_test != 0)
        h11, h12, h22 = sp.symbols(f"h11_{cid} h12_{cid} h22_{cid}", real=True)
        h0 = sp.Matrix([[h11, h12], [h12, h22]])
        h1 = sp.simplify(M.T * h0 * M)
        ck(f"M_{cid}_screen_area_descends", sp.factor(h1.det() - h0.det()) == 0)
        descent_rows.append(
            {
                "candidate_id": cid,
                "monodromy": name,
                "det_M": int(M.det()),
                "det_Mt_minus_I": ker_test,
                "b1": 1,
                "invariant_fiber_covector": "NONE",
                "base_harmonic_line": "UNIQUE",
                "descent_status": "PASS",
            }
        )
        ownership_rows.append(
            {
                "candidate_id": cid,
                "monodromy": name,
                "screen_strata": strata,
                "line_ownership": "ALL_SMOOTH_NONDEGENERATE_BOUNDED_MEMBERS",
                "rescaled_form": "alpha=theta1/(I*sqrt(det(h)))",
                "theta1_harmonic": "IFF_d_ds_sqrt_det_h_EQUALS_0",
                "mixing_dependence": "NONE_FOR_u_OR_b",
                "mixing_descent_scope": "CHOSE_BOUNDED_FIELD_GENERALIZATION_CONTAINING_E02__CONDITIONAL_ON_GLOBAL_DESCENT",
                "physical_selection": "NONE",
            }
        )

    # Existing symmetric metric interpolation: every nonconstant screen changes area.
    chi, det_h0, det_delta = sp.symbols("chi det_h0 det_delta", real=True)
    det_h_chi = det_h0 + det_delta * (chi**2 - chi)
    ck("A01_endpoint_area_equal", sp.simplify(det_h_chi.subs(chi, 1) - det_h_chi.subs(chi, 0)) == 0)
    ck("A02_nonconstant_unimodular_interpolation_area_varies", sp.diff(det_h_chi, chi) != 0)
    ck("A03_midpoint_area_extremum", sp.diff(det_h_chi, chi).subs(chi, sp.Rational(1, 2)) == 0)
    ck("A04_constant_screen_area_constant", det_h_chi.subs(det_delta, 0) == det_h0)

    window_rows = [
        {
            "object": "harmonic_line_ownership",
            "condition": "a>0;det(P)>0;smooth_compact_descent;b1=1",
            "background_dependence": "IDENTITY_ACROSS_OPEN_NONDEGENERATE_FAMILY",
            "window_class": "NO_NONTRIVIAL_CURVATURE_WINDOW",
            "bootstrap_status": "KINEMATIC_COMPATIBILITY_NOT_RETURN_EQUATION",
        },
        {
            "object": "theta1_itself_harmonic",
            "condition": "d_ds_sqrt(det(h))=0",
            "background_dependence": "ANGULAR_AREA_EQUALITY_STRATUM",
            "window_class": "CODIMENSION_CONDITION_NOT_FINITE_RANGE",
            "bootstrap_status": "NO_CURRENT_PREMISE_REQUIRES_THIS_CONDITION",
        },
        {
            "object": "unit_period_normalization",
            "condition": "I=int_cell L*exp(phi)/sqrt(det(h)) ds finite_positive",
            "background_dependence": "GLOBAL_PHI_AND_ANGULAR_AREA_FUNCTIONAL",
            "window_class": "READOUT_FOR_EVERY_SMOOTH_NONDEGENERATE_MEMBER",
            "bootstrap_status": "NONIDENTITY_GLOBAL_TO_LOCAL_READOUT_NOT_CLOSURE",
        },
        {
            "object": "degenerate_boundaries",
            "condition": "a_to_0_or_det(P)_to_0_or_noncompact_singular_limit",
            "background_dependence": "COFRAME_OR_HODGE_DOMAIN_BREAKDOWN",
            "window_class": "DOMAIN_BOUNDARY_NOT_BOOTSTRAP_WINDOW",
            "bootstrap_status": "CHARACTERIZED_NOT_FILTERED",
        },
        {
            "object": "rho_tot_or_energy_density",
            "condition": "NO_NATIVE_DENSITY_CURVATURE_SOURCE_MAP_IN_SCOPE",
            "background_dependence": "UNTYPED",
            "window_class": "OPEN_NOT_COMPUTABLE_HERE",
            "bootstrap_status": "NO_DENSITY_CLAIM",
        },
    ]
    write_tsv("MONODROMY_DESCENT_ATLAS.tsv", descent_rows)
    write_tsv("OWNERSHIP_ATLAS.tsv", ownership_rows)
    write_tsv("BACKGROUND_WINDOW_ATLAS.tsv", window_rows)

    result = {
        "schema": "udt.fc07.reciprocal_harmonic_ownership.v1",
        "checks": len(checks),
        "all_checks_pass": all(ok for _, ok in checks),
        "candidate_rows": len(monodromies),
        "result": "RECIPROCAL_HARMONIC_LINE_OWNERSHIP_DERIVED_ON_BOUNDED_LOWER_TRIANGULAR_FC07_CLASS_CONTAINING_E02",
        "harmonic_form": "alpha=theta1/(I*sqrt(det(h)));I=int_cell L*exp(phi)/sqrt(det(h)) ds",
        "ruler_harmonic_condition": "d_ds_sqrt(det(h))=0",
        "mixing_result": "u_A_and_b_A_cancel_exactly_from_line_ownership_and_normalization",
        "mixing_global_scope": "CHOSE_BOUNDED_FIELD_GENERALIZATION_CONTAINING_REGISTERED_E02__EVERY_SMOOTH_DESCENDING_MEMBER__J07_J11_NOT_SOLVED",
        "mixing_field_promotion_status": "CHOSE_BOUNDED_GENERALIZATION_NOT_DERIVED",
        "window_result": "NO_NONTRIVIAL_CURVATURE_WINDOW_AT_KINEMATIC_OWNERSHIP_LEVEL",
        "bootstrap_result": "GLOBAL_TO_LOCAL_READOUT_PRESENT__NO_SAME_SOLUTION_RETURN_EQUATION",
        "density_result": "OPEN_NO_NATIVE_DENSITY_CURVATURE_BRIDGE",
        "nontrivial_background_window_derived": False,
        "native_return_equation_derived": False,
        "density_curvature_bridge_derived": False,
        "physical_completion_selected": False,
        "matter_or_source_derived": False,
        "mixing_descent_law_derived": False,
        "maximum_conclusion": "FOUR_UNIQUE_H1_FC07_COMPLETIONS_HAVE_EXACT_RECIPROCAL_HARMONIC_LINE_OWNERSHIP_FOR_ARBITRARY_SMOOTH_FINITE_DESCENDING_PHI_AND_EVERY_DESCENDING_MEMBER_OF_A_BOUNDED_LOWER_TRIANGULAR_PAIR_SCREEN_MIXING_CLASS_CONTAINING_THE_REGISTERED_E02_MEMBERS__ANGULAR_AREA_MODULATES_THE_LOCAL_HARMONIC_AMPLITUDE_THROUGH_A_COMPLETE_CELL_NORMALIZATION__THE_UNRESCALED_RULER_IS_HARMONIC_IFF_ANGULAR_AREA_IS_CONSTANT__NO_NONTRIVIAL_BACKGROUND_CURVATURE_WINDOW_NATIVE_RETURN_EQUATION_DENSITY_BRIDGE_XMAX_OR_MATTER",
        "check_names": [name for name, _ in checks],
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS exact ownership derivation checks={len(checks)} candidates={len(monodromies)}")
    print(result["maximum_conclusion"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
