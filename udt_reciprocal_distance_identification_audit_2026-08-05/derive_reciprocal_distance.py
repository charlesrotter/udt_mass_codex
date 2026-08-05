#!/usr/bin/env python3
"""Exact primary derivation for reciprocal depth versus physical separation."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("DERIVATION_RESULT.json")


def require(name: str, condition: bool, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def lorentz_generators() -> list[sp.Matrix]:
    out: list[sp.Matrix] = []
    for i in range(1, 4):
        g = sp.zeros(4)
        g[0, i] = 1
        g[i, 0] = 1
        out.append(g)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        g = sp.zeros(4)
        g[i, j] = 1
        g[j, i] = -1
        out.append(g)
    return out


def main() -> None:
    checks: dict[str, bool] = {}
    d, d1, d2 = sp.symbols("d d1 d2", real=True)
    z, h = sp.symbols("z h", positive=True)
    r = sp.symbols("r", nonnegative=True)
    kappa, xmax = sp.symbols("kappa xmax", positive=True)
    k_dual = sp.Matrix([[0, 1], [1, 0]])
    eta = sp.diag(-1, 1)

    def D(arg: sp.Expr) -> sp.Matrix:
        return sp.diag(sp.exp(-arg), sp.exp(arg))

    require("dual_pairing_preserved", sp.simplify(D(d).T * k_dual * D(d) - k_dual) == sp.zeros(2), checks)
    require("composition", sp.simplify(D(d2) * D(d1) - D(d1 + d2)) == sp.zeros(2), checks)
    require("reversal", sp.simplify(D(-d) * D(d) - sp.eye(2)) == sp.zeros(2), checks)
    require("determinant_one", sp.simplify(D(d).det() - 1) == 0, checks)
    require("signed_ratio", sp.simplify(D(d)[1, 1] / D(d)[0, 0] - sp.exp(2 * d)) == 0, checks)
    require("even_half_trace", sp.simplify(sp.trace(D(d)) / 2 - sp.cosh(d)) == 0, checks)
    require("physical_eta_not_preserved", sp.simplify(D(d).T * eta * D(d) - eta) != sp.zeros(2), checks)

    # Two distinct bounded profiles with identical origin value, slope, monotonicity and Xmax limit.
    f_tanh = xmax * sp.tanh(kappa * r)
    f_exp = xmax * (1 - sp.exp(-kappa * r))
    require("profiles_zero", f_tanh.subs(r, 0) == 0 and f_exp.subs(r, 0) == 0, checks)
    require("profiles_same_slope", sp.diff(f_tanh, r).subs(r, 0) == sp.diff(f_exp, r).subs(r, 0), checks)
    require("profiles_limit", sp.limit(f_tanh, r, sp.oo) == xmax and sp.limit(f_exp, r, sp.oo) == xmax, checks)
    require("profiles_distinct", sp.simplify(sp.diff(f_tanh, r, 2).subs(r, 0) - sp.diff(f_exp, r, 2).subs(r, 0)) != 0, checks)

    # Exact subadditivity numerators after x=tanh(a), y=tanh(b) and u=exp(-a), v=exp(-b).
    x, y, u, v = sp.symbols("x y u v", positive=True)
    tanh_gap = sp.factor((x + y) - (x + y) / (1 + x * y))
    exp_gap = sp.factor((1 - u) + (1 - v) - (1 - u * v))
    require("tanh_subadditive_form", tanh_gap == x * y * (x + y) / (x * y + 1), checks)
    require("exp_subadditive_form", exp_gap == (u - 1) * (v - 1), checks)

    # Exact pointwise factorization freedom: the complete coframe is unchanged while z changes.
    bar = sp.Matrix([[2, 3], [5, 7]])
    dz = sp.diag(1 / z, z)
    dh_inv = sp.diag(h, 1 / h)
    shifted = sp.diag(1 / (z * h), z * h) * dh_inv * bar
    require("factorization_same_coframe", sp.simplify(shifted - dz * bar) == sp.zeros(2), checks)

    zp, zq, hp, hq = map(sp.Rational, (2, 3, 5, 7))
    old_ratio = zq / zp
    new_ratio = (zq * hq) / (zp * hp)
    require("endpoint_depth_ratio_changes", old_ratio != new_ratio, checks)

    # Static diagonal control: reciprocal coordinate-covector scaling maps orthonormal coframes
    # exactly, leaving identity as their physical orthonormal comparison along the registered path.
    c = sp.symbols("c", positive=True)
    theta_p = sp.diag(c / zp, zp)
    theta_q = sp.diag(c / zq, zq)
    coordinate_covector_transport = sp.diag(zp / zq, zq / zp)
    require("static_coordinate_transport_maps_coframe", coordinate_covector_transport * theta_p == theta_q, checks)

    # Full Lorentz holonomy has only the scalar centralizer in End(R^4).
    unknowns = sp.symbols("x0:16")
    generic = sp.Matrix(4, 4, unknowns)
    equations: list[sp.Expr] = []
    for generator in lorentz_generators():
        equations.extend(list(generic * generator - generator * generic))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, unknowns)
    centralizer_rank = coefficient_matrix.rank()
    require("full_lorentz_centralizer_rank_15", centralizer_rank == 15, checks)
    require("full_lorentz_centralizer_dimension_one", 16 - centralizer_rank == 1, checks)

    lam = sp.symbols("lam", real=True)
    extension = sp.diag(-1, 1, lam, lam)
    require("founded_extension_not_scalar", extension[0, 0] != extension[1, 1], checks)
    require("founded_extension_not_full_holonomy_invariant", extension * lorentz_generators()[0] != lorentz_generators()[0] * extension, checks)

    # Angular separation witness: constant reciprocal depth cannot distinguish angularly separated
    # events, while the supplied spherical metric sector gives a nonzero short equatorial arc.
    radius, alpha = sp.symbols("R alpha", positive=True)
    delta_angular = sp.Integer(0)
    angular_arc = radius * alpha
    require("same_depth_nonzero_angular_arc", delta_angular == 0 and angular_arc != 0, checks)

    result = {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "checks": checks,
        "check_count": len(checks),
        "derived_reciprocal_subgroup_readouts": {
            "signed_depth": "delta(D)=1/2 log(D_22/D_11)",
            "symmetric_magnitude": "rho(D)=arcosh(Tr(D)/2)=abs(delta)",
            "composition": "delta(D2 D1)=delta2+delta1",
            "triangle": "rho(D2 D1)<=rho(D2)+rho(D1)",
        },
        "centralizer": {"constraint_rank": centralizer_rank, "dimension": 16 - centralizer_rank},
        "profile_counterfamily": {
            "profile_1": "Xmax*tanh(kappa*rho)",
            "profile_2": "Xmax*(1-exp(-kappa*rho))",
            "same_origin_slope": "Xmax*kappa",
            "same_limit": "Xmax",
            "different_second_derivative_at_origin": "0 versus -Xmax*kappa^2",
        },
        "maximum_conclusion": (
            "SIGNED_DEPTH_AND_RECIPROCAL_MAGNITUDE_DERIVED_FROM_SUPPLIED_FOUNDED_ARROW__"
            "PHYSICAL_SEPARATION_IDENTIFICATION_AND_COMPLETE_METRIC_EXTRACTION_NOT_DERIVED"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
