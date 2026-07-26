#!/usr/bin/env python3
"""Exact algebra for the UDT metric-orchestra common-domain rehearsal."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
FIELDS = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")
RATE_NAMES = tuple(f"d{direction}_{field}" for direction in ("0", "1") for field in FIELDS)


def require(name: str, condition: object, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def coframe(values: dict[str, sp.Expr]) -> sp.Matrix:
    phi = values["phi"]
    sigma = values["sigma"]
    alpha = values["alpha"]
    k = values["k"]
    s10, s11, s20, s21 = (values[name] for name in ("S10", "S11", "S20", "S21"))
    r = sp.exp(sigma / 2 - alpha)
    q = sp.exp(sigma / 2 + alpha)
    return sp.Matrix([
        [sp.exp(-phi), 0, 0, 0],
        [0, sp.exp(phi), 0, 0],
        [r * (s10 + k * s20), r * (s11 + k * s21), r, k * r],
        [q * s20, q * s21, 0, q],
    ])


def metric(values: dict[str, sp.Expr]) -> sp.Matrix:
    eta = sp.diag(-1, 1, 1, 1)
    E = coframe(values)
    return sp.simplify(E.T * eta * E)


def coframe_field_two_jet(symbols: dict[str, sp.Symbol]) -> sp.Matrix:
    """Second-order Taylor coframe with exact field jets at the neutral point."""
    phi, sigma, alpha, k, s10, s11, s20, s21 = (symbols[name] for name in FIELDS)
    a = sigma / 2 - alpha
    b = sigma / 2 + alpha
    em = 1 - phi + phi**2 / 2
    ep = 1 + phi + phi**2 / 2
    r = 1 + a + a**2 / 2
    q = 1 + b + b**2 / 2
    return sp.Matrix([
        [em, 0, 0, 0],
        [0, ep, 0, 0],
        [s10 + k * s20 + a * s10, s11 + k * s21 + a * s11,
         r, k + a * k],
        [s20 + b * s20, s21 + b * s21, 0, q],
    ])


def curvature_at_origin(values: dict[str, sp.Expr], x0: sp.Symbol, x1: sp.Symbol) -> sp.Expr:
    """Scalar curvature at x0=x1=0 from exact metric first/second jets."""
    g = metric(values)
    origin = {x0: 0, x1: 0}
    coordinates = (x0, x1, None, None)
    g0 = sp.simplify(g.subs(origin))
    dg: list[sp.Matrix] = []
    for coordinate in coordinates:
        dg.append(sp.zeros(4) if coordinate is None else sp.simplify(g.diff(coordinate).subs(origin)))
    ddg: list[list[sp.Matrix]] = []
    for first in coordinates:
        row: list[sp.Matrix] = []
        for second in coordinates:
            if first is None or second is None:
                row.append(sp.zeros(4))
            else:
                row.append(sp.simplify(g.diff(first, second).subs(origin)))
        ddg.append(row)
    return scalar_curvature_from_jets(g0, dg, ddg)


def curvature_tensors_from_jets(
    g0: sp.Matrix, dg: list[sp.Matrix], ddg: list[list[sp.Matrix]]
) -> tuple[sp.Matrix, sp.Expr]:
    """Return exact Ricci tensor and scalar from coordinate metric two-jets."""
    inv = g0.inv()
    dinv = [-inv * item * inv for item in dg]

    gamma = [[[
        sp.expand(sp.Rational(1, 2) * sum(
            inv[rho, s] * (dg[nu][s, mu] + dg[mu][s, nu] - dg[s][mu, nu])
            for s in range(4)
        ))
        for nu in range(4)] for mu in range(4)] for rho in range(4)]

    dgamma = [[[[
        sp.expand(sp.Rational(1, 2) * sum(
            dinv[lam][rho, s] * (dg[nu][s, mu] + dg[mu][s, nu] - dg[s][mu, nu])
            + inv[rho, s] * (
                ddg[lam][nu][s, mu] + ddg[lam][mu][s, nu] - ddg[lam][s][mu, nu]
            )
            for s in range(4)
        ))
        for nu in range(4)] for mu in range(4)] for rho in range(4)] for lam in range(4)]

    ricci = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            value = 0
            for rho in range(4):
                value += dgamma[rho][rho][mu][nu] - dgamma[nu][rho][mu][rho]
                for lam in range(4):
                    value += gamma[rho][rho][lam] * gamma[lam][mu][nu]
                    value -= gamma[rho][nu][lam] * gamma[lam][mu][rho]
            ricci[mu, nu] = sp.expand(value)
    scalar = sp.expand(sum(inv[mu, nu] * ricci[mu, nu]
                           for mu in range(4) for nu in range(4)))
    return ricci, scalar


def scalar_curvature_from_jets(
    g0: sp.Matrix, dg: list[sp.Matrix], ddg: list[list[sp.Matrix]]
) -> sp.Expr:
    return curvature_tensors_from_jets(g0, dg, ddg)[1]


def metric_field_jets(symbols: dict[str, sp.Symbol]) -> tuple[
    sp.Matrix, dict[str, sp.Matrix], dict[tuple[str, str], sp.Matrix]
]:
    """Metric value, first field derivatives, and field Hessian at zero."""
    eta = sp.diag(-1, 1, 1, 1)
    E_fields = coframe_field_two_jet(symbols)
    g_fields = sp.expand(E_fields.T * eta * E_fields)
    zero = {symbol: 0 for symbol in symbols.values()}
    g0 = g_fields.subs(zero)
    first = {
        field: g_fields.diff(symbols[field]).subs(zero) for field in FIELDS
    }
    second = {
        (left, right): g_fields.diff(symbols[left], symbols[right]).subs(zero)
        for left in FIELDS for right in FIELDS
    }
    return g0, first, second


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def direct_response_rows() -> list[dict[str, str]]:
    mapping: dict[str, dict[str, str]] = {}

    def row(output: str, default: str = "ZERO_EXACT") -> dict[str, str]:
        return {field: default for field in FIELDS} | {"output_id": output}

    mapping["O01"] = row("O01") | {"phi": "DIRECT_RECIPROCAL"}
    mapping["O02"] = row("O02") | {"sigma": "DIRECT"}
    mapping["O03"] = row("O03") | {"phi": "DIRECT", "sigma": "DIRECT"}
    mapping["O04"] = row("O04") | {"alpha": "DIRECT", "k": "DIRECT"}
    mapping["O05"] = row("O05") | {"sigma": "DIRECT"}
    mapping["O06"] = row("O06") | {name: "DIRECT_GAUGE_COMPONENT" for name in FIELDS[4:]}
    mapping["O07"] = row("O07") | {name: "DERIVATIVE_GAUGE_INVARIANT" for name in FIELDS[4:]}
    mapping["O08"] = row("O08") | {"alpha": "PIECEWISE_SET_VALUED", "k": "PIECEWISE_SET_VALUED"}
    mapping["O09"] = row("O09") | {
        "phi": "SELF_AND_DERIVATIVE",
        "sigma": "D04_GENERAL_DPHI_ONLY", "alpha": "D04_GENERAL_DPHI_ONLY",
        "k": "D04_GENERAL_DPHI_ONLY", "S10": "D04_GENERAL_DPHI_ONLY",
        "S11": "D04_GENERAL_DPHI_ONLY", "S20": "D04_GENERAL_DPHI_ONLY",
        "S21": "D04_GENERAL_DPHI_ONLY",
    }
    mapping["O10"] = dict(mapping["O09"]) | {"output_id": "O10"}
    mapping["O11"] = row("O11", "DERIVATIVE_COUPLING_CENSUSED")
    mapping["O12"] = row("O12", "CONDITIONAL_THROUGH_CURVATURE_AND_BOUNDARY")
    mapping["O13"] = row("O13") | {
        "phi": "DIRECT", "sigma": "DIRECT", "alpha": "DIRECT", "k": "DIRECT",
        "S10": "DIRECT_TANGENTIAL", "S20": "DIRECT_TANGENTIAL",
    }
    mapping["O14"] = row("O14", "DERIVATIVE_AND_FUNCTIONAL_DEPENDENT")
    mapping["O15"] = row("O15", "OBSERVER_PROTOCOL_OR_GLOBAL_PROFILE_DEPENDENT")
    mapping["O16"] = row("O16", "DISCRETE_NOT_JACOBIAN")
    return [mapping[f"O{i:02d}"] for i in range(1, 17)]


def main() -> None:
    checks: dict[str, str] = {}
    print("stage=kinematic_identities", flush=True)
    phi, sigma, alpha, k = sp.symbols("phi sigma alpha k", real=True)
    s10, s11, s20, s21 = sp.symbols("S10 S11 S20 S21", real=True)
    values = dict(zip(FIELDS, (phi, sigma, alpha, k, s10, s11, s20, s21)))
    E = coframe(values)
    det_E = sp.factor(E.det())
    det_g = sp.factor(-det_E**2)
    require("coframe_determinant", det_E == sp.exp(sigma), checks)
    require("metric_determinant", det_g == -sp.exp(2 * sigma), checks)

    r = sp.exp(sigma / 2 - alpha)
    q = sp.exp(sigma / 2 + alpha)
    D = sp.Matrix([[r, k * r], [0, q]])
    G_ang = sp.simplify(D.T * D)
    H = sp.simplify(G_ang / sp.exp(sigma))
    H_expected = sp.Matrix([
        [sp.exp(-2 * alpha), k * sp.exp(-2 * alpha)],
        [k * sp.exp(-2 * alpha), k**2 * sp.exp(-2 * alpha) + sp.exp(2 * alpha)],
    ])
    require("normalized_angular_metric",
            all(sp.simplify(item) == 0 for item in H - H_expected)
            and sp.simplify(H.det()) == 1, checks)
    require("H_sigma_independent", H.diff(sigma) == sp.zeros(2), checks)

    spatial = E.extract([1, 2, 3], [1, 2, 3])
    spatial_volume = sp.factor(spatial.det())
    boundary = E.extract([0, 2, 3], [0, 2, 3])
    boundary_volume = sp.factor(boundary.det())
    require("observer_rest_spatial_volume",
            sp.simplify(spatial_volume - sp.exp(phi + sigma)) == 0, checks)
    require("x_boundary_induced_volume",
            sp.simplify(boundary_volume - sp.exp(-phi + sigma)) == 0, checks)

    p0, p1, p2, p3 = sp.symbols("p0 p1 p2 p3", real=True)
    p = sp.Matrix([p0, p1, p2, p3])
    expected_components = sp.Matrix([
        sp.exp(phi) * (p0 - p2 * s10 - p3 * s20),
        sp.exp(-phi) * (p1 - p2 * s11 - p3 * s21),
        sp.exp(-sigma / 2 + alpha) * p2,
        sp.exp(-sigma / 2 - alpha) * (p3 - k * p2),
    ])
    require("general_covector_coframe_components",
            all(sp.simplify(item) == 0 for item in E.T * expected_components - p), checks)
    components = expected_components
    depth_norm = sp.factor((-components[0]**2 + sum(components[i]**2 for i in range(1, 4))))
    depth_norm_expected = sp.factor(
        -sp.exp(2 * phi) * (p0 - p2 * s10 - p3 * s20)**2
        + sp.exp(-2 * phi) * (p1 - p2 * s11 - p3 * s21)**2
        + sp.exp(-sigma + 2 * alpha) * p2**2
        + sp.exp(-sigma - 2 * alpha) * (p3 - k * p2)**2
    )
    require("general_depth_norm", sp.simplify(depth_norm - depth_norm_expected) == 0, checks)
    torus_invariant_norm = sp.factor(depth_norm.subs({p2: 0, p3: 0}))
    require("torus_invariant_dphi_norm",
            sp.simplify(torus_invariant_norm
                        - (-p0**2 * sp.exp(2 * phi) + p1**2 * sp.exp(-2 * phi))) == 0,
            checks)

    # Connection and gauge-curvature control.
    dl10, dl11, dl20, dl21 = sp.symbols("dl10 dl11 dl20 dl21")
    d0s11, d1s10, d0s21, d1s20 = sp.symbols("d0S11 d1S10 d0S21 d1S20")
    d0dl11, d1dl10, d0dl21, d1dl20 = sp.symbols("d0dl11 d1dl10 d0dl21 d1dl20")
    F1 = d0s11 - d1s10
    F2 = d0s21 - d1s20
    F1_gauge = (d0s11 - d0dl11) - (d1s10 - d1dl10)
    F2_gauge = (d0s21 - d0dl21) - (d1s20 - d1dl20)
    require("connection_curvature_gauge_invariant",
            sp.simplify(F1_gauge.subs(d0dl11, d1dl10) - F1) == 0
            and sp.simplify(F2_gauge.subs(d0dl21, d1dl20) - F2) == 0,
            checks)

    w1, w2 = sp.symbols("w1 w2", integer=True)
    dual_norm = sp.factor((sp.Matrix([[w1, w2]]) * G_ang.inv() * sp.Matrix([w1, w2]))[0])
    normalized_dual_norm = sp.factor((sp.Matrix([[w1, w2]]) * H.inv() * sp.Matrix([w1, w2]))[0])
    require("dual_character_common_scale_factor",
            sp.simplify(dual_norm - sp.exp(-sigma) * normalized_dual_norm) == 0, checks)

    # Exact scalar-curvature quadratic form for all first base jets.
    print("stage=metric_field_jets", flush=True)
    rates0 = sp.symbols(" ".join(f"d0_{name}" for name in FIELDS), real=True)
    rates1 = sp.symbols(" ".join(f"d1_{name}" for name in FIELDS), real=True)
    zero_fields = {symbol: 0 for symbol in values.values()}
    E_taylor = coframe_field_two_jet(values)
    coframe_jet_match = True
    for field in FIELDS:
        coframe_jet_match &= all(
            item == 0 for item in (E.diff(values[field]) - E_taylor.diff(values[field])).subs(zero_fields)
        )
        for other in FIELDS:
            coframe_jet_match &= all(
                item == 0 for item in (
                    E.diff(values[field], values[other])
                    - E_taylor.diff(values[field], values[other])
                ).subs(zero_fields)
            )
    require("coframe_taylor_matches_all_72_exact_field_jets", coframe_jet_match, checks)
    g0, field_first, field_second = metric_field_jets(values)
    print("stage=curvature_rate_form", flush=True)
    rate_by_direction = (rates0, rates1)
    dg_rate = []
    for direction in range(4):
        derivative = sp.zeros(4)
        if direction < 2:
            for index, field in enumerate(FIELDS):
                derivative += field_first[field] * rate_by_direction[direction][index]
        dg_rate.append(derivative)
    ddg_rate: list[list[sp.Matrix]] = []
    for first_direction in range(4):
        row = []
        for second_direction in range(4):
            derivative = sp.zeros(4)
            if first_direction < 2 and second_direction < 2:
                for i, left in enumerate(FIELDS):
                    for j, right in enumerate(FIELDS):
                        derivative += (field_second[(left, right)]
                                       * rate_by_direction[first_direction][i]
                                       * rate_by_direction[second_direction][j])
            row.append(derivative)
        ddg_rate.append(row)
    ricci_rate, scalar_rate = curvature_tensors_from_jets(g0, dg_rate, ddg_rate)
    scalar_rate = sp.expand(scalar_rate)
    require("curvature_rate_Ricci_symmetric", ricci_rate == ricci_rate.T, checks)
    require("curvature_rate_Ricci_trace_matches_scalar",
            sp.expand(-ricci_rate[0, 0] + ricci_rate[1, 1]
                      + ricci_rate[2, 2] + ricci_rate[3, 3] - scalar_rate) == 0,
            checks)
    print("stage=curvature_rate_hessian", flush=True)
    rate_variables = tuple(rates0) + tuple(rates1)
    rate_poly = sp.Poly(sp.expand(scalar_rate), *rate_variables)
    require("curvature_rate_form_quadratic", rate_poly.total_degree() <= 2, checks)
    require("curvature_rate_form_no_constant_or_linear",
            scalar_rate.subs({variable: 0 for variable in rate_variables}) == 0
            and all(sp.diff(scalar_rate, variable).subs({item: 0 for item in rate_variables}) == 0
                    for variable in rate_variables), checks)
    hessian = sp.hessian(scalar_rate, rate_variables)
    require("curvature_rate_hessian_symmetric", hessian == hessian.T, checks)

    hessian_rows = []
    for index, name in enumerate(RATE_NAMES):
        hessian_rows.append({"rate": name, **{
            RATE_NAMES[j]: str(sp.factor(hessian[index, j])) for j in range(len(RATE_NAMES))
        }})
    write_tsv("CURVATURE_RATE_HESSIAN.tsv", ["rate", *RATE_NAMES], hessian_rows)

    coupling_rows = []
    for i, left in enumerate(RATE_NAMES):
        for j in range(i, len(RATE_NAMES)):
            coefficient = sp.factor(hessian[i, j])
            if coefficient != 0:
                coupling_rows.append({
                    "left_rate": left, "right_rate": RATE_NAMES[j],
                    "hessian_entry": str(coefficient),
                    "relation": "SELF" if i == j else "CROSS",
                })
    write_tsv("CURVATURE_RATE_COUPLINGS.tsv",
              ["left_rate", "right_rate", "hessian_entry", "relation"], coupling_rows)

    ricci_components = tuple((mu, nu) for mu in range(4) for nu in range(mu, 4))
    ricci_component_names = tuple(f"R{mu}{nu}" for mu, nu in ricci_components)
    ricci_hessians = {
        component: sp.hessian(ricci_rate[component[0], component[1]], rate_variables)
        for component in ricci_components
    }
    ricci_coupling_rows = []
    for i, left in enumerate(RATE_NAMES):
        for j in range(i, len(RATE_NAMES)):
            entries = {
                name: sp.factor(ricci_hessians[component][i, j])
                for name, component in zip(ricci_component_names, ricci_components)
            }
            if any(value != 0 for value in entries.values()):
                ricci_coupling_rows.append({
                    "left_rate": left, "right_rate": RATE_NAMES[j],
                    "relation": "SELF" if i == j else "CROSS",
                    **{name: str(value) for name, value in entries.items()},
                })
    write_tsv("RICCI_RATE_COUPLINGS.tsv",
              ["left_rate", "right_rate", "relation", *ricci_component_names],
              ricci_coupling_rows)

    # Every pure second base jet, with first jets held zero. Linearity of the
    # metric two-jet chain rule permits one exact joint contraction.
    print("stage=curvature_second_jets", flush=True)
    second_symbols: dict[tuple[str, str], sp.Symbol] = {}
    for field in FIELDS:
        c00, c01, c11 = sp.symbols(f"d00_{field} d01_{field} d11_{field}", real=True)
        second_symbols[(field, "d00")] = c00
        second_symbols[(field, "d01")] = c01
        second_symbols[(field, "d11")] = c11
    dg_second = [sp.zeros(4) for _ in range(4)]
    ddg_second = [[sp.zeros(4) for _ in range(4)] for _ in range(4)]
    for field in FIELDS:
        ddg_second[0][0] += field_first[field] * second_symbols[(field, "d00")]
        ddg_second[0][1] += field_first[field] * second_symbols[(field, "d01")]
        ddg_second[1][0] += field_first[field] * second_symbols[(field, "d01")]
        ddg_second[1][1] += field_first[field] * second_symbols[(field, "d11")]
    ricci_second, scalar_second = curvature_tensors_from_jets(g0, dg_second, ddg_second)
    scalar_second = sp.expand(scalar_second)
    require("curvature_second_Ricci_symmetric", ricci_second == ricci_second.T, checks)
    require("curvature_second_Ricci_trace_matches_scalar",
            sp.expand(-ricci_second[0, 0] + ricci_second[1, 1]
                      + ricci_second[2, 2] + ricci_second[3, 3] - scalar_second) == 0,
            checks)
    print("stage=write_results", flush=True)
    all_second_symbols = tuple(second_symbols.values())
    require("curvature_second_jet_form_linear",
            sp.Poly(sp.expand(scalar_second), *all_second_symbols).total_degree() <= 1, checks)
    second_rows = []
    second_nonzero = 0
    for field in FIELDS:
        for derivative in ("d00", "d01", "d11"):
            variable = second_symbols[(field, derivative)]
            coefficient = sp.factor(sp.diff(scalar_second, variable))
            if coefficient != 0:
                second_nonzero += 1
            second_rows.append({
                "instrument": field, "second_jet": derivative,
                "curvature_response": str(coefficient),
                "status": "NONZERO" if coefficient != 0 else "ZERO_EXACT",
            })
    require("all_24_second_jets_covered", len(second_rows) == 24, checks)
    write_tsv("CURVATURE_SECOND_JET_RESPONSE.tsv",
              ["instrument", "second_jet", "curvature_response", "status"], second_rows)
    ricci_second_rows = []
    ricci_second_nonzero = 0
    for field in FIELDS:
        for derivative in ("d00", "d01", "d11"):
            variable = second_symbols[(field, derivative)]
            entries = {
                name: sp.factor(sp.diff(ricci_second[component[0], component[1]], variable))
                for name, component in zip(ricci_component_names, ricci_components)
            }
            if any(value != 0 for value in entries.values()):
                ricci_second_nonzero += 1
            ricci_second_rows.append({
                "instrument": field, "second_jet": derivative,
                "status": "NONZERO" if any(value != 0 for value in entries.values()) else "ZERO_EXACT",
                **{name: str(value) for name, value in entries.items()},
            })
    write_tsv("RICCI_SECOND_JET_RESPONSE.tsv",
              ["instrument", "second_jet", "status", *ricci_component_names],
              ricci_second_rows)

    response_rows = direct_response_rows()
    require("all_16_outputs_covered", len(response_rows) == 16, checks)
    write_tsv("DIRECT_RESPONSE_MATRIX.tsv", ["output_id", *FIELDS], response_rows)

    result = {
        "schema": "udt-metric-orchestra-rehearsal-algebra-1.0",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "instruments": len(FIELDS), "outputs": len(response_rows),
            "rate_variables": len(rate_variables), "curvature_hessian_entries": 256,
            "curvature_nonzero_upper_triangle_couplings": len(coupling_rows),
            "Ricci_nonzero_upper_triangle_couplings": len(ricci_coupling_rows),
            "curvature_second_jet_controls": len(second_rows),
            "curvature_second_jet_nonzero": second_nonzero,
            "Ricci_second_jet_nonzero": ricci_second_nonzero,
        },
        "exact_objects": {
            "coframe_determinant": str(det_E),
            "metric_determinant": str(det_g),
            "four_volume_density_x0_coordinate": "exp(sigma)",
            "four_volume_density_t_coordinate": "c_E*exp(sigma)",
            "spatial_volume_density": str(spatial_volume),
            "x_boundary_volume_density": str(boundary_volume),
            "normalized_angular_metric": [[str(item) for item in row] for row in H.tolist()],
            "general_depth_norm": str(depth_norm_expected),
            "torus_invariant_dphi_norm": str(torus_invariant_norm),
            "torus_curvature": [str(F1), str(F2)],
            "scalar_curvature_rate_form": str(scalar_rate),
        },
        "maximum_conclusion": "EXACT_TYPED_PARTIAL_R_GEOM_AND_COMMON_DOMAIN_CROSS_RESPONSE_ATLAS_ONLY",
    }
    (HERE / "ALGEBRA_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
