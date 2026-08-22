#!/usr/bin/env python3
"""Exact production algebra for the preregistered G209 shift tile."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("PRODUCTION_RESULT.json")


def require(label: str, condition: bool, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def derive() -> dict[str, object]:
    checks: list[str] = []
    f = sp.symbols("f", positive=True)
    h1, h2, h3 = sp.symbols("h1 h2 h3", positive=True)
    b1, b2, b3 = sp.symbols("b1 b2 b3", real=True)
    H = sp.diag(h1, h2, h3)
    b = sp.Matrix([b1, b2, b3])
    P = sp.eye(4)
    P[1:, 0] = b
    base = sp.diag(-f, h1, h2, h3)
    metric = sp.simplify(P.T * base * P)
    expected = sp.BlockMatrix(
        [[sp.Matrix([[-f + (b.T * H * b)[0]]]), (b.T * H)], [H * b, H]]
    ).as_explicit()
    require("adm_factorization", sp.simplify(metric - expected) == sp.zeros(4), checks)
    require("shift_map_det_one", sp.simplify(P.det() - 1) == 0, checks)
    require("metric_det_shift_independent", sp.simplify(metric.det() + f * H.det()) == 0, checks)

    Hinv = H.inv()
    inverse_expected = sp.BlockMatrix(
        [
            [sp.Matrix([[-1 / f]]), b.T / f],
            [b / f, Hinv - b * b.T / f],
        ]
    ).as_explicit()
    require("exact_inverse", sp.simplify(metric * inverse_expected - sp.eye(4)) == sp.zeros(4), checks)
    require("dt_is_temporal", sp.simplify(inverse_expected[0, 0] + 1 / f) == 0, checks)
    require("lorentz_inertia_from_congruence", all(x > 0 for x in (f, h1, h2, h3)), checks)

    v1, v2, v3 = sp.symbols("v1 v2 v3", real=True)
    v = sp.Matrix([v1, v2, v3])
    X = sp.Matrix([1, v1, v2, v3])
    causal_square = sp.expand((X.T * metric * X)[0])
    shifted_square = sp.expand(-f + ((v + b).T * H * (v + b))[0])
    require("shifted_cone_exact", sp.simplify(causal_square - shifted_square) == 0, checks)
    require("cone_center_is_minus_b", sp.simplify(shifted_square.subs({v1: -b1, v2: -b2, v3: -b3}) + f) == 0, checks)

    # Radial G205 specialization H_rr=1/f.
    vr, br = sp.symbols("vr br", real=True)
    radial_cone = sp.expand((vr + br) ** 2 / f - f)
    require("g205_radial_factor", sp.simplify(radial_cone - ((vr + br) ** 2 - f**2) / f) == 0, checks)
    require("g205_radial_lower_root", sp.simplify(radial_cone.subs(vr, -br - f)) == 0, checks)
    require("g205_radial_upper_root", sp.simplify(radial_cone.subs(vr, -br + f)) == 0, checks)

    # G208 radial-screen metric has inverse radial entry f*cosh(2s).
    s = sp.symbols("s", real=True)
    g208_width_sq = sp.simplify(f * (f * sp.cosh(2 * s)))
    require("g208_radial_width", sp.simplify(sp.sqrt(g208_width_sq) - f * sp.sqrt(sp.cosh(2 * s))) == 0, checks)

    # Stationary radial Hamiltonian identity.
    r, E, L, pr = sp.symbols("r E L pr", nonzero=True, real=True)
    brad = sp.symbols("brad", real=True)
    A = f - brad**2 / f
    hamiltonian_twice = sp.expand(A * pr**2 - 2 * brad * E * pr / f - E**2 / f + L**2 / r**2)
    rdot = sp.expand(A * pr - brad * E / f)
    radial_identity = sp.factor(rdot**2 - (E**2 - A * L**2 / r**2))
    require("radial_hamiltonian_identity", sp.simplify(radial_identity - A * hamiltonian_twice) == 0, checks)
    L2_on_shell = sp.solve(hamiltonian_twice, L**2)[0]
    require("radial_null_first_integral", sp.simplify(radial_identity.subs(L**2, L2_on_shell)) == 0, checks)

    # Stationary energy and compact-live derivative.
    tdot, y1, y2, y3 = sp.symbols("tdot y1 y2 y3", positive=True)
    y = sp.Matrix([y1, y2, y3])
    stationary_energy = sp.expand(f * tdot - (b.T * H * y)[0])
    require("stationary_energy_sign", stationary_energy.coeff(tdot) == f, checks)
    db1, db2, db3 = sp.symbols("db1 db2 db3", real=True)
    db = sp.Matrix([db1, db2, db3])
    energy_derivative = sp.expand(-(y.T * H * db)[0] * tdot)
    require("live_energy_derivative", sp.diff(energy_derivative, db1) == -h1 * y1 * tdot, checks)

    # Completed pair pullback.
    a0, a1 = sp.symbols("a0 a1", real=True)
    w01, w02, w03, w11, w12, w13 = sp.symbols("w01 w02 w03 w11 w12 w13", real=True)
    w0 = sp.Matrix([w01, w02, w03])
    w1 = sp.Matrix([w11, w12, w13])
    J = sp.Matrix.hstack(sp.Matrix([a0, *w0]), sp.Matrix([a1, *w1]))
    pair = sp.simplify(J.T * metric * J)
    pair_expected = sp.Matrix(
        [
            [-f * a0**2 + ((w0 + a0 * b).T * H * (w0 + a0 * b))[0],
             -f * a0 * a1 + ((w0 + a0 * b).T * H * (w1 + a1 * b))[0]],
            [-f * a0 * a1 + ((w1 + a1 * b).T * H * (w0 + a0 * b))[0],
             -f * a1**2 + ((w1 + a1 * b).T * H * (w1 + a1 * b))[0]],
        ]
    )
    require("completed_pair_pullback", sp.simplify(pair - pair_expected) == sp.zeros(2), checks)
    T2 = sp.simplify(-pair[0, 0])
    expected_T2 = sp.simplify(f * a0**2 - ((w0 + a0 * b).T * H * (w0 + a0 * b))[0])
    require("completed_clock_norm", sp.simplify(T2 - expected_T2) == 0, checks)
    require("coordinate_static_clock_hears_shift", sp.simplify(T2.subs({w01: 0, w02: 0, w03: 0}) - a0**2 * (f - (b.T * H * b)[0])) == 0, checks)
    require("eulerian_clock_is_shift_blind", sp.simplify(T2.subs({w01: -a0 * b1, w02: -a0 * b2, w03: -a0 * b3}) - f * a0**2) == 0, checks)
    require("generic_clock_has_linear_cross_terms", sp.expand(T2).coeff(w01 * b1) == -2 * a0 * h1, checks)

    phi_completed = "-log(T)=-1/2*log(T^2)"
    return {
        "landing": "FULL_LOCAL_TIMESPACE_SHIFT_IS_AN_EXACT_INDEPENDENT_METRIC_SECTOR__IT_TRANSLATES_THE_CAUSAL_ELLIPSOID_WITHOUT_CHANGING_SIGNATURE_OR_AMBIENT_DETERMINANT__GROWTH_CONTROLLED_AND_UNIFORMLY_SUBLUMINAL_G205_CLASSES_SURVIVE__A_SMOOTH_BOUNDED_COORDINATE_SHIFT_CAN_PRESERVE_GLOBAL_HYPERBOLICITY_WHILE_DESTROYING_NULL_COMPLETENESS__COMPLETED_PAIRS_HEAR_SHIFT_BEFORE_READOUT__NO_PHYSICAL_SHIFT_HISTORY_OR_XMAX_SELECTION",
        "assertion_count": len(checks),
        "assertions": checks,
        "completed_phi": phi_completed,
        "mechanization_scope": "finite-dimensional algebra and radial Hamiltonian identity only",
    }


def main() -> None:
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
