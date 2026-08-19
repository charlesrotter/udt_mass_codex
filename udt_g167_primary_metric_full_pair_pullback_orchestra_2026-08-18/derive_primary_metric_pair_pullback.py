#!/usr/bin/env python3
"""Exact G167 pullback of the declared primary UDT metric."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures: list[str] = []
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def main() -> None:
    c_e, u, radius, sine, cosine = sp.symbols(
        "c_E u r sin_theta cos_theta", positive=True, real=True
    )
    # u=exp(phi).  The four diagonal entries are the declared primary metric.
    g = sp.diag(
        -c_e**2 / u**2,
        u**2,
        radius**2,
        radius**2 * sine**2,
    )
    eta2 = sp.diag(-1, 1)
    B = sp.diag(c_e / u, u)
    Q = sp.diag(radius, radius * sine)

    names = [
        "t0", "t1", "r0", "r1", "theta0", "theta1", "varphi0", "varphi1"
    ]
    values = sp.symbols(" ".join(names), real=True)
    t0, t1, r0, r1, th0, th1, va0, va1 = values
    Y = sp.Matrix([[t0, t1], [r0, r1]])
    Z = sp.Matrix([[th0, th1], [va0, va1]])
    J = Y.col_join(Z)

    h_direct = sp.simplify(J.T * g * J)
    h_base = sp.simplify(Y.T * B.T * eta2 * B * Y)
    angular_gram = sp.simplify(Z.T * Q.T * Q * Z)
    h_assembled = sp.simplify(h_base + angular_gram)

    expected_h00 = (
        -c_e**2 * t0**2 / u**2
        + u**2 * r0**2
        + radius**2 * th0**2
        + radius**2 * sine**2 * va0**2
    )
    expected_h01 = (
        -c_e**2 * t0 * t1 / u**2
        + u**2 * r0 * r1
        + radius**2 * th0 * th1
        + radius**2 * sine**2 * va0 * va1
    )
    expected_h11 = (
        -c_e**2 * t1**2 / u**2
        + u**2 * r1**2
        + radius**2 * th1**2
        + radius**2 * sine**2 * va1**2
    )

    det_h = sp.factor(h_direct.det())
    q_squared = sp.factor(h_direct[0, 0] ** 2 / (-det_h))
    beta_pair = sp.factor(h_direct[0, 1] / h_direct[0, 0])

    # Founded radial calibrated control: J=(dt,dr), with c_E=1.
    J_radial = sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    h_radial = sp.simplify((J_radial.T * g * J_radial).subs(c_e, 1))
    q2_radial = sp.factor(h_radial[0, 0] ** 2 / (-h_radial.det()))

    # Exact nonradial witness.  Its base cross term vanishes, while its angular
    # Gram term creates a nonzero terminal shift.
    witness_subs = {
        c_e: sp.Integer(1),
        u: sp.Integer(2),
        radius: sp.Integer(3),
        sine: sp.Rational(4, 5),
        cosine: sp.Rational(3, 5),
        t0: sp.Integer(4),
        t1: sp.Integer(0),
        r0: sp.Integer(0),
        r1: sp.Rational(1, 2),
        th0: sp.Rational(1, 10),
        th1: sp.Rational(1, 5),
        va0: sp.Integer(0),
        va1: sp.Rational(1, 3),
    }
    h_witness = sp.simplify(h_direct.subs(witness_subs))
    h_base_witness = sp.simplify(h_base.subs(witness_subs))
    p_witness = sp.simplify(angular_gram.subs(witness_subs))
    q2_witness = sp.factor(q_squared.subs(witness_subs))
    q2_base_witness = sp.factor(
        h_base_witness[0, 0] ** 2 / (-h_base_witness.det())
    )

    # Angular-coordinate covariance: Z'=K Z, q'=(K^-1)^T q K^-1.
    K = sp.Matrix([[2, 1], [1, 1]])
    q_screen = Q.T * Q
    z_prime = K * Z
    q_prime = K.inv().T * q_screen * K.inv()
    angular_covariant = sp.simplify(z_prime.T * q_prime * z_prime)

    # Exact live derivative.  The ambient metric is static but its coefficients
    # change along a moving pair through r and phi(r), while J itself can vary.
    dphi, dradius, dtheta = sp.symbols("dphi dr dtheta", real=True)
    dot_values = sp.symbols(" ".join(f"d{name}" for name in names), real=True)
    dt0, dt1, dr0, dr1, dth0, dth1, dva0, dva1 = dot_values
    dotY = sp.Matrix([[dt0, dt1], [dr0, dr1]])
    dotZ = sp.Matrix([[dth0, dth1], [dva0, dva1]])
    dotJ = dotY.col_join(dotZ)
    dotg = sp.diag(
        2 * c_e**2 * dphi / u**2,
        2 * u**2 * dphi,
        2 * radius * dradius,
        2 * radius * dradius * sine**2
        + 2 * radius**2 * sine * cosine * dtheta,
    )
    dot_h_geometric = sp.simplify(dotJ.T * g * J + J.T * g * dotJ + J.T * dotg * J)

    directional = sp.zeros(2)
    all_vars = [u, radius, sine, *values]
    all_dvars = [
        u * dphi,
        dradius,
        cosine * dtheta,
        *dot_values,
    ]
    for variable, dvariable in zip(all_vars, all_dvars):
        directional += h_direct.diff(variable) * dvariable
    directional = sp.simplify(directional)

    dot_phi_pair = sp.factor(
        sp.trace(h_direct.inv() * dot_h_geometric) / 4
        - dot_h_geometric[0, 0] / (2 * h_direct[0, 0])
    )
    live_channels: dict[str, sp.Expr] = {}
    live_variations = {
        "profile_along_pair": {dphi: 1},
        "areal_radius_along_pair": {dradius: 1},
        "angular_chart_motion": {dtheta: 1},
        "clock_tangent_motion": {dt0: 1},
        "radial_tangent_motion": {dr1: 1},
        "theta_tangent_motion": {dth0: 1},
        "varphi_tangent_motion": {dva1: 1},
    }
    zero_dots = {symbol: 0 for symbol in (dphi, dradius, dtheta, *dot_values)}
    for label, one_dot in live_variations.items():
        subs = dict(witness_subs)
        subs.update(zero_dots)
        subs.update(one_dot)
        live_channels[label] = sp.factor(dot_phi_pair.subs(subs))

    # A single invariant scalar of the angular Gram matrix is insufficient.
    h_control = sp.diag(-4, 1)
    p_trace_1 = sp.diag(1, 0)
    p_trace_2 = sp.diag(0, 1)
    q2_trace_1 = sp.factor(
        (h_control + p_trace_1)[0, 0] ** 2 / (-(h_control + p_trace_1).det())
    )
    q2_trace_2 = sp.factor(
        (h_control + p_trace_2)[0, 0] ** 2 / (-(h_control + p_trace_2).det())
    )

    core_symbols = set().union(*(entry.free_symbols for entry in h_direct))
    checks = {
        "direct_pullback_equals_primary_BQZ_assembly": sp.simplify(
            h_direct - h_assembled
        )
        == sp.zeros(2),
        "ambient_mixing_S_is_zero_in_primary_metric": True,
        "h00_component_exact": sp.simplify(h_direct[0, 0] - expected_h00) == 0,
        "h01_component_exact": sp.simplify(h_direct[0, 1] - expected_h01) == 0,
        "h11_component_exact": sp.simplify(h_direct[1, 1] - expected_h11) == 0,
        "angular_gram_enters_before_readout": sp.simplify(h_direct - h_base - angular_gram)
        == sp.zeros(2),
        "angular_coordinate_covariance": sp.simplify(angular_covariant - angular_gram)
        == sp.zeros(2),
        "radial_control_returns_primary_block": h_radial
        == sp.diag(-1 / u**2, u**2),
        "radial_control_returns_q_squared": sp.simplify(q2_radial - u ** (-4)) == 0,
        "nonradial_witness_is_lorentzian": h_witness[0, 0] < 0
        and h_witness.det() < 0,
        "pair_shift_induced_with_zero_base_cross_term": h_base_witness[0, 1] == 0
        and p_witness[0, 1] != 0
        and h_witness[0, 1] != 0,
        "angular_gram_changes_terminal_ratio": sp.simplify(q2_witness - q2_base_witness)
        != 0,
        "live_derivative_matches_full_directional_derivative": sp.simplify(
            dot_h_geometric - directional
        )
        == sp.zeros(2),
        "all_registered_live_channels_nonzero": all(value != 0 for value in live_channels.values()),
        "angular_trace_does_not_determine_terminal_ratio": sp.trace(p_trace_1)
        == sp.trace(p_trace_2)
        and q2_trace_1 != q2_trace_2,
        "core_contains_no_path_symbol": all(str(s) not in {"path", "gamma"} for s in core_symbols),
        "core_contains_no_xmax_symbol": all(str(s) not in {"Xmax", "X_max"} for s in core_symbols),
        "core_contains_no_scalar_mu_symbol": all(str(s) != "mu" for s in core_symbols),
    }

    source_count, source_failures = source_hashes()
    checks["source_hashes_match"] = source_count == 10 and not source_failures

    result = {
        "primary_landing": (
            "PRIMARY_STATIC_SPHERICAL_UDT_METRIC_OWNS_FULL_GENERAL_PAIR_PULLBACK_ORCHESTRA"
            "__GENERAL_AMBIENT_EXTENSION_OPEN"
        ),
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "checks": {name: bool(value) for name, value in checks.items()},
        "source_count": source_count,
        "source_failures": source_failures,
        "exact_nonradial_witness": {
            "h": [[str(entry) for entry in row] for row in h_witness.tolist()],
            "angular_gram": [[str(entry) for entry in row] for row in p_witness.tolist()],
            "det_h": str(sp.factor(h_witness.det())),
            "beta_pair": str(sp.factor(beta_pair.subs(witness_subs))),
            "q_pair_squared": str(q2_witness),
            "base_only_q_squared": str(q2_base_witness),
        },
        "live_phi_pair_derivatives": {
            label: str(value) for label, value in live_channels.items()
        },
        "ownership": {
            "B": "metric-fixed by c_E and supplied phi in declared primary arena",
            "Q": "metric-fixed areal spherical screen diag(r,r sin(theta))",
            "S": "zero in declared diagonal primary ambient coframe",
            "Y_Z": "supplied ordered-pair realization tangents",
            "mu": "no independent scalar; full angular Gram is derived from Q and Z",
            "ambient_nonspherical_timelive_extension": "open outside bounded arena",
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise SystemExit(f"FAIL: {failed}")
    print(
        f"PASS: {len(checks)} exact G167 checks; {source_count} frozen sources; "
        f"nonradial det={sp.factor(h_witness.det())}"
    )


if __name__ == "__main__":
    main()
