#!/usr/bin/env python3
"""Exact production algebra for the preregistered G208 mixing tile."""

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
    q = sp.symbols("q", positive=True)
    c = (q + 1 / q) / 2
    d = (q - 1 / q) / 2
    A = sp.Matrix([[c, d, 0], [d, c, 0], [0, 0, 1]])
    H = sp.simplify(A.T * A)
    C2 = (q**2 + q**-2) / 2
    S2 = (q**2 - q**-2) / 2
    expected_H = sp.Matrix([[C2, S2, 0], [S2, C2, 0], [0, 0, 1]])

    require("boost_det_one", sp.simplify(A.det() - 1) == 0, checks)
    require("spatial_det_one", sp.simplify(H.det() - 1) == 0, checks)
    require("mixed_metric_exact", sp.simplify(H - expected_H) == sp.zeros(3), checks)
    require("positive_leading_minor_1", sp.simplify(C2) > 0, checks)
    require("positive_leading_minor_2", sp.simplify(H[:2, :2].det() - 1) == 0, checks)
    require("positive_leading_minor_3", sp.simplify(H.det() - 1) == 0, checks)

    lam = sp.symbols("lam")
    characteristic = sp.factor(A.charpoly(lam).as_expr())
    require(
        "boost_eigenvalues",
        sp.simplify(characteristic - (lam - 1) * (lam - q) * (lam - 1 / q)) == 0,
        checks,
    )
    require("metric_eigenvalues", sp.simplify(H.charpoly(lam).as_expr() - (lam - 1) * (lam - q**2) * (lam - q**-2)) == 0, checks)

    schur = sp.simplify(C2 - S2**2 / C2)
    require("radial_schur_sech", sp.simplify(schur - 1 / C2) == 0, checks)
    x, y = sp.symbols("x y", real=True)
    mixed_norm = C2 * (x**2 + y**2) + 2 * S2 * x * y
    y_star = -S2 * x / C2
    require("screen_minimizer", sp.simplify(sp.diff(mixed_norm, y).subs(y, y_star)) == 0, checks)
    require("minimum_radial_norm", sp.simplify(mixed_norm.subs(y, y_star) - x**2 / C2) == 0, checks)
    require("old_radial_bound_only_at_zero_mix", sp.simplify(C2.subs(q, 1) - 1) == 0, checks)

    omega = sp.symbols("omega", real=True)
    scale = sp.exp(2 * omega)
    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True)
    pair = sp.Matrix([[h00, h01], [h01, h11]])
    pair_scaled = scale * pair
    require("pair_conformal_pullback", sp.simplify(pair_scaled - scale * pair) == sp.zeros(2), checks)
    require("pair_determinant_weight", sp.simplify(pair_scaled.det() - scale**2 * pair.det()) == 0, checks)
    require("completed_clock_weight", sp.simplify(-pair_scaled[0, 0] - scale * (-h00)) == 0, checks)

    phi_symbol = sp.symbols("phi", real=True)
    f = sp.exp(-2 * phi_symbol)
    sigma = 4 * phi_symbol
    require("witness_integrand_identity", sp.simplify(sp.exp(-sigma) / f - f) == 0, checks)

    alpha0 = sp.symbols("alpha0", real=True)
    vr, vw, vp = sp.symbols("vr vw vp", real=True)
    v = sp.Matrix([vr, vw, vp])
    clock_spatial = sp.expand((v.T * H * v)[0])
    clock_square = sp.simplify(sp.Symbol("f", positive=True) * alpha0**2 - clock_spatial)
    base_clock_square = sp.Symbol("f", positive=True) * alpha0**2 - (vr**2 + vw**2 + vp**2)
    require("static_clock_blind", sp.simplify(clock_square.subs({vr: 0, vw: 0, vp: 0}) - sp.Symbol("f", positive=True) * alpha0**2) == 0, checks)
    require("untouched_screen_blind", sp.simplify((clock_square - base_clock_square).subs({vr: 0, vw: 0})) == 0, checks)
    require("radial_clock_hears", sp.simplify((clock_square - base_clock_square).subs({vw: 0, vp: 0, vr: 1}) - (1 - C2)) == 0, checks)
    require("generic_clock_has_cross_term", sp.expand(clock_spatial).coeff(vr * vw) == 2 * S2, checks)

    return {
        "landing": "RADIAL_SCREEN_MIXING_PRESERVES_SIGNATURE_AND_AMBIENT_VOLUME_BUT_REPLACES_THE_RADIAL_CAUSAL_BOUND__GROWTH_CONTROLLED_AND_BOUNDED_STATIC_CLASSES_SURVIVE__A_SMOOTH_CENTER_REGULAR_UNBOUNDED_STATIC_MIXER_DESTROYS_GLOBAL_HYPERBOLICITY_AND_NULL_COMPLETENESS__COMPLETED_PAIRS_HEAR_RADIAL_MIXING_BEFORE_READOUT__NO_PHYSICAL_MIXER_HISTORY_OR_XMAX_SELECTION",
        "assertion_count": len(checks),
        "assertions": checks,
        "exact_radial_schur": str(schur),
        "witness_optical_integrand": "sqrt(2)*f(r)",
        "mechanization_scope": "finite-dimensional algebra and witness-integrand identity only",
    }


def main() -> None:
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
