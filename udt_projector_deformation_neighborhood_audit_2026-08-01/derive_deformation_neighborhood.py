#!/usr/bin/env python3
"""Exact metric-led projector deformation-neighborhood derivation.

No action, carrier, bootstrap equation, or physics filter is used.  The
stationary complete-S3 first-jet Cartan system is rebuilt directly, and the
functional-neighborhood result follows from exact nonzero center margins plus
continuity in the stated finite-jet topology.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT_PAIR = ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27"
PARENT_PROJECTOR = ROOT / "udt_branchwise_projector_holonomy_census_2026-08-01"
HALF = sp.Rational(1, 2)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def general_screen_response() -> dict[str, object]:
    """Rebuild the pair-to-screen Cartan block and projector curvature."""

    p1, p2, p3, t0, t1, m = sp.symbols("p1 p2 p3 t0 t1 m", real=True)
    c11, c12, c21, c22 = sp.symbols("c11 c12 c21 c22", real=True)
    c = sp.Matrix([[c11, c12], [c21, c22]])
    ell = {
        direction: sp.Matrix(
            2,
            2,
            lambda row, column: sp.symbols(
                f"L{direction}{row + 1}{column + 1}", real=True
            ),
        )
        for direction in (1, 2, 3)
    }

    # Exterior coefficients d theta^upper = coefficient theta^left wedge theta^right.
    exterior: dict[tuple[int, int, int], sp.Expr] = {}

    def add(upper: int, left: int, right: int, value: sp.Expr) -> None:
        if left == right:
            return
        if left > right:
            left, right, value = right, left, -value
        exterior[(upper, left, right)] = sp.expand(
            exterior.get((upper, left, right), 0) + value
        )

    add(0, 1, 0, -p1)
    add(0, 2, 0, -p2)
    add(0, 3, 0, -p3)
    add(0, 2, 3, t0)
    add(1, 1, 1, p1)
    add(1, 2, 1, p2)
    add(1, 3, 1, p3)
    add(1, 2, 3, t1)
    for out in range(2):
        for direction in (1, 2, 3):
            for column in range(2):
                add(out + 2, direction, column + 2, ell[direction][out, column])
        for column in range(2):
            add(out + 2, 1, column + 2, m * c[out, column])

    structure: dict[tuple[int, int, int], sp.Expr] = {}
    for (upper, left, right), coefficient in exterior.items():
        structure[(upper, left, right)] = -coefficient
        structure[(upper, right, left)] = coefficient
    signs = (-1, 1, 1, 1)

    def lower(out: int, left: int, right: int) -> sp.Expr:
        return signs[out] * structure.get((out, left, right), 0)

    def gamma(direction: int, acted: int, out: int) -> sp.Expr:
        return sp.expand(
            HALF
            * (
                lower(out, direction, acted)
                - lower(direction, acted, out)
                + lower(acted, out, direction)
            )
        )

    vectors = {
        direction: sp.Matrix([gamma(direction, 1, 2), gamma(direction, 1, 3)])
        for direction in range(4)
    }
    expected = {
        0: sp.Matrix([0, 0]),
        1: sp.Matrix([-p2, -p3]),
        2: sp.Matrix(
            [
                ell[1][0, 0] + c11 * m,
                HALF
                * (
                    ell[1][0, 1]
                    + ell[1][1, 0]
                    + (c12 + c21) * m
                    + t1
                ),
            ]
        ),
        3: sp.Matrix(
            [
                HALF
                * (
                    ell[1][0, 1]
                    + ell[1][1, 0]
                    + (c12 + c21) * m
                    - t1
                ),
                ell[1][1, 1] + c22 * m,
            ]
        ),
    }
    for direction in range(4):
        assert sp.simplify(vectors[direction] - expected[direction]) == sp.zeros(2, 1)

    def wedge_scalar(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
        return sp.factor(left[0] * right[1] - left[1] * right[0])

    response = {
        f"W{left}{right}": wedge_scalar(vectors[left], vectors[right])
        for left in range(4)
        for right in range(left + 1, 4)
    }
    assert response["W01"] == response["W02"] == response["W03"] == 0
    return {
        "symbols": {
            "p1": p1,
            "p2": p2,
            "p3": p3,
            "t0": t0,
            "t1": t1,
            "m": m,
            "c11": c11,
            "c12": c12,
            "c21": c21,
            "c22": c22,
        },
        "C": c,
        "L": ell,
        "vectors": vectors,
        "response": response,
    }


def serialize(value: object) -> object:
    if isinstance(value, sp.MatrixBase):
        return [[str(sp.factor(value[i, j])) for j in range(value.cols)] for i in range(value.rows)]
    if isinstance(value, sp.Basic):
        return str(sp.factor(value))
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def main() -> int:
    algebra = general_screen_response()
    symbols = algebra["symbols"]
    response = algebra["response"]
    ell = algebra["L"]
    p1, p2, p3 = symbols["p1"], symbols["p2"], symbols["p3"]
    t1, m = symbols["t1"], symbols["m"]
    c11, c12, c21, c22 = (
        symbols["c11"],
        symbols["c12"],
        symbols["c21"],
        symbols["c22"],
    )

    lam, mu, nu = sp.symbols("lambda mu nu", real=True)
    north = {
        p1: sp.Rational(3, 50),
        p2: sp.Rational(1, 50),
        p3: sp.Rational(2, 50),
        t1: sp.Rational(-2),
        m: sp.Rational(-2),
        c11: 0,
        c12: -1,
        c21: 1,
        c22: 0,
    }
    generator = sp.Matrix([[lam + mu, nu], [nu, lam - mu]])
    for direction, derivative in (
        (1, sp.Rational(3, 50)),
        (2, sp.Rational(1, 50)),
        (3, sp.Rational(2, 50)),
    ):
        for row in range(2):
            for column in range(2):
                north[ell[direction][row, column]] = derivative * generator[row, column]

    symmetric_response = {
        key: sp.factor(value.subs(north)) for key, value in response.items()
    }
    expected_w23 = 1 + sp.Rational(9, 2500) * (lam**2 - mu**2 - nu**2)
    assert sp.simplify(symmetric_response["W23"] - expected_w23) == 0

    equal_screen = {mu: 0, nu: 0}
    equal_w23 = sp.factor(symmetric_response["W23"].subs(equal_screen))
    assert sp.simplify(equal_w23 - (1 + sp.Rational(9, 2500) * lam**2)) == 0
    assert sp.simplify(equal_w23 - 1 - (sp.Rational(3, 50) * lam) ** 2) == 0

    # Solve the complete north-event response wall without using a numerical search.
    zero_line = {
        lam: sp.Rational(5, 4) * nu + sp.Rational(25, 2),
        mu: -sp.Rational(3, 4) * nu - sp.Rational(125, 6),
    }
    for key in ("W12", "W13", "W23"):
        assert sp.simplify(symmetric_response[key].subs(zero_line)) == 0
    linear_jacobian = sp.Matrix(
        [symmetric_response["W12"], symmetric_response["W13"]]
    ).jacobian([lam, mu])
    assert sp.factor(linear_jacobian.det()) != 0
    assert sp.simplify(
        symmetric_response["W23"].subs(zero_line)
    ) == 0
    assert sp.simplify(
        sp.Matrix([symmetric_response["W12"], symmetric_response["W13"]]).subs(zero_line)
    ) == sp.zeros(2, 1)
    shear1_zero_point = {
        lam: sp.Rational(25, 2), mu: sp.Rational(-125, 6), nu: 0
    }
    shear2_zero_point = {
        lam: sp.Rational(-200, 9), mu: 0, nu: sp.Rational(-250, 9)
    }
    for point in (shear1_zero_point, shear2_zero_point):
        for key in ("W12", "W13", "W23"):
            assert sp.simplify(symmetric_response[key].subs(point)) == 0

    parent_centers = {
        row["branch_id"]: row
        for row in read_tsv(PARENT_PROJECTOR / "TWISTED_S3_RELATIVE_CURVATURE.tsv")
    }
    parent_certificates = {
        row["candidate_id"]: row
        for row in read_tsv(PARENT_PAIR / "CANDIDATE_OUTCOMES.tsv")
    }
    center_lambdas = {
        "C01": sp.Rational(-2),
        "C02": sp.Rational(-1),
        "C03": sp.Rational(0),
        "C04": sp.Rational(1, 2),
        "C05": sp.Rational(1),
        "C06": sp.Rational(2),
    }
    center_rows: list[dict[str, object]] = []
    for center, value in center_lambdas.items():
        computed = sp.factor(equal_w23.subs(lam, value))
        expected = sp.Rational(parent_centers[center]["relative_curvature_component_Q23_12"])
        determinant = sp.Rational(parent_certificates[center]["gradient_determinant"])
        assert computed == expected and computed > 0 and determinant != 0
        center_rows.append(
            {
                "center": center,
                "lambda": str(value),
                "clock_certificate_determinant": str(determinant),
                "certificate_nonzero": "YES",
                "relative_curvature_W23": str(computed),
                "response_nonzero": "YES",
                "functional_neighborhood": "OPEN_IN_C3_STATIONARY_PHI_P_TOPOLOGY",
                "global_gate": "OPEN_BY_COMPACT_C0_MARGIN",
                "maximum_status": "DERIVED_CONDITIONAL_ON_REGISTERED_OFFSHELL_FAMILY",
            }
        )
    write_tsv("CENTER_NEIGHBORHOOD_ATLAS.tsv", center_rows)

    subfamily_rows = [
        {
            "family": "E01_EQUAL_SCREEN",
            "parameters": "lambda_real",
            "W12": str(symmetric_response["W12"].subs(equal_screen)),
            "W13": str(symmetric_response["W13"].subs(equal_screen)),
            "W23": str(equal_w23),
            "north_event_zero_locus": "EMPTY_BECAUSE_W23_GE_1",
            "classification": "NONZERO_FOR_ALL_REAL_LAMBDA_AT_P00",
        },
        {
            "family": "E02_ONE_SHEAR_S1",
            "parameters": "lambda;mu;nu=0",
            "W12": str(symmetric_response["W12"].subs(nu, 0)),
            "W13": str(symmetric_response["W13"].subs(nu, 0)),
            "W23": str(symmetric_response["W23"].subs(nu, 0)),
            "north_event_zero_locus": "lambda=25/2;mu=-125/6",
            "classification": "ONE_ISOLATED_ZERO_POINT_RETAINED_AT_P00",
        },
        {
            "family": "E03_ONE_SHEAR_S2",
            "parameters": "lambda;nu;mu=0",
            "W12": str(symmetric_response["W12"].subs(mu, 0)),
            "W13": str(symmetric_response["W13"].subs(mu, 0)),
            "W23": str(symmetric_response["W23"].subs(mu, 0)),
            "north_event_zero_locus": "lambda=-200/9;nu=-250/9",
            "classification": "ONE_ISOLATED_ZERO_POINT_RETAINED_AT_P00",
        },
        {
            "family": "E04_TWO_SHEAR_SYMMETRIC",
            "parameters": "lambda;mu;nu",
            "W12": str(symmetric_response["W12"]),
            "W13": str(symmetric_response["W13"]),
            "W23": str(symmetric_response["W23"]),
            "north_event_zero_locus": "lambda=5nu/4+25/2;mu=-3nu/4-125/6",
            "classification": "ONE_AFFINE_ZERO_LINE_RETAINED_AT_P00",
        },
    ]
    write_tsv("EXACT_SUBFAMILY_ATLAS.tsv", subfamily_rows)

    local_rows = [
        {
            "object": key,
            "exact_formula": str(sp.factor(value)),
            "zero_meaning": (
                "ONE_SCREEN_CURVATURE_COMPONENT_ZERO"
                if key in {"W12", "W13", "W23"}
                else "IDENTICALLY_ZERO_FROM_STATIONARITY_AND_INTRINSIC_FRAME"
            ),
            "complete_gate": "W12=W13=W23=0_AT_EVENT",
        }
        for key, value in response.items()
    ]
    write_tsv("LOCAL_RESPONSE_FORMULAS.tsv", local_rows)

    openness_rows = [
        {
            "gate": "CLOCK_CERTIFICATE",
            "center_fact": "det(dI1,dI2,dI3)_P00_nonzero_all_C01_C06",
            "dependency": "metric_C3_jet_at_P00",
            "neighborhood": "OPEN_IN_STATIONARY_C3_CONFIGURATION_TOPOLOGY",
            "wall": "det_gradient_zero_is_certificate_wall_only",
        },
        {
            "gate": "TWIST_SELECTED_RULER",
            "center_fact": "a*kappa_nonzero",
            "dependency": "a*kappa*exp(-3phi)/detP",
            "neighborhood": "EXACT_THROUGHOUT_SMOOTH_GL2_FAMILY_WITH_a_kappa_nonzero",
            "wall": "a=0_or_kappa=0_or_detP=0",
        },
        {
            "gate": "RANK1_PROJECTOR_AND_RANK2_COMPLEMENT",
            "center_fact": "global_unoriented_ruler_line",
            "dependency": "algebraic_in_clock_and_ruler_lines",
            "neighborhood": "EXACT_WHERE_CLOCK_AND_RULER_GATES_HOLD",
            "wall": "loss_of_either_line",
        },
        {
            "gate": "GLOBAL_CONFIGURATION_AND_POSITIVE_SLICE",
            "center_fact": "compact_S3;detP_nonzero;exp(4phi)>a2",
            "dependency": "phi_P_C0_uniform_margins",
            "neighborhood": "OPEN_BY_COMPACTNESS_IN_C0_HENCE_C3",
            "wall": "detP=0_is_metric_wall;slice_equality_is_only_displayed_slice_wall",
        },
        {
            "gate": "NONZERO_RELATIVE_CURVATURE_SOMEWHERE",
            "center_fact": "W23_P00_nonzero_all_C01_C06",
            "dependency": "metric_projector_C1_jets_at_P00",
            "neighborhood": "OPEN_IN_C1_HENCE_C3",
            "wall": "all_event_components_zero_is_local_witness_wall_not_global_no_go",
        },
    ]
    write_tsv("FUNCTIONAL_OPENNESS_GATES.tsv", openness_rows)

    wall_rows = [
        {"wall": "SCREEN_RANK", "equation": "detP=0", "effect": "FOUR_METRIC_DEGENERATE", "overclaim_guard": "NOT_A_REGULAR_CONFIGURATION"},
        {"wall": "DISPLAYED_SLICE", "equation": "exp(4phi)=a^2", "effect": "t_constant_slice_degenerate", "overclaim_guard": "FOUR_METRIC_REMAINS_LORENTZIAN_IF_detP_nonzero"},
        {"wall": "TWIST_RULER", "equation": "a*kappa=0", "effect": "registered_twist_selector_vanishes", "overclaim_guard": "OTHER_RULER_SELECTORS_NOT_REFUTED"},
        {"wall": "CLOCK_CERTIFICATE", "equation": "det(dI1,dI2,dI3)=0_at_certificate_event", "effect": "three_invariant_sufficient_certificate_fails", "overclaim_guard": "INTRINSIC_CLOCK_MAY_STILL_EXIST"},
        {"wall": "LOCAL_RESPONSE_CERTIFICATE", "equation": "W12=W13=W23=0_at_P00", "effect": "relative_projector_curvature_zero_at_registered_event", "overclaim_guard": "MAY_BE_NONZERO_ELSEWHERE"},
        {"wall": "SYMMETRIC_TWO_SHEAR_P00", "equation": "lambda=5nu/4+25/2;mu=-3nu/4-125/6", "effect": "complete_local_response_zero_at_P00", "overclaim_guard": "OFFSHELL_SUBFAMILY_WALL_NOT_DYNAMICS"},
        {"wall": "POLAR_SHEAR_AXIS", "equation": "v=0_in_polar_screen_chart", "effect": "beta_coordinate_undefined", "overclaim_guard": "REGULAR_logH_q1_q2_CHART_HAS_BOTH_SHEARS"},
    ]
    write_tsv("DEGENERACY_WALL_ATLAS.tsv", wall_rows)

    result = {
        "schema": "udt.projector_deformation_neighborhood.derivation.v1",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "center_count": len(center_rows),
        "all_centers_clock_certificate_nonzero": True,
        "all_centers_relative_curvature_nonzero": True,
        "functional_open_neighborhood_count": len(center_rows),
        "equal_screen_W23": str(equal_w23),
        "equal_screen_global_minimum": "1",
        "symmetric_two_shear_P00_zero_locus": {
            "lambda": "5*nu/4+25/2",
            "mu": "-3*nu/4-125/6",
            "nu": "free_real",
        },
        "general_first_jet_complete_zero_condition": "W12=W13=W23=0",
        "external_semantic_review": "OPEN_NOT_AUTHORIZED",
        "action_used": False,
        "carrier_used": False,
        "bootstrap_used": False,
        "on_shell_claimed": False,
        "maximum_conclusion": (
            "EACH_C01_C06_CENTER_HAS_AN_OPEN_STATIONARY_COMPLETE_OFFSHELL_"
            "CONFIGURATION_NEIGHBORHOOD_WITH_INTRINSIC_PROJECTOR_GATES_AND_"
            "NONZERO_RELATIVE_CURVATURE_SOMEWHERE"
        ),
    }
    compact_algebra = {
        "projector_connection_vectors": {
            str(direction): [str(sp.expand(entry)) for entry in vector]
            for direction, vector in algebra["vectors"].items()
        },
        "general_relative_curvature_scalars": {
            key: str(value) for key, value in response.items()
        },
        "symmetric_two_shear_north_specialization": {
            key: str(value) for key, value in symmetric_response.items()
        },
    }
    (HERE / "GENERAL_RESPONSE_ALGEBRA.json").write_text(
        json.dumps(compact_algebra, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
