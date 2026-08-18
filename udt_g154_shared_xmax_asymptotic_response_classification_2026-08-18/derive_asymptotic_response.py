#!/usr/bin/env python3
"""Production symbolic derivation for the preregistered G154 classification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def _s(value: sp.Expr) -> str:
    return str(sp.simplify(value))


def derive() -> dict[str, object]:
    q = sp.symbols("q", positive=True)
    x_star = sp.symbols("X_star", positive=True, finite=True)
    z1, z2 = sp.symbols("z1 z2", real=True)

    # A supplied fixed-scale Mobius law is exactly additive after artanh.
    mobius_residual = sp.simplify(
        x_star * sp.tanh(z1 + z2)
        - (x_star * sp.tanh(z1) + x_star * sp.tanh(z2))
        / (1 + sp.tanh(z1) * sp.tanh(z2))
    )

    # The actually adopted normalized law contains no dimensionful scale and therefore cannot
    # select one.  A nonconstant X(q) leaves chi=tanh(phi) and its composition untouched.
    chi_composition_residual = sp.simplify(
        sp.tanh(z1 + z2)
        - (sp.tanh(z1) + sp.tanh(z2)) / (1 + sp.tanh(z1) * sp.tanh(z2))
    )
    x_countermodel = x_star + q
    x_countermodel_derivative = sp.diff(x_countermodel, q)

    # Hold the reciprocal profile fixed and vary only retained common scale through L=q^-ell.
    # This is stronger than comparing unrelated phi profiles: rho(q) is identical in all classes.
    fixed_scale: dict[str, dict[str, str]] = {}
    temporal_dual_matches = True
    p_profile = sp.Rational(1, 3)
    for label, ell in (
        ("quiet", sp.Rational(1, 2)),
        ("finite_live", sp.Rational(1, 3)),
        ("divergent", sp.Rational(1, 4)),
    ):
        by_sign: dict[str, str] = {}
        for epsilon in (-1, 1):
            phi = epsilon * (-p_profile * sp.log(q))
            # The witness chooses L=q^-ell, so n=q^ell*(-d/dq).
            n_phi = sp.simplify(q**ell * (-sp.diff(phi, q)))
            response = sp.simplify(x_star * sp.sech(phi) ** 2 * n_phi)
            # The time-live dual chooses T=q^-ell and has u=q^ell*(-d/dq).
            u_phi = sp.simplify(q**ell * (-sp.diff(phi, q)))
            temporal_response = sp.simplify(x_star * sp.sech(phi) ** 2 * u_phi)
            temporal_dual_matches = temporal_dual_matches and sp.simplify(temporal_response - response) == 0
            by_sign[str(epsilon)] = _s(sp.limit(response, q, 0, dir="+"))
        fixed_scale[label] = by_sign

    # A smooth interior critical witness with positive oscillatory L has no response limit.
    p_critical = p_profile
    amplitude = sp.Rational(1, 2)
    phi_critical = -p_critical * sp.log(q)
    oscillatory_response = sp.simplify(
        x_star
        * sp.sech(phi_critical) ** 2
        * p_critical
        * q ** (sp.Rational(1, 3) - 1)
        * (1 + amplitude * sp.sin(1 / q))
    )
    n = sp.symbols("n", positive=True, integer=True)
    q_plus = 1 / (sp.pi / 2 + 2 * sp.pi * n)
    q_minus = 1 / (3 * sp.pi / 2 + 2 * sp.pi * n)
    oscillatory_limits = {
        "sin_plus_one": _s(sp.limit(oscillatory_response.subs(q, q_plus), n, sp.oo)),
        "sin_minus_one": _s(sp.limit(oscillatory_response.subs(q, q_minus), n, sp.oo)),
    }

    # Live-X endpoint witnesses all share X(q)->X_star and use the quiet p=1/2 metric profile.
    p_live = sp.Rational(1, 2)
    phi_live = -p_live * sp.log(q)
    n_phi_live = sp.simplify(q**p_live * (-sp.diff(phi_live, q)))
    live_scale: dict[str, str] = {}
    for label, exponent in (
        ("quiet", sp.Integer(1)),
        ("finite_live", sp.Rational(1, 2)),
        ("divergent", sp.Rational(1, 4)),
    ):
        x_field = x_star + q**exponent
        n_x = sp.simplify(q**p_live * (-sp.diff(x_field, q)))
        response = sp.simplify(
            sp.tanh(phi_live) * n_x + x_field * sp.sech(phi_live) ** 2 * n_phi_live
        )
        live_scale[label] = _s(sp.limit(response, q, 0, dir="+"))

    # Same finite endpoint but two different subsequential responses.
    x_nonconvergent = x_star + q * sp.sin(q ** sp.Rational(-1, 2))
    n_x_nonconvergent = sp.simplify(q**p_live * (-sp.diff(x_nonconvergent, q)))
    response_nonconvergent = sp.simplify(
        sp.tanh(phi_live) * n_x_nonconvergent
        + x_nonconvergent * sp.sech(phi_live) ** 2 * n_phi_live
    )
    q_cos_plus = 1 / (2 * sp.pi * n) ** 2
    q_cos_minus = 1 / ((2 * n + 1) * sp.pi) ** 2
    live_nonconvergent_limits = {
        "cos_plus_one": _s(sp.limit(response_nonconvergent.subs(q, q_cos_plus), n, sp.oo)),
        "cos_minus_one": _s(sp.limit(response_nonconvergent.subs(q, q_cos_minus), n, sp.oo)),
    }

    # Exact cancellation: live scale and profile terms are individually nonzero, rho is constant.
    c = sp.symbols("C", positive=True)
    x_cancel = c / sp.tanh(phi_live)
    rho_cancel = sp.simplify(x_cancel * sp.tanh(phi_live))
    n_x_cancel = sp.simplify(q**p_live * (-sp.diff(x_cancel, q)))
    cancellation_response = sp.simplify(
        sp.tanh(phi_live) * n_x_cancel
        + x_cancel * sp.sech(phi_live) ** 2 * n_phi_live
    )

    checks = {
        "mobius_composition_exact": mobius_residual == 0,
        "normalized_composition_exact_without_scale": chi_composition_residual == 0,
        "normalized_composition_allows_nonconstant_scale": x_countermodel_derivative != 0,
        "fixed_quiet_both_signs": fixed_scale["quiet"] == {"-1": "0", "1": "0"},
        "fixed_finite_both_signs": fixed_scale["finite_live"]
        == {"-1": "-4*X_star/3", "1": "4*X_star/3"},
        "fixed_divergent_both_signs": fixed_scale["divergent"]
        == {"-1": "-oo", "1": "oo"},
        "fixed_nonconvergent_subsequences_differ": len(set(oscillatory_limits.values())) == 2,
        "temporal_dual_matches_spatial_classes": temporal_dual_matches,
        "live_endpoint_quiet": live_scale["quiet"] == "0",
        "live_endpoint_finite": live_scale["finite_live"] == "-1/2",
        "live_endpoint_divergent": live_scale["divergent"] == "-oo",
        "live_nonconvergent_subsequences_differ": len(set(live_nonconvergent_limits.values())) == 2,
        "cancellation_rho_constant": rho_cancel == c,
        "cancellation_response_zero": cancellation_response == 0,
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing_candidate": "EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED",
        "mobius_residual": _s(mobius_residual),
        "normalized_composition_countermodel": {
            "composition_residual": _s(chi_composition_residual),
            "scale_field": _s(x_countermodel),
            "scale_derivative": _s(x_countermodel_derivative),
        },
        "fixed_scale_limits": fixed_scale,
        "fixed_nonconvergent_subsequences": oscillatory_limits,
        "live_scale_limits": live_scale,
        "live_nonconvergent_subsequences": live_nonconvergent_limits,
        "cancellation": {
            "rho": _s(rho_cancel),
            "response": _s(cancellation_response),
            "scale_endpoint": _s(sp.limit(x_cancel, q, 0, dir="+")),
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
