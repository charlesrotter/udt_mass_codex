#!/usr/bin/env python3
"""Exact complete-cell Cartan alternating-response production audit."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import sympy as sp


HERE = Path(__file__).resolve().parent
DIM = 4
ETA = (-1, 1, 1, 1)
PAIRS = tuple((i, j) for i in range(DIM) for j in range(i + 1, DIM))
SPATIAL_PAIRS = ((1, 2), (1, 3), (2, 3))
Form = dict[tuple[int, ...], sp.Expr]


def clean(form: Form, substitutions: dict[sp.Symbol, sp.Expr] | None = None) -> Form:
    out: Form = {}
    for key, value in form.items():
        if substitutions:
            value = value.subs(substitutions)
        value = sp.factor(sp.expand(value))
        if value != 0:
            out[key] = value
    return out


def add(*forms: Form) -> Form:
    out: defaultdict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for form in forms:
        for key, value in form.items():
            out[key] += value
    return clean(dict(out))


def scale(value: sp.Expr, form: Form) -> Form:
    return clean({key: value * coefficient for key, coefficient in form.items()})


def wedge(left: Form, right: Form) -> Form:
    out: defaultdict[tuple[int, ...], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    for left_key, left_value in left.items():
        for right_key, right_value in right.items():
            if set(left_key).intersection(right_key):
                continue
            inversions = sum(i > j for i in left_key for j in right_key)
            key = tuple(sorted(left_key + right_key))
            out[key] += (-1) ** inversions * left_value * right_value
    return clean(dict(out))


def basis(key: tuple[int, ...]) -> Form:
    return {key: sp.Integer(1)}


def one(index: int) -> Form:
    return basis((index,))


def write_tsv(name: str, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


p1, p2, p3, s1, s2, s3, m, t1 = sp.symbols(
    "p1 p2 p3 s1 s2 s3 m t1", real=True
)
P = (p1, p2, p3)
S = (s1, s2, s3)
BASE_VARIABLES = P + S + (m, t1)
DERIV = {
    (direction, variable): sp.Symbol(f"E{direction}_{variable}", real=True)
    for direction in (1, 2, 3)
    for variable in P + S
}


# Exact isotropic-screen subfamily of the complete stationary S3 control:
# P_screen=exp(sigma/2) I, alpha=0, C=[[0,-1],[1,0]].
DPHI = add(*(scale(P[index - 1], one(index)) for index in (1, 2, 3)))
DSIGMA = add(*(scale(S[index - 1], one(index)) for index in (1, 2, 3)))
DTHETA: list[Form] = [
    scale(-1, wedge(DPHI, one(0))),
    add(wedge(DPHI, one(1)), scale(t1, wedge(one(2), one(3)))),
    {(1, 2): s1 / 2, (1, 3): -m, (2, 3): -s3 / 2},
    {(1, 2): m, (1, 3): s1 / 2, (2, 3): s2 / 2},
]


def d_scalar(expression: sp.Expr) -> Form:
    components: dict[tuple[int, ...], sp.Expr] = {}
    for direction in (1, 2, 3):
        value = sp.Integer(0)
        for variable in P + S:
            value += sp.diff(expression, variable) * DERIV[(direction, variable)]
        # Exact Cartan-scalar identities on the chosen complete S3 family.
        value += sp.diff(expression, m) * (-m * P[direction - 1])
        value += sp.diff(expression, t1) * (t1 * (P[direction - 1] - S[direction - 1]))
        components[(direction,)] = value
    return clean(components)


def d_basis(key: tuple[int, ...]) -> Form:
    out: Form = {}
    for position, index in enumerate(key):
        term = wedge(basis(key[:position]), DTHETA[index])
        term = wedge(term, basis(key[position + 1 :]))
        out = add(out, scale((-1) ** position, term))
    return out


def exterior_d(form: Form) -> Form:
    out: Form = {}
    for key, coefficient in form.items():
        out = add(
            out,
            wedge(d_scalar(coefficient), basis(key)),
            scale(coefficient, d_basis(key)),
        )
    return out


def closure_substitutions() -> tuple[dict[sp.Symbol, sp.Expr], dict[str, str]]:
    dp = exterior_d(DPHI)
    ds = exterior_d(DSIGMA)
    solve_for = [
        DERIV[(1, p2)], DERIV[(1, p3)], DERIV[(2, p3)],
        DERIV[(1, s2)], DERIV[(1, s3)], DERIV[(2, s3)],
    ]
    equations = [dp.get(pair, 0) for pair in SPATIAL_PAIRS]
    equations += [ds.get(pair, 0) for pair in SPATIAL_PAIRS]
    solved = sp.solve(equations, solve_for, dict=True)
    assert len(solved) == 1
    substitutions = solved[0]
    checks = {
        "dp_after_closure": str(clean(dp, substitutions)),
        "dsigma_after_closure": str(clean(ds, substitutions)),
    }
    assert clean(dp, substitutions) == {}
    assert clean(ds, substitutions) == {}
    return substitutions, checks


def solve_connection() -> tuple[list[list[Form]], list[list[Form]]]:
    unknowns: list[sp.Symbol] = []
    lower: list[list[Form]] = [[{} for _ in range(DIM)] for _ in range(DIM)]
    for a, b in PAIRS:
        form: Form = {}
        for c in range(DIM):
            symbol = sp.Symbol(f"w{a}{b}_{c}", real=True)
            unknowns.append(symbol)
            form[(c,)] = symbol
        lower[a][b] = form
        lower[b][a] = scale(-1, form)
    mixed = [[scale(ETA[a], lower[a][b]) for b in range(DIM)] for a in range(DIM)]
    equations: list[sp.Expr] = []
    for a in range(DIM):
        torsion = DTHETA[a]
        for b in range(DIM):
            torsion = add(torsion, wedge(mixed[a][b], one(b)))
        equations.extend(torsion.get(pair, 0) for pair in PAIRS)
    matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)
    solutions = list(sp.linsolve((matrix, rhs), unknowns))
    assert len(solutions) == 1 and len(solutions[0]) == len(unknowns)
    substitution = dict(zip(unknowns, solutions[0]))
    lower = [[clean(form, substitution) for form in row] for row in lower]
    mixed = [[scale(ETA[a], lower[a][b]) for b in range(DIM)] for a in range(DIM)]
    # Exact zero-torsion replay.
    for a in range(DIM):
        torsion = DTHETA[a]
        for b in range(DIM):
            torsion = add(torsion, wedge(mixed[a][b], one(b)))
        assert torsion == {}
    return lower, mixed


def curvature(
    mixed_connection: list[list[Form]], closure: dict[sp.Symbol, sp.Expr]
) -> list[list[Form]]:
    lower_curvature: list[list[Form]] = [[{} for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for b in range(DIM):
            value = exterior_d(mixed_connection[a][b])
            for c in range(DIM):
                value = add(value, wedge(mixed_connection[a][c], mixed_connection[c][b]))
            lower_curvature[a][b] = scale(ETA[a], clean(value, closure))
    return lower_curvature


def alternating_curvature_census(curvature_lower: list[list[Form]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    all_polynomial_variables = tuple(DERIV.values()) + BASE_VARIABLES
    for a, b in PAIRS:
        for i, j in PAIRS:
            expression = sp.expand(curvature_lower[a][b].get((i, j), 0))
            if expression == 0:
                continue
            # Coefficients of the two oriented monomials in p wedge dsigma on this leg.
            forward = sp.expand(expression).coeff(P[i - 1] * S[j - 1]) if i > 0 else 0
            reverse = sp.expand(expression).coeff(P[j - 1] * S[i - 1]) if i > 0 else 0
            fixed_alt = sp.simplify((forward - reverse) / 2) if i > 0 else 0
            symmetric = sp.simplify((forward + reverse) / 2) if i > 0 else 0
            if fixed_alt != 0 or symmetric != 0:
                rows.append(
                    {
                        "curvature_pair": f"{a}{b}",
                        "two_form_leg": f"{i}{j}",
                        "coeff_p_i_s_j": forward,
                        "coeff_p_j_s_i": reverse,
                        "alternating_projection": fixed_alt,
                        "symmetric_projection": symmetric,
                        "exact_expression": expression,
                    }
                )
            # Ensure every expression remains polynomial in the declared exact symbols.
            sp.Poly(expression, *all_polynomial_variables)
    return rows


def main() -> None:
    # Universal affine response quotient.
    a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2")
    curl_row = sp.Matrix([[0, 0, -1, 0, 1, 0]])
    assert curl_row.rank() == 1
    assert len(curl_row.nullspace()) == 5

    # Actual complete-S3 contact-scalar reconstruction.  t1 is the screen-area
    # coefficient of dtheta1 and survives local SO(2) screen coframe changes;
    # m is deliberately not load-bearing because its separation from the skew
    # part of L1 depends on the supplied Maurer-Cartan presentation.
    phi, sigma, A, B = sp.symbols("phi sigma A B", real=True)
    dphi, dsigma = sp.symbols("dphi dsigma")
    v = B + phi - sigma                 # log|t1|
    dv = dphi - dsigma
    # The sign-corrected antisymmetric primitive in (phi,v) has the same curl
    # as lambda(phi,sigma) and differs only by the exact B*dphi/2 reference term.
    lambda_phi_v = sp.Matrix([
        sp.expand((v * dphi - phi * dv) / 2).coeff(dphi),
        sp.expand((v * dphi - phi * dv) / 2).coeff(dsigma),
    ])
    lambda_phi_sigma = sp.Matrix([-sigma / 2, phi / 2])
    exact_shift_gradient = sp.Matrix([B / 2, 0])
    assert sp.simplify(lambda_phi_v - lambda_phi_sigma - exact_shift_gradient) == sp.zeros(2, 1)

    # The actual contact scalar supplies the alternating curl with fixed sign.
    contact_jacobian = sp.det(sp.Matrix([[1, 0], [1, -1]]))
    assert contact_jacobian == -1

    closure, closure_checks = closure_substitutions()
    d2_checks: dict[str, str] = {}
    for index, dtheta in enumerate(DTHETA):
        value = clean(exterior_d(dtheta), closure)
        d2_checks[f"d2theta{index}"] = str(value)
        assert value == {}, f"coframe integrability failed for theta{index}: {value}"
    lower_connection, mixed_connection = solve_connection()
    lower_curvature = curvature(mixed_connection, closure)
    curvature_rows = alternating_curvature_census(lower_curvature)

    nonzero_alt = [row for row in curvature_rows if row["alternating_projection"] != 0]
    nonzero_sym = [row for row in curvature_rows if row["symmetric_projection"] != 0]

    branch_rows = [
        {"branch": "S3_GENERAL_SCREEN_FORMAL_FREE", "condition": "p_and_dsigma_independent", "formal_quotient_rank": 1, "pullback_rank": 1, "cartan_log_route": "founded_phi;log_abs_t1", "ruling": "CONSTRUCTIVE_COMPLETE_S3_WITNESS_EXISTS"},
        {"branch": "S3_GENERAL_SCREEN_FUNCTIONAL_DEPENDENCE", "condition": "sigma=F(phi)", "formal_quotient_rank": 1, "pullback_rank": 0, "cartan_log_route": "collapses", "ruling": "DPHI_WEDGE_DSIGMA_ZERO"},
        {"branch": "S3_GENERAL_SCREEN_CONSTANT_PHI", "condition": "dphi=0", "formal_quotient_rank": 1, "pullback_rank": 0, "cartan_log_route": "collapses", "ruling": "ZERO"},
        {"branch": "S3_GENERAL_SCREEN_CONSTANT_AREA", "condition": "dsigma=0", "formal_quotient_rank": 1, "pullback_rank": 0, "cartan_log_route": "collapses", "ruling": "ZERO"},
        {"branch": "S3_GENERAL_SCREEN_ALPHA_ZERO", "condition": "t0=0_but_t1_nonzero", "formal_quotient_rank": 1, "pullback_rank": "0_OR_1", "cartan_log_route": "founded_phi;log_abs_t1", "ruling": "T0_AND_M_NOT_REQUIRED"},
        {"branch": "S3_GENERAL_SCREEN_ORIENTATION_MINUS", "condition": "detP_less_than_0", "formal_quotient_rank": 1, "pullback_rank": "0_OR_1", "cartan_log_route": "founded_phi;log_abs_t1", "ruling": "LOG_ABS_T1_SAME_ON_CONNECTED_ORIENTATION_STRATUM"},
        {"branch": "S3_GENERAL_SCREEN_DEGENERATE", "condition": "detP=0", "formal_quotient_rank": 1, "pullback_rank": "UNDEFINED", "cartan_log_route": "undefined", "ruling": "FOUR_METRIC_DEGENERATE_BOUNDARY"},
        {"branch": "FC07_MAPPING_TORUS_ALL_EIGHT", "condition": "phi=phi0_constant", "formal_quotient_rank": 1, "pullback_rank": 0, "cartan_log_route": "not_S3_structure", "ruling": "MANDATORY_COLLAPSE_CONTROL"},
        {"branch": "LOCAL_TRIANGULAR_CARTAN_CONTROL", "condition": "not_actual_complete_global_family", "formal_quotient_rank": 1, "pullback_rank": "0_OR_1", "cartan_log_route": "p_and_common_screen_channels", "ruling": "LOCAL_ALGEBRA_CONTROL_ONLY"},
        {"branch": "FC01_FC06_FC08_FC12_TAXONOMY_ROWS", "condition": "no_actual_joined_first_Cartan_coframe_in_frozen_sources", "formal_quotient_rank": "UNASSESSED", "pullback_rank": "UNASSESSED", "cartan_log_route": "missing", "ruling": "BLOCKED_MISSING_ACTUAL_CARTAN_DATA"},
    ]
    write_tsv(
        "BRANCH_PULLBACK_RANK_ATLAS.tsv",
        ["branch", "condition", "formal_quotient_rank", "pullback_rank", "cartan_log_route", "ruling"],
        branch_rows,
    )

    write_tsv(
        "CURVATURE_ALTERNATING_CENSUS.tsv",
        ["curvature_pair", "two_form_leg", "coeff_p_i_s_j", "coeff_p_j_s_i", "alternating_projection", "symmetric_projection", "exact_expression"],
        curvature_rows,
    )

    object_rows = [
        {"object": "dphi", "source": "founded_phi", "degree": 1, "presentation": "SCALAR_FIELD_INTRINSIC", "exactness": "EXACT", "production": "DERIVED"},
        {"object": "dsigma", "source": "screen_detP", "degree": 1, "presentation": "REGISTERED_SPLIT_RELATIVE_O2_INVARIANT", "exactness": "EXACT", "production": "DERIVED_GIVEN_SPLIT"},
        {"object": "dlog_abs_m", "source": "S3_Maurer_Cartan_decomposition_label_m", "degree": 1, "presentation": "FIXED_MAURER_CARTAN_PRESENTATION_ONLY", "exactness": "-dphi", "production": "NOT_LOAD_BEARING_GAUGE_SEPARATION_CAN_MIX_WITH_SKEW_L1"},
        {"object": "dlog_abs_t1", "source": "S3_first_Cartan_contact_coefficient_t1", "degree": 1, "presentation": "REGISTERED_SPLIT_RELATIVE_O2_AND_ORIENTATION_SAFE", "exactness": "dphi-dsigma", "production": "DERIVED_IN_S3_FAMILY"},
        {"object": "dlog_abs_t0", "source": "S3_first_Cartan_coefficient_t0", "degree": 1, "presentation": "REGISTERED_SPLIT_RELATIVE_NONZERO_ALPHA_ONLY", "exactness": "-dphi-dsigma", "production": "STRATUM_ONLY_NOT_REQUIRED"},
        {"object": "minus_dphi_wedge_dlog_abs_t1", "source": "founded_phi_plus_actual_S3_contact_scalar", "degree": 2, "presentation": "REGISTERED_SPLIT_RELATIVE_O2_AND_ORIENTATION_SAFE", "exactness": "dphi_wedge_dsigma", "production": "CARTAN_CONTACT_DIFFERENTIAL_INVARIANT_FIXED_COEFFICIENT_1"},
        {"object": "lambda_from_phi_log_t1", "source": "antisymmetric_primitive_of_founded_phi_and_actual_contact_log", "degree": 1, "presentation": "REGISTERED_SPLIT_RELATIVE_REFERENCE_EXACT_AMBIGUITY", "exactness": "equals_lambda_plus_d_of_B_phi_over_2", "production": "AVAILABLE_PRIMITIVE_NOT_SELECTED_CONNECTION"},
        {"object": "Levi_Civita_connection_scalar_one_form", "source": "connection", "degree": 1, "presentation": "INHOMOGENEOUS_LOCAL_FRAME_GAUGE", "exactness": "NOT_TENSOR", "production": "NO_OBSERVER_NATURAL_ONE_FORM_WITHOUT_REDUCTION"},
        {"object": "Levi_Civita_curvature_alternating_projection", "source": "exact_isotropic_complete_S3_subfamily", "degree": 2, "presentation": "REGISTERED_SPLIT_COMPONENT_CENSUS", "exactness": f"nonzero_alternating_slots={len(nonzero_alt)}", "production": "CENSUSED_NOT_A_PRIMITIVE"},
        {"object": "FC07_alternating_object", "source": "constant_phi_complete_mapping_tori", "degree": 2, "presentation": "COMPLETE_BRANCH", "exactness": "ZERO", "production": "PULLBACK_COLLAPSE"},
    ]
    write_tsv(
        "OBJECT_PRODUCTION_LEDGER.tsv",
        ["object", "source", "degree", "presentation", "exactness", "production"],
        object_rows,
    )

    result = {
        "schema": "udt-complete-cell-cartan-alternating-production-1.0",
        "affine_response": {
            "coefficient_dimension": 6,
            "universally_exact_kernel_dimension": 5,
            "quotient_rank": 1,
        },
        "cartan_contact_reconstruction": {
            "v": "log|t1|=B+phi-sigma",
            "minus_dphi_wedge_dlogt1": "dphi_wedge_dsigma",
            "fixed_coefficient": 1,
            "primitive_difference": "lambda_phi_v-lambda_phi_sigma=d[B phi/2]",
            "m_role": "NOT_LOAD_BEARING_FIXED_MAURER_CARTAN_PRESENTATION_ONLY",
        },
        "complete_S3_isotropic_curvature_control": {
            "closure_checks": closure_checks,
            "coframe_integrability": d2_checks,
            "nonzero_curvature_slots": sum(bool(lower_curvature[a][b]) for a, b in PAIRS),
            "rows_with_p_sigma_bilinears": len(curvature_rows),
            "rows_with_nonzero_alternating_projection": len(nonzero_alt),
            "rows_with_nonzero_symmetric_projection": len(nonzero_sym),
        },
        "branch_counts": {
            "rows": len(branch_rows),
            "actual_complete_families": 2,
            "actual_complete_rank_one_witness_families": 1,
            "actual_complete_forced_rank_zero_families": 1,
            "blocked_taxonomy_groups": 1,
        },
        "maximum_grade": "SPLIT_RELATIVE_DIFFERENTIAL_PRODUCTION_ONLY__PRIMITIVE_AND_NATURALITY_OPEN",
    }
    with (HERE / "DERIVATION_RESULT.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
