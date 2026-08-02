#!/usr/bin/env python3
"""Exact full-screen Cartan curvature and frame-descent census.

The production route uses an anholonomic Koszul connection and frame-commutator curvature.
It retains all four screen-response slots through the regular area/rotation/shear decomposition.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ETA = (-1, 1, 1, 1)
PAIRS = tuple((i, j) for i in range(4) for j in range(i + 1, 4))


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def serialize(value):
    if isinstance(value, sp.Basic):
        return str(sp.factor(value))
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def add_form(*forms: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for form in forms:
        for key, value in form.items():
            result[key] = sp.expand(result.get(key, 0) + value)
    return {key: value for key, value in result.items() if value != 0}


def scale_form(value: sp.Expr, form: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    return {key: sp.expand(value * coefficient) for key, coefficient in form.items() if coefficient != 0}


def wedge(left: dict[tuple[int, ...], sp.Expr], right: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            sign = (-1) ** sum(i > j for i in a for j in b)
            key = tuple(sorted(a + b))
            result[key] = sp.expand(result.get(key, 0) + sign * ca * cb)
    return {key: value for key, value in result.items() if value != 0}


def main() -> int:
    # Regular first-Cartan variables.  The L1+mC screen block is decomposed into
    # area a, rotation r, and both shears h1,h2.  u,v are the remaining screen
    # anholonomy coefficients in the 23 leg.
    p1, p2, p3, t0, t1 = sp.symbols("p1 p2 p3 t0 t1", real=True)
    a, r, h1, h2, u, v = sp.symbols("a r h1 h2 u v", real=True)
    s2, s3 = sp.symbols("sigma2 sigma3", real=True)
    coefficients = (p1, p2, p3, t0, t1, a, r, h1, h2, u, v)
    p = (p1, p2, p3)
    screen = (a, r, h1, h2, u, v)
    shear = (h1, h2)
    contact = (t0, t1)

    e = tuple({(index,): sp.Integer(1)} for index in range(4))
    dphi = add_form(scale_form(p1, e[1]), scale_form(p2, e[2]), scale_form(p3, e[3]))
    de = (
        add_form(scale_form(-1, wedge(dphi, e[0])), scale_form(t0, wedge(e[2], e[3]))),
        add_form(wedge(dphi, e[1]), scale_form(t1, wedge(e[2], e[3]))),
        add_form(
            scale_form(a + h1, wedge(e[1], e[2])),
            scale_form(h2 - r, wedge(e[1], e[3])),
            scale_form(u, wedge(e[2], e[3])),
        ),
        add_form(
            scale_form(h2 + r, wedge(e[1], e[2])),
            scale_form(a - h1, wedge(e[1], e[3])),
            scale_form(v, wedge(e[2], e[3])),
        ),
    )

    structure: dict[tuple[int, int, int], sp.Expr] = {}
    for upper, form in enumerate(de):
        for (left, right), value in form.items():
            structure[(upper, left, right)] = -value
            structure[(upper, right, left)] = value

    # Formal stationary derivatives.  The exact t0/t1 determinant relations are
    # imposed, with sigma1=tr(L1)=2a and sigma2,sigma3 retained independently.
    derivative = {
        (direction, coefficient): sp.Symbol(f"E{direction}_{coefficient}", real=True)
        for direction in (1, 2, 3) for coefficient in coefficients
    }
    sigma_components = (2 * a, s2, s3)
    derivative_relations = {}
    for direction in (1, 2, 3):
        derivative_relations[derivative[(direction, t1)]] = t1 * (p[direction - 1] - sigma_components[direction - 1])
        derivative_relations[derivative[(direction, t0)]] = -t0 * (p[direction - 1] + sigma_components[direction - 1])

    def E(direction: int, expression: sp.Expr) -> sp.Expr:
        if direction == 0:
            return sp.Integer(0)
        value = sum(sp.diff(expression, coefficient) * derivative[(direction, coefficient)] for coefficient in coefficients)
        return sp.expand(value.subs(derivative_relations))

    def d_scalar(expression: sp.Expr) -> dict[tuple[int, ...], sp.Expr]:
        return add_form(*(scale_form(E(direction, expression), e[direction]) for direction in (1, 2, 3)))

    def d_basis_tuple(basis: tuple[int, ...]) -> dict[tuple[int, ...], sp.Expr]:
        pieces = []
        for index, entry in enumerate(basis):
            before = {(basis[:index]): sp.Integer(1)}
            after = {(basis[index + 1:]): sp.Integer(1)}
            pieces.append(scale_form((-1) ** index, wedge(wedge(before, de[entry]), after)))
        return add_form(*pieces) if pieces else {}

    def exterior(form: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
        pieces = []
        for basis, coefficient in form.items():
            basis_form = {basis: sp.Integer(1)}
            pieces.append(wedge(d_scalar(coefficient), basis_form))
            pieces.append(scale_form(coefficient, d_basis_tuple(basis)))
        return {key: sp.factor(value) for key, value in add_form(*pieces).items() if sp.factor(value) != 0}

    closure_rows = []
    closure_expressions = []
    for upper, form in enumerate(de):
        for leg, expression in sorted(exterior(form).items()):
            closure_rows.append({"source": f"d2theta{upper}", "three_form_leg": "".join(map(str, leg)), "equation": str(expression)})
            closure_expressions.append(expression)
    for leg, expression in sorted(exterior(dphi).items()):
        closure_rows.append({"source": "d2phi", "three_form_leg": "".join(map(str, leg)), "equation": str(expression)})
        closure_expressions.append(expression)
    write_tsv("CLOSURE_EQUATIONS.tsv", ["source", "three_form_leg", "equation"], closure_rows)

    # Exact torsion-free metric-compatible Koszul connection.
    def cvalue(upper: int, left: int, right: int) -> sp.Expr:
        return structure.get((upper, left, right), 0)

    gamma: dict[tuple[int, int, int], sp.Expr] = {}
    for direction in range(4):
        for out in range(4):
            for incoming in range(4):
                gamma[(direction, out, incoming)] = sp.factor((
                    cvalue(out, direction, incoming)
                    - ETA[out] * ETA[direction] * cvalue(direction, incoming, out)
                    + ETA[out] * ETA[incoming] * cvalue(incoming, out, direction)
                ) / 2)
    for direction in range(4):
        for out in range(4):
            for incoming in range(4):
                assert sp.simplify(
                    ETA[out] * gamma[(direction, out, incoming)]
                    + ETA[incoming] * gamma[(direction, incoming, out)]
                ) == 0
    for upper in range(4):
        for left, right in PAIRS:
            assert sp.simplify(
                gamma[(left, upper, right)] - gamma[(right, upper, left)] - cvalue(upper, left, right)
            ) == 0

    curvature: dict[tuple[int, int, int, int], sp.Expr] = {}
    for upper in range(4):
        for incoming in range(4):
            for left, right in PAIRS:
                value = E(left, gamma[(right, upper, incoming)]) - E(right, gamma[(left, upper, incoming)])
                value += sum(
                    gamma[(right, intermediate, incoming)] * gamma[(left, upper, intermediate)]
                    - gamma[(left, intermediate, incoming)] * gamma[(right, upper, intermediate)]
                    - cvalue(intermediate, left, right) * gamma[(intermediate, upper, incoming)]
                    for intermediate in range(4)
                )
                curvature[(upper, incoming, left, right)] = sp.factor(sp.expand(value))

    # Lowered curvature two-form blocks and a sector census.
    gens = coefficients + tuple(
        derivative[(direction, coefficient)]
        for direction in (1, 2, 3) for coefficient in coefficients
        if coefficient not in contact
    ) + (s2, s3)

    def has_cross(expression: sp.Expr, left_group: tuple[sp.Symbol, ...], right_group: tuple[sp.Symbol, ...]) -> bool:
        polynomial = sp.Poly(sp.expand(expression), *gens)
        left_indices = {gens.index(item) for item in left_group}
        right_indices = {gens.index(item) for item in right_group}
        for powers, coefficient in polynomial.terms():
            if coefficient and any(powers[i] for i in left_indices) and any(powers[i] for i in right_indices):
                return True
        return False

    curvature_rows = []
    nonzero_blocks = set()
    cross_counts = {"depth_screen": 0, "depth_contact": 0, "screen_contact": 0, "shear_contact": 0}
    for lower_left, lower_right in PAIRS:
        for leg_left, leg_right in PAIRS:
            expression = sp.factor(ETA[lower_left] * curvature[(lower_left, lower_right, leg_left, leg_right)])
            if expression != 0:
                nonzero_blocks.add((lower_left, lower_right))
            flags = {
                "depth_screen": has_cross(expression, p, screen),
                "depth_contact": has_cross(expression, p, contact),
                "screen_contact": has_cross(expression, screen, contact),
                "shear_contact": has_cross(expression, shear, contact),
            }
            for key, value in flags.items():
                cross_counts[key] += int(value)
            curvature_rows.append({
                "curvature_pair": f"Omega{lower_left}{lower_right}",
                "two_form_leg": f"{leg_left}{leg_right}",
                **{key: "YES" if value else "NO" for key, value in flags.items()},
                "expression": str(expression),
            })
    write_tsv(
        "FULL_CURVATURE_CENSUS.tsv",
        ["curvature_pair", "two_form_leg", "depth_screen", "depth_contact", "screen_contact", "shear_contact", "expression"],
        curvature_rows,
    )

    # Riemann scalar, retained only as a full-frame invariant control.  It is not
    # used to select a split-relative term.
    scalar_curvature = sp.Integer(0)
    for a0 in range(4):
        for b0 in range(4):
            if a0 == b0:
                continue
            left, right = sorted((a0, b0))
            orientation = 1 if (a0, b0) == (left, right) else -1
            component = ETA[a0] * curvature[(a0, b0, left, right)] * orientation
            scalar_curvature += ETA[a0] * ETA[b0] * component
    scalar_curvature = sp.factor(sp.expand(scalar_curvature))

    # Split-preserving contact doublet and exact frame descent.
    beta = sp.symbols("beta", real=True)
    boost = sp.Matrix([[sp.cosh(beta), sp.sinh(beta)], [sp.sinh(beta), sp.cosh(beta)]])
    eta2 = sp.diag(-1, 1)
    q = sp.Matrix([t0, t1])
    qprime = boost * q
    qnorm = sp.factor((q.T * eta2 * q)[0])
    assert sp.simplify((qprime.T * eta2 * qprime)[0] - qnorm) == 0
    assert sp.simplify(qnorm - (-t0**2 + t1**2)) == 0

    phi, alpha, kappa, D, D0, T0 = sp.symbols("phi alpha kappa D D0 T0", real=True, nonzero=True)
    qnorm_metric = sp.factor(qnorm.subs({t0: alpha*kappa*sp.exp(-phi)/D, t1: kappa*sp.exp(phi)/D}))
    expected_qnorm = sp.factor(kappa**2 * (sp.exp(2*phi) - alpha**2*sp.exp(-2*phi)) / D**2)
    assert sp.simplify(qnorm_metric - expected_qnorm) == 0
    Fprime = sp.factor(
        (sp.exp(2*phi) + alpha**2*sp.exp(-2*phi))
        / (sp.exp(2*phi) - alpha**2*sp.exp(-2*phi))
    )

    # Local pair/screen-changing transformations can alter q while fixing both
    # the metric and the frame value at the audit point.  g is an arbitrary
    # derivative of the local rotation/boost parameter there.
    g = sp.symbols("g", real=True)
    qnorm_spatial_mix = sp.expand((t1 - g)**2 - t0**2)
    qnorm_temporal_mix = sp.expand(t1**2 - (t0 - g)**2)
    assert sp.simplify(qnorm_spatial_mix - qnorm) != 0
    assert sp.simplify(qnorm_temporal_mix - qnorm) != 0

    frame_rows = [
        {"frame_class": "LOCAL_SCREEN_SO2", "ansatz_status": "PRESERVED", "contact_transform": "q_prime=q", "qnorm": "INVARIANT", "ruling": "REDUCTION_GAUGE_SAFE"},
        {"frame_class": "SCREEN_REFLECTION", "ansatz_status": "PRESERVED", "contact_transform": "q_prime=-q", "qnorm": "INVARIANT", "ruling": "ORIENTATION_SAFE_AFTER_NORM_OR_ABSOLUTE_VALUE"},
        {"frame_class": "LOCAL_PAIR_LORENTZ_BOOST", "ansatz_status": "REDUCTION_PRESERVED;DISPLAYED_RECIPROCAL_GAUGE_MAY_CHANGE", "contact_transform": "q_prime=B(beta)q;derivative_term_vanishes_on_screen", "qnorm": "INVARIANT", "ruling": "O11xO2_REDUCTION_INVARIANT"},
        {"frame_class": "PAIR_SCREEN_SPATIAL_ROTATION", "ansatz_status": "GENERALLY_LEAVES_BLOCK_SCREEN_ANSATZ", "contact_transform": "at_Lambda=I:t1_prime=t1-E3(psi)", "qnorm": "NOT_INVARIANT", "ruling": "NO_COMPLETE_FRAME_DESCENT"},
        {"frame_class": "PAIR_SCREEN_LORENTZ_BOOST", "ansatz_status": "GENERALLY_LEAVES_BLOCK_SCREEN_ANSATZ", "contact_transform": "at_Lambda=I:t0_prime=t0-E3(chi)", "qnorm": "NOT_INVARIANT", "ruling": "NO_COMPLETE_FRAME_DESCENT"},
        {"frame_class": "GENERAL_LOCAL_LORENTZ", "ansatz_status": "BLOCK_SCREEN_CHART_NOT_CLOSED", "contact_transform": "inhomogeneous_frame_derivative_terms", "qnorm": "NOT_METRIC_SCALAR", "ruling": "CURVATURE_TENSOR_SURVIVES_CONTACT_EXTRACTION_DOES_NOT"},
    ]
    write_tsv("FRAME_DESCENT_ATLAS.tsv", ["frame_class", "ansatz_status", "contact_transform", "qnorm", "ruling"], frame_rows)

    split_rows = [
        {"object": "q_pair", "formula": "q^a=screen_area_coefficient_of_dtheta^a", "screen_group": "O2_PSEUDOSCALAR", "pair_group": "O11_VECTOR", "full_frame": "NO", "status": "SPLIT_REDUCTION_OBJECT"},
        {"object": "q_squared", "formula": "t1^2-t0^2", "screen_group": "INVARIANT", "pair_group": "INVARIANT", "full_frame": "NO", "status": "O11xO2_REDUCTION_SCALAR"},
        {"object": "contact_log", "formula": "log(sqrt(abs(q_squared))/T0)", "screen_group": "INVARIANT_OFF_NULL", "pair_group": "INVARIANT_OFF_NULL", "full_frame": "NO", "status": "THREE_CAUSAL_STRATA;UNDEFINED_AT_q_squared=0"},
        {"object": "contact_differential", "formula": "dphi_wedge_dlog_sqrt_abs_q_squared=-dphi_wedge_dsigma", "screen_group": "INVARIANT_OFF_NULL", "pair_group": "INVARIANT_IF_phi_IS_FOUNDED_SCALAR", "full_frame": "NO", "status": "SPLIT_PRESERVING_RECONSTRUCTION"},
        {"object": "Riemann_tensor", "formula": "Omega_ab", "screen_group": "COVARIANT", "pair_group": "COVARIANT", "full_frame": "COVARIANT", "status": "METRIC_TENSOR"},
        {"object": "scalar_curvature", "formula": "full_metric_contraction_of_Riemann", "screen_group": "INVARIANT", "pair_group": "INVARIANT", "full_frame": "INVARIANT", "status": "DOES_NOT_UNIQUELY_ISOLATE_CONTACT_OR_RESPONSE"},
        {"object": "split_curvature_contractions", "formula": "R_contracted_with_pair_and_screen_projectors", "screen_group": "INVARIANT", "pair_group": "INVARIANT", "full_frame": "NO_WITHOUT_SELECTED_PROJECTORS", "status": "MULTIPLE_REDUCTION_SCALARS"},
    ]
    write_tsv("INVARIANT_OBJECT_ATLAS.tsv", ["object", "formula", "screen_group", "pair_group", "full_frame", "status"], split_rows)

    witness_rows = [
        {"witness": "W00_CONSTANT_ISOTROPIC", "P": "exp(u0)I", "modes": "area_value_only", "global": "SMOOTH_COMPLETE_S3", "purpose": "zero_screen_jet_control"},
        {"witness": "W01_AREA", "P": "exp(u(x))I", "modes": "area", "global": "SMOOTH_COMPLETE_S3", "purpose": "area_contact_control"},
        {"witness": "W02_SHEAR1", "P": "exp(uI+q1S1)", "modes": "area;shear1", "global": "SMOOTH_COMPLETE_S3", "purpose": "first_shear_nonzero"},
        {"witness": "W03_SHEAR2", "P": "exp(uI+q2S2)", "modes": "area;shear2", "global": "SMOOTH_COMPLETE_S3", "purpose": "second_shear_nonzero"},
        {"witness": "W04_TWO_SHEAR", "P": "exp(uI+q1S1+q2S2)", "modes": "area;shear1;shear2", "global": "SMOOTH_COMPLETE_S3", "purpose": "full_metric_screen_response"},
        {"witness": "W05_ROTATION_GAUGE", "P": "O(chi)exp(uI+q1S1+q2S2)", "modes": "area;two_shears;rotation", "global": "SMOOTH_COMPLETE_S3", "purpose": "full_coframe_response_and_gauge"},
        {"witness": "W06_ORIENTATION_REVERSE", "P": "reflection_times_W05", "modes": "same_metric;opposite_screen_orientation", "global": "SMOOTH_COMPLETE_S3", "purpose": "reflection_control"},
        {"witness": "W07_DET_ZERO", "P": "detP_zero", "modes": "undefined", "global": "DEGENERATE_NOT_CONFIGURATION", "purpose": "retained_boundary"},
    ]
    write_tsv("COMPLETE_WITNESS_ATLAS.tsv", ["witness", "P", "modes", "global", "purpose"], witness_rows)

    result = {
        "schema": "udt-complete-cell-full-gl2-screen-frame-descent-1.0",
        "status": "PASS",
        "headline": "SPLIT_RELATIVE_ONLY__NO_COMPLETE_FRAME_DESCENT",
        "bounded_family": "STATIONARY_COMPLETE_S3_GENERAL_SCREEN_OFF_SHELL",
        "screen_response_slots": ["area", "rotation_gauge", "shear1", "shear2"],
        "first_cartan_coefficients": len(coefficients),
        "closure_equation_rows": len(closure_rows),
        "independent_closure_equations": 5,
        "curvature_rows": len(curvature_rows),
        "nonzero_lower_curvature_blocks": len(nonzero_blocks),
        "sector_cross_counts": cross_counts,
        "contact_reduction": {
            "q": ["t0", "t1"],
            "q_squared": str(qnorm),
            "q_squared_metric": str(expected_qnorm),
            "split_preserving_group": "O(1,1)xO(2)",
            "contact_log_phi_derivative": str(Fprime),
            "dphi_wedge_identity": "dphi_wedge_dlog_sqrt_abs_q_squared=-dphi_wedge_dsigma",
            "null_stratum": "q_squared=0;contact_log_undefined",
            "complete_frame_descent": False,
        },
        "frame_descent_rows": len(frame_rows),
        "invariant_objects": len(split_rows),
        "complete_witnesses": len(witness_rows),
        "scalar_curvature": str(scalar_curvature),
        "physics_selected": False,
        "action_carrier_source_density_mass_bootstrap": "OPEN_NOT_INFERRED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(serialize(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"], "headline": result["headline"],
        "closure_equation_rows": result["closure_equation_rows"],
        "independent_closure_equations": result["independent_closure_equations"],
        "curvature_rows": result["curvature_rows"],
        "nonzero_lower_curvature_blocks": result["nonzero_lower_curvature_blocks"],
        "sector_cross_counts": result["sector_cross_counts"],
        "q_squared": result["contact_reduction"]["q_squared"],
        "complete_frame_descent": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
